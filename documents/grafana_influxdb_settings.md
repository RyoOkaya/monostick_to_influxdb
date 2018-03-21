# 事前想定

- 環境はパブリッククラウド(AWS, GCP, Azurenなど)のVMで構築
- VMのOSはUbuntu

# InfluxDBの設定

## インストール

マニュアルに書いてある通りでよい。
https://docs.influxdata.com/influxdb/v1.3/introduction/installation/

> sudo service influxdb start
> sudo service influxdb status

で、起動していればOK.


## 初期DB作成

influxdbにローカルからログイン
> influx -precision rfc3339

センサデータ保持用のDB作成
> CREATE DATABASE door_sensor


## ポート開放

クラウド側の設定で、クライアントからVMへの
HTTP(80番)とInfluxDB(8086番)用のポートを空ける。


## 通信確認

クライアントからinfluxDBにデータを飛ばして、
influxDB側からデータが確認できれば完了。

> influx -precision rfc3339
> USE door_sensor 
> show measurements
> select * from meeting_rooms;


# Grafanaの設定


## インストール

マニュアルの手順通りでよい。
http://docs.grafana.org/installation/


## 設定変更

パラメータファイルを適当にいじる。
/etc/grafana/grafana.ini

### ポート変更方法

- 方法1. /etc/grafana/grafana.iniを変更する
	- ;http_port = 3000 を、 http_port = 80 に変更する。
	- うまくいかなかった
- 方法2. ポートフォワーディング
	- 下記のようにして80番向けの通信を3000番にフォワードする。
> sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 3000
- 確認方法
	- URLのポート3000番(80番に設定した場合は80番)にアクセスする

## サーバ起動
> sudo service grafana-server start

