# monostick_to_influxdb.py
TWELITE 無線データのHTTP送信スクリプト

## プログラム概要
TWELITEのデータをinfluxDBサーバにリモート通信するpythonスクリプト

## 用語概説
- TWELITE
モノワイヤレス社の無線マイコンモジュール
- MONOSTICK
TWELITEをPC等に接続するUSB端子を持つモノワイヤレス社の製品。

- InfluxDB
時系列データベース
- TWELITE DIP  
https://mono-wireless.com/jp/products/TWE-Lite-DIP/index.html
- MONOSTICK  
https://mono-wireless.com/jp/products/MoNoStick/index.html


### 想定構成図

![構成図](https://github.com/RyoOkaya/monostick_to_influxdb/blob/master/architechture.png)


## プログラム実行方法
本スクリプトは、下記のモノワイヤレス社の配布スクリプトを元にして作成。
https://mono-wireless.com/jp/products/TWE-APPS/App_Twelite/python_twelite/index.html

### 実行要件
- Python3系のみ対応。Python2系には非対応。
- 下記のコマンドで、関連モジュールをインストールしておく
`pip install pyserial # シリアル通信用ライブラリ`  
`pip install requests # HTTP通信用ライブラリ`  
※ 実行にはOSの管理者権限が必要  

### 実行方法
- pythonコマンド等で実行する
`python monostick_to_influxdb.py [Device Name]`  
- 実行例(Windowsの場合):  
`python monostick_to_influxdb.py COM4`

[出力例]

<pre>
open serial port: COM3
waiting sensor data to receive ...

- TWELITE
モノワイヤレス社の無線マイコンモジュール
2018/03/21 15:58:36
  row binary data                   : b':7F8115019F810E2A54000002000B431D00004B293A10F320'
  source device logical id          : 0x7f (127 in decimal)
  packet id (generated from app id) : 0x15 (21 in decimal)
  source device physical id         : 0x810e2a54 (2165189204 in decimal)
  Link Quality Indicator (LQI)      : 159 (very good) / -42.85 [dbm]
  source voltage value              : 2883 [mV]
  digital input 1                   : 0 (off)
  digital input 1 change status     : 0 (off)

curl -i -XPOST 'http://xxx.xxx.xxx.xxx:8086/write?db=door_sensor' --data-binary 'meeting_rooms,logical_device_id=127,packet_id=21,physical_device_id=xxxxxxxxxx LQI=159,mV=2883,open=0,relay_count=0'
  HTTP post request for influxDB:
    http://xxx.xxx.xxx.xxx:8086/write?db=door_sensor --data-binarymeeting_rooms,logical_device_id=127,packet_id=21,physical_device_id=xxxxxxxxxx LQI=159,mV=2883,open=0,relay_count=0
  HTTP status code: 204 (succeeded)
</pre>

### 停止方法

Ctrl + C などで停止できます。

### 設定ファイル
monostick_to_influxdb.iniファイルで、下記のパラメータを設定できます。
- デフォルトのデバイス名
- influxDBのURL
- influxDBのポート番号
- influxDBのデータベース名
- influxDBのメジャメント名(テーブル名)


### 事前準備

- TWELITE DIP  
https://mono-wireless.com/jp/products/TWE-Lite-DIP/index.html
- MONOSTICK  
https://mono-wireless.com/jp/products/MoNoStick/index.html
- InflaxDBサーバ



