# monostick_to_influxdb
TWELITE �����f�[�^��HTTP���M�X�N���v�g

## �v���O�����T�v
���m���C�����X�Ђ̖����}�C�R�����W���[��TWELITE����擾�����f�[�^���A
�����[�g��influxDB�T�[�o��HTTP�ő��M����X�N���v�g�ł��B
���̃X�N���v�g�́AMONOSTICK�𖳐��f�[�^�̎�M�@�Ƃ��Ď��t����OS��Ŏ��s���邱�Ƃ�z�肵�Ă��܂��B

- TWELITE DIP  
https://mono-wireless.com/jp/products/TWE-Lite-DIP/index.html
- MONOSTICK  
https://mono-wireless.com/jp/products/MoNoStick/index.html



### �z��\���}

[�摜]


## �v���O�������s���@
�{�X�N���v�g�́A���L�̃��m���C�����X�Ђ̔z�z�X�N���v�g�����ς��č쐬���܂����B  
https://mono-wireless.com/jp/products/TWE-APPS/App_Twelite/python_twelite/index.html

### ���ӎ���
- Python3�n�Ŏ��s���Ă��������BPython2�n�ł͓����܂���B
- ���L�̃R�}���h�ŁA�֘A���W���[�����C���X�g�[�����܂�  
`pip install pyserial # �V���A���ʐM�p���C�u����`  
`pip install requests # HTTP�ʐM�p���C�u����`  
��OS�̊Ǘ��Ҍ������K�v  

### ���s���@
python�X�N���v�g�����s���܂��B  
`python monostick_to_influxdb.py [Device Name]`  
��(Windows�̏ꍇ):  
`python monostick_to_influxdb.py COM4`

[�o�͗�]

### Settings
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



