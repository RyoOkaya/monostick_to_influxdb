# monostick_to_influxdb.py
TWELITE �����f�[�^��HTTP���M�X�N���v�g

## �v���O�����T�v
TWELITE�̃f�[�^��influxDB�T�[�o�Ƀ����[�g�ʐM����python�X�N���v�g

## �p��T��
- TWELITE
���m���C�����X�Ђ̖����}�C�R�����W���[��
- MONOSTICK
TWELITE��PC���ɐڑ�����USB�[�q�������m���C�����X�Ђ̐��i�B

- InfluxDB
���n��f�[�^�x�[�X
- TWELITE DIP  
https://mono-wireless.com/jp/products/TWE-Lite-DIP/index.html
- MONOSTICK  
https://mono-wireless.com/jp/products/MoNoStick/index.html


### �z��\���}

![�\���}](https://github.com/RyoOkaya/monostick_to_influxdb/blob/master/architechture.png)


## �v���O�������s���@
�{�X�N���v�g�́A���L�̃��m���C�����X�Ђ̔z�z�X�N���v�g�����ɂ��č쐬�B
https://mono-wireless.com/jp/products/TWE-APPS/App_Twelite/python_twelite/index.html

### ���s�v��
- Python3�n�̂ݑΉ��BPython2�n�ɂ͔�Ή��B
- ���L�̃R�}���h�ŁA�֘A���W���[�����C���X�g�[�����Ă���
`pip install pyserial # �V���A���ʐM�p���C�u����`  
`pip install requests # HTTP�ʐM�p���C�u����`  
�� ���s�ɂ�OS�̊Ǘ��Ҍ������K�v  

### ���s���@
- python�R�}���h���Ŏ��s����
`python monostick_to_influxdb.py [Device Name]`  
- ���s��(Windows�̏ꍇ):  
`python monostick_to_influxdb.py COM4`

[�o�͗�]

<pre>
open serial port: COM3
waiting sensor data to receive ...

- TWELITE
���m���C�����X�Ђ̖����}�C�R�����W���[��
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

### ��~���@

Ctrl + C �ȂǂŒ�~�ł��܂��B

### �ݒ�t�@�C��
monostick_to_influxdb.ini�t�@�C���ŁA���L�̃p�����[�^��ݒ�ł��܂��B
- �f�t�H���g�̃f�o�C�X��
- influxDB��URL
- influxDB�̃|�[�g�ԍ�
- influxDB�̃f�[�^�x�[�X��
- influxDB�̃��W�������g��(�e�[�u����)


### ���O����

- TWELITE DIP  
https://mono-wireless.com/jp/products/TWE-Lite-DIP/index.html
- MONOSTICK  
https://mono-wireless.com/jp/products/MoNoStick/index.html
- InflaxDB�T�[�o



