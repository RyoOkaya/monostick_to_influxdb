# monostick_to_influxdb
TWELITE 無線データのHTTP送信スクリプト

## プログラム概要
モノワイヤレス社の無線マイコンモジュールTWELITEから取得したデータを、
リモートのinfluxDBサーバにHTTPで送信するスクリプトです。
このスクリプトは、MONOSTICKを無線データの受信機として取り付けたOS上で実行することを想定しています。

- TWELITE DIP  
https://mono-wireless.com/jp/products/TWE-Lite-DIP/index.html
- MONOSTICK  
https://mono-wireless.com/jp/products/MoNoStick/index.html



### 想定構成図

[画像]


## プログラム実行方法
本スクリプトは、下記のモノワイヤレス社の配布スクリプトを改変して作成しました。  
https://mono-wireless.com/jp/products/TWE-APPS/App_Twelite/python_twelite/index.html

### 注意事項
- Python3系で実行してください。Python2系では動きません。
- 下記のコマンドで、関連モジュールをインストールします  
`pip install pyserial # シリアル通信用ライブラリ`  
`pip install requests # HTTP通信用ライブラリ`  
※OSの管理者権限が必要  

### 実行方法
pythonスクリプトを実行します。  
`python monostick_to_influxdb.py [Device Name]`  
例(Windowsの場合):  
`python monostick_to_influxdb.py COM4`

[出力例]

### Settings
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



