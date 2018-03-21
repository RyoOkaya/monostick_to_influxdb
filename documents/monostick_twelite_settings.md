# monostickの設定

## monostickへのコンソール接続
- Teratermの事前設定
	- シリアルポート設定のボーレートを115200bpsに設定する
	-Teratermのメニューバー > 設定 > シリアルポート > ボーレート を115200に変更
	- パリティ なし, データビット 8bit, ストップビット 1bit, フロー制御 なし
- TeratermからMonostickに接続
	- MonostickをPCにUSB接続する
	- 接続したUSBデバイスに向けてTeratermでシリアルポート接続する。
	- 「+」を3回押してTeratermのコンソール上に下記のような画面が表示されれば成功
<pre>
--- CONFIG/MONO WIRELESS TWELITE DIP APP V1-08-1/SID=0x8102e183/LID=0x78 ---
 a: set Application ID (0x67720102)
 i: set Device ID (--)
 c: set Channels (18)
 x: set Tx Power (03)
 t: set mode4 sleep dur (1000ms)
 y: set mode7 sleep dur (10s)
 f: set mode3 fps (32)
 z: set PWM HZ (1000,1000,1000,1000)
 o: set Option Bits (0x00000000)
 b: set UART baud (38400)
 p: set UART parity (N)
---
 S: save Configuration
 R: reset to Defaults
 </pre>


## Monostickの設定
- 今回は、下記のパラメータを変更する
	- a: アプリケーションID
		デバイスのグループを識別するID。同一のアプリケーションIDを持つTWELITE機器のみ通信可能
		0x00010001 ～ 0x7FFFFFFEの値を任意に設定可能。
	- f: TWELITEモード7のスリープ時間(待機時間)を設定
- 設定項目の詳細については、公式マニュアルを参照
	-monowireless インタラクティブモード
	https://mono-wireless.com/jp/products/TWE-APPS/App_Twelite/interactive.html

### 設定変更手順
- アプリケーションIDの設定
	- 例えば、0x1FFAA000に設定する場合。
<pre>
 a: set Application ID (0x67720102)
↓
 a: set Application ID (0x1ffaa000)
</pre>
- 送信間隔の設定
	- 電波の送信間隔を10秒から60秒(1分)に変更
<pre>
 y: set mode7 sleep dur (10s)
↓
 y: set mode7 sleep dur (60s)
</pre>

- 設定変更
	- 「S」を押して設定を反映する

# TWELITEの設定


## TWELITEへのコンソール接続

- TWEWriterとマイクロUSBケーブルが必要
- TWEWriterにTWELITEをはめ込む(※向きに注意！逆向きに接続すると、電流がショートして高熱になり壊れます)
- 以降はmonostickの設定手順と同じ

