# ���O�z��

- ���̓p�u���b�N�N���E�h(AWS, GCP, Azuren�Ȃ�)��VM�ō\�z
- VM��OS��Ubuntu

# InfluxDB�̐ݒ�

## �C���X�g�[��

�}�j���A���ɏ����Ă���ʂ�ł悢�B
https://docs.influxdata.com/influxdb/v1.3/introduction/installation/

> sudo service influxdb start
> sudo service influxdb status

�ŁA�N�����Ă����OK.


## ����DB�쐬

influxdb�Ƀ��[�J�����烍�O�C��
> influx -precision rfc3339

�Z���T�f�[�^�ێ��p��DB�쐬
> CREATE DATABASE door_sensor


## �|�[�g�J��

�N���E�h���̐ݒ�ŁA�N���C�A���g����VM�ւ�
HTTP(80��)��InfluxDB(8086��)�p�̃|�[�g���󂯂�B


## �ʐM�m�F

�N���C�A���g����influxDB�Ƀf�[�^���΂��āA
influxDB������f�[�^���m�F�ł���Ί����B

> influx -precision rfc3339
> USE door_sensor 
> show measurements
> select * from meeting_rooms;


# Grafana�̐ݒ�


## �C���X�g�[��

�}�j���A���̎菇�ʂ�ł悢�B
http://docs.grafana.org/installation/


## �ݒ�ύX

�p�����[�^�t�@�C����K���ɂ�����B
/etc/grafana/grafana.ini

### �|�[�g�ύX���@

- ���@1. /etc/grafana/grafana.ini��ύX����
	- ;http_port = 3000 ���A http_port = 80 �ɕύX����B
	- ���܂������Ȃ�����
- ���@2. �|�[�g�t�H���[�f�B���O
	- ���L�̂悤�ɂ���80�Ԍ����̒ʐM��3000�ԂɃt�H���[�h����B
> sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 3000
- �m�F���@
	- URL�̃|�[�g3000��(80�Ԃɐݒ肵���ꍇ��80��)�ɃA�N�Z�X����

## �T�[�o�N��
> sudo service grafana-server start

