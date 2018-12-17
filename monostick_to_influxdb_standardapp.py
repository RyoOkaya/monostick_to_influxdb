#!/usr/bin/python
# coding: UTF-8

### TWELITE標準アプリ版 無線データのHTTP送信スクリプト
# 本ソースコードは、モノワイヤレス社の配布スクリプト
# https://mono-wireless.com/jp/products/TWE-APPS/App_Twelite/python_twelite/index.html
# を改変したものです。
#
# - Python 3系で実行してください。Python 2系のバージョンでは動作しません。
#   This script requires Python3 or later version.
# - 事前に下記のコマンドで、関連モジュールをインストールしておいてください。
#   To run this script, the python libraries below are required.
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
config.read('./monostick_to_influxdb.ini') # Reading parameters form .ini file

# InfluxdbへのHTTP送信
def sendHTTPRequest(dict):
    # Setting query strings
    url = '{url}:{port}/write?u={user}&p={password}'.format(url=config["influxdb"]["url"],port=config["influxdb"]["port"],user=config["influxdb"]["basic_auth_user"],password=config["influxdb"]["basic_auth_password"]) # URL
    payload = {'db': config["influxdb"]["db_name"]} # database name
    tag_keys = 'logical_device_id={logical_id},packet_id={packet_id},physical_device_id={physical_id}'.format(logical_id=dict.get("logical_id"),packet_id=dict.get("packet_id"),physical_id=dict.get("physical_id"))  # columns with index
    field_keys = 'LQI={LQI},mV={mV},is_closed={di1}'.format(LQI=dict.get("LQI"),mV=dict.get("mV"),di1=dict.get("di1")) # columns without index
    query = '{measurement_name},{tag_keys} {field_keys}'.format(measurement_name=config["influxdb"]["measurement_name"],tag_keys=tag_keys,field_keys=field_keys) # query string
    print('curl -i -XPOST \'{url}?db={db_name}\' --data-binary \'{data}\''.format(url=url,db_name=config["influxdb"]["db_name"],data=query)) # print in the form of curl command

    ### for python3.6 or later
    # url = f'{config["influxdb"]["url"]}:{config["influxdb"]["port"]}/write?u={config["influxdb"]["basic_auth_user"]}&p={config["influxdb"]["basic_auth_password"]}' # URL
    # tag_keys = f'logical_device_id={dict.get("logical_id")},packet_id={dict.get("packet_id")},physical_device_id={dict.get("physical_id")}' # columns with index
    # field_keys = f'LQI={dict.get("LQI")},mV={dict.get("mV")},is_closed={dict.get("di1")}' # columns without index
    # query = f'{config["influxdb"]["measurement_name"]},{tag_keys} {field_keys}' # query string
    # print(f'curl -i -XPOST \'{url}?db={config["influxdb"]["db_name"]}\' --data-binary \'{query}\'') # print in the form of curl command

    response = requests.post(url=url, params=payload, data=query) # send HTTP request to influxdb

    print ("  HTTP post request for influxDB:")
    print ("    " + response.url + " --data-binary " +  query)
    print ("  HTTP status code:", response.status_code, ("(succeeded)" if response.status_code == 204 else "failed"))
    print ("  " + response.text) # エラーメッセージを表示

# バイト列データを辞書型データに変換
def toDictionary(byte):
    dict = {} # センサデータ
    dict["logical_id"] = byte[0] # 送信元の論理デバイスID
    dict["command"] = byte[1]  # 0x81ならIO関連のデータの受信
    dict["packet_id"] = byte[2] # パケット識別子 (アプリケーションIDより生成される)
    dict["protocol_version"] = byte[3]  #プロトコルバージョン  (0x01 固定)
    dict["LQI"] = byte[4] # LQI値(電波通信品質)
    dict["physical_id"] = (byte[5] << 24 | byte[6] << 16 | byte[7] << 8 | byte[8])  # 送信元の個体識別番号
    dict["logical_id_to"] = byte[9]  # 宛先の論理デバイスID(未指定の場合は0)
    dict["timestamp"] = byte[10] << 8 | byte[11] # タイムスタンプ (秒64カウント)
    dict["relay_count"] = byte[12] # 中継フラグ(中継回数0~3)
    dict["mV"] = (byte[13] << 8 | byte[14]) # 電源電圧
    dict["di1"] = (0 if (byte[16] & 0x1) == 0 else 1)  # DI1の現在の状態
    dict["di1cs"] = (0 if (byte[17] & 0x1) == 0 else 1)  # DI1の変更状態。一度でもLo(1)になったら1
    return dict

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

# 受信データの出力
def printPayload(dict):
    print ("  source device logical id          : 0x%02x (%d in decimal)" % (dict.get("logical_id"), dict.get("logical_id"))) # 送信元の論理デバイスID
    print ("  packet id (generated from app id) : 0x%02x (%d in decimal)" % (dict.get("packet_id"), dict.get("packet_id"))) # パケット識別子 (アプリケーションIDより生成される)
    print ("  source device physical id         : 0x%08x (%d in decimal)" % (dict.get("physical_id"), dict.get("physical_id"))) # 送信元の個体識別番号
    print ("  Link Quality Indicator (LQI)      : %d (%s) / %.2f [dbm]" % (dict.get("LQI"), evaluateLQI(dict.get("LQI")), (7*dict.get("LQI")-1970)/20.)) # LQI値(電波通信品質)
    print ("  source voltage value              : %04d [mV]" % dict.get("mV")) # 電源電圧
    # print ("  command                           : 0x%02x (IO data arrival)" % dict.get("command")) # コマンド(0x81: IO状態の通知)
    # print ("  destination device logical id     : 0x%02x" % dict.get("logical_id_to")) # 宛先の論理デバイスID(未指定の場合は0)
    # print ("  protocol version                  : 0x%02x" % dict.get("protocol_version")) #プロトコルバージョン  (0x01 固定)
    # print ("  relay count                        : %d" % dict.get("relay_count")) # 中継フラグ(中継回数0~3)
    # print ("  timestamp (sec 64 cound )         : %.3f [s]" % (dict.get("timestamp") / 64.0)) # タイムスタンプ (秒64カウント)

    # DI1 のデータ
    di1 = dict.get("di1") # DI1の現在の状態
    di1_status = "on" if di1 == 1 else "off"
    di1_chg = dict.get("di1cs") # DI1の変更状態。一度でもLo(1)になったら1
    di1_chg_status = "on" if di1 == 1 else "off"

    print ("  digital input 1                   : %d (%s)" % (di1, di1_status))
    print ("  digital input 1 change status     : %d (%s)" % (di1_chg, di1_chg_status))
    print () # 改行

    return True

# 受信データを１行ずつ解釈するスレッド
def readThread():
    global ser, bTerm
    while True:
        if bTerm: return # 終了処理
        binary_line = ser.readline().rstrip() # 1行単位で読み出し(データ受信まで待機)、末尾の改行コードを削除
        if len(binary_line) > 0 and chr(binary_line[0]) == ':':
            print (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            print ("  row binary data                   : %s" % binary_line)
        else : # 想定外のデータ受信は無視
            continue
        try:
            string_line = binary_line[1:].decode("ascii") # bytes -> str 変換
            import codecs
            byte = codecs.decode(string_line, "hex_codec") # hex_codec でバイト列に変換 (bytes)
            csum = sum(byte) & 0xff  # チェックサム 8bit計算で全部足して　0x00 なら OK
            byte = byte[0:len(byte)-1] # チェックサムをリストから削除
            dict = toDictionary(byte) # データを連想配列に変換
            if csum == 0:
                printPayload(dict) # 受信データを出力
                sendHTTPRequest(dict) # HTTP送信
            else:
                print ("checksum ng")
        except:
            if len(binary_line) > 0: # エラー時
                print ("Unexpected error:", traceback.print_exc())
                print ("    received data: %s" % binary_line)

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
    #   第一引数: シリアルポート名の場合
    if len(sys.argv) == 2:
        serial_port = sys.argv[1]
    else :
        serial_port = config['serial']['port'] # iniファイルのシリアルポート名

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
