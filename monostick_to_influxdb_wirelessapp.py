#!/usr/bin/python
# coding: UTF-8

### TWELITE 無線データのHTTP送信スクリプト
# 本ソースコードは、モノワイヤレス社の配布スクリプト
# https://mono-wireless.com/jp/products/TWE-APPS/App_Twelite/python_twelite/index.html
# を改変したものです。
#
# - Python3系で実行してください。Python2系では動きません。
# - 事前に下記のコマンドで、関連モジュールをインストールしておいてください。
#  > pip install pyserial # シリアル通信用ライブラリ
#  > pip install requests # HTTP通信用ライブラリ
#

from serial import *
from sys import stdout, stdin, stderr, exit
from datetime import datetime
import configparser
import threading
import requests
import codecs
import traceback


# global 変数の定義
t1 = None  # 読み出しスレッド
bTerm = False # 終了フラグ

#iniファイルの読み込み
config = configparser.ConfigParser() 
config.read('./monostick_to_influxdb.ini') # パラメータ読み出し

# 受信データのHTTP送信
def sendHTTPRequest(dict):
    url = config['influxdb']['url'] + ':' + config['influxdb']['port'] + '/write'
    payload = {'db': config['influxdb']['db_name']} # データベース名

    # {'rc': '80000000', 'lq': '153', 'ct': '0001', 'ed': '8102E86A', 'id': '0', 'ba': '2740', 'bt': '0001'}
    tag_keys = 'logical_device_id=' + dict.get('id') + ',serial_id=' + dict.get('ed') # 索引付き列
    field_keys = 'LQI=' + dict.get('lq') + ',mV=' + dict.get('ba') + ',is_open=' + str(0 if dict.get('bt') == '0001' else 1) # 索引なし列
    data = config['influxdb']['measurement_name'] + ',' + tag_keys + ' ' + field_keys # クエリ用文字列

    print('curl -i -XPOST \''+ url + '?db=' + config['influxdb']['db_name'] + '\' --data-binary \'' + data +'\'')
    response = requests.post(url=url, params=payload, data=data) # HTTP送信
    
    print ("  HTTP post request for influxDB:")
    print ("    " + response.url + " --data-binary" +  data)
    print ("  HTTP status code:", response.status_code, ("(succeeded)" if response.status_code == 204 else "failed"))
    print ("  " + response.text) # エラーメッセージを表示

# バイナリデータを辞書型データに変換
def toDictionary(binary_line):
    string_line = binary_line[1:].decode("ascii") # bytes -> str 変換
    array_line = string_line.split(':')
    dictionary = {}
    for str in array_line:
        pair = str.split('=')
        if len(pair) == 2:
           dictionary[pair[0]] = pair[1]
    return dictionary

# 想定外の受信データの表示 (そのまま出力)
def printPayload(l):
    if len(l) < 3: return False # データサイズのチェック
    
    print (" command = 0x%02x (other)" % l[1])
    print ("  src     = 0x%02x" % l[0])
    
    # ペイロードをそのまま出力する
    print ("  payload =",)
    for c in l[2:]:
        print ("%02x" % c,)
    print ("(hex)")
    return True

# LQI値(電波通信品質) 50未満(悪い -80dbm 未満)、50～100(やや悪い)、100～150(良好)、150以上(アンテナの近傍)
def evaluateLQI(lqi):
    if lqi < 50:
        str = "bad"
    elif lqi < 100:
        str = "not good"
    elif lqi < 150:
        str = "good"
    else:
        str = "very good"
    return str

# 受信データの表示、TWELITE標準アプリ版
def printPayload_default_app(l):
    if len(l) != 23: return False # データサイズのチェック
    
    print ("  source device logical id          : 0x%02x (%d in decimal)" % (l[0], l[0])) # 送信元の論理デバイスID
    print ("  packet id (generated from app id) : 0x%02x (%d in decimal)" % (l[2], l[2])) # パケット識別子 (アプリケーションIDより生成される)
    ladr = l[5] << 24 | l[6] << 16 | l[7] << 8 | l[8] # 送信元の個体識別番号
    print ("  source device physical id         : 0x%08x (%d in decimal)" % (ladr, ladr))
    print ("  Link Quality Indicator (LQI)      : %d (%s) / %.2f [dbm]" % (l[4], evaluateLQI(l[4]), (7*l[4]-1970)/20.)) # LQI値(電波通信品質)
    print ("  source voltage value              : %04d [mV]" % (l[13] << 8 | l[14])) # 電源電圧
    
    # print ("  command                           : 0x%02x (IO data arrival)" % l[1]) # コマンド(0x81: IO状態の通知)
    # print ("  destination device logical id     : 0x%02x" % l[9]) # 宛先の論理デバイスID(未指定の場合は0)
    # print ("  protocol version                  : 0x%02x" % l[3]) #プロトコルバージョン  (0x01 固定)
    # print ("  relay flag                        : %d" % l[12]) # 中継フラグ(中継回数0~3)
    # ts = l[10] << 8 | l[11]
    # print ("  timestamp (sec 64 cound )         : %.3f [s]" % (ts / 64.0)) # タイムスタンプ (秒64カウント)
    
    # DI1 のデータ
    di1 = 0 if (l[16] & 0x1) == 0 else 1 # DI1の現在の状態
    di1_on_off = "on" if di1 == 1 else "off"
    di1_chg = 0 if (l[17] & 0x1) == 0 else 1 # DI1の変更状態。一度でもLo(1)になったら1
    di1_chg_on_off = "on" if di1 == 1 else "off"
    
    print ("  digital input 1                   : %d (%s)" % (di1, di1_on_off))
    print ("  digital input 1 change status     : %d (%s)" % (di1_chg, di1_chg_on_off))
    print () # 改行
    
    return True

# 受信データを１行ずつ解釈するスレッド
def readThread():
    global ser, bTerm
    while True:
        if bTerm: return # 終了処理
        binary_line = ser.readline().rstrip() # 1行単位で読み出し(データ受信まで待機)、末尾の改行コードを削除
        if len(binary_line) > 0 and chr(binary_line[0]) == ':':
            dict = toDictionary(binary_line) # データを連想配列に変換
            if 'ts' in dict: # タイムスタンプは無視
                continue
            print (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            print ("  row binary data                   : %s" % binary_line)
        else : # 想定外のデータ受信は無視
            continue
        try:
            sendHTTPRequest(dict) # HTTP送信
        except:
            if len(line) > 0: # エラー時
                print ("Unexpected error:", traceback.print_exc())
                print ("    received data: %s" % line)

# 終了処理
def DoTerminate():
    global t1, bTerm

    # スレッドの停止
    bTerm = True
    
    print ("... quitting")
    time.sleep(0.5) # スリープでスレッドの終了待ちをする
        
    exit(0)

# 主処理
if __name__=='__main__':
    # パラメータの確認
    #   第一引数: シリアルポート名
    #if len(sys.argv) != 2:
    #    print ("Error: Please specify the serial port name for the argument. \n")
    #    print ("Example:")
    #    print ("  python", sys.argv[0], "{serial port name}")
    #    exit(1)

    #   第一引数: シリアルポート名の場合
    if len(sys.argv) == 2:
        serial_port = sys.argv[1]
    else :
        serial_port = config['serial']['port'] # iniファイルのシリアルポート
    
    # シリアルポートを開く
    try:
        ser = Serial(serial_port, 115200, timeout=0.1)
        print ("open serial port: %s" % serial_port)
        print ("waiting sensor data to receive ...\n")
    except:
        print ("cannot open serial port: %s" % serial_port)
        exit(1)
        
    # 読み出しスレッドの開始
    t1=threading.Thread(target=readThread)
    t1.setDaemon(True)
    t1.start()
    
    # 標準入力(stdin)処理
    while True:
        try:
            l = stdin.readline().rstrip()
            if len(l) > 0:
                if l[0] == 'q': # q を入力すると終了
                    DoTerminate()
                    
                if l[0] == ':': # :からの系列はそのままコマンドの送信
                    cmd = l + "\r\n"
                    print ("--> "+ l)
                    ser.write(cmd)
        except KeyboardInterrupt: # Ctrl+C
            DoTerminate()
        except SystemExit:
            exit(0)
        except:
            # 例外発生時には終了
            print ("... unknown exception detected")
            break
    exit(0)

