# monostick�̐ݒ�

## monostick�ւ̃R���\�[���ڑ�
- Teraterm�̎��O�ݒ�
	- �V���A���|�[�g�ݒ�̃{�[���[�g��115200bps�ɐݒ肷��
	-Teraterm�̃��j���[�o�[ > �ݒ� > �V���A���|�[�g > �{�[���[�g ��115200�ɕύX
	- �p���e�B �Ȃ�, �f�[�^�r�b�g 8bit, �X�g�b�v�r�b�g 1bit, �t���[���� �Ȃ�
- Teraterm����Monostick�ɐڑ�
	- Monostick��PC��USB�ڑ�����
	- �ڑ�����USB�f�o�C�X�Ɍ�����Teraterm�ŃV���A���|�[�g�ڑ�����B
	- �u+�v��3�񉟂���Teraterm�̃R���\�[����ɉ��L�̂悤�ȉ�ʂ��\�������ΐ���
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


## Monostick�̐ݒ�
- ����́A���L�̃p�����[�^��ύX����
	- a: �A�v���P�[�V����ID
		�f�o�C�X�̃O���[�v�����ʂ���ID�B����̃A�v���P�[�V����ID������TWELITE�@��̂ݒʐM�\
		0x00010001 �` 0x7FFFFFFE�̒l��C�ӂɐݒ�\�B
	- f: TWELITE���[�h7�̃X���[�v����(�ҋ@����)��ݒ�
- �ݒ荀�ڂ̏ڍׂɂ��ẮA�����}�j���A�����Q��
	-monowireless �C���^���N�e�B�u���[�h
	https://mono-wireless.com/jp/products/TWE-APPS/App_Twelite/interactive.html

### �ݒ�ύX�菇
- �A�v���P�[�V����ID�̐ݒ�
	- �Ⴆ�΁A0x1FFAA000�ɐݒ肷��ꍇ�B
<pre>
 a: set Application ID (0x67720102)
��
 a: set Application ID (0x1ffaa000)
</pre>
- ���M�Ԋu�̐ݒ�
	- �d�g�̑��M�Ԋu��10�b����60�b(1��)�ɕύX
<pre>
 y: set mode7 sleep dur (10s)
��
 y: set mode7 sleep dur (60s)
</pre>

- �ݒ�ύX
	- �uS�v�������Đݒ�𔽉f����

# TWELITE�̐ݒ�


## TWELITE�ւ̃R���\�[���ڑ�

- TWEWriter�ƃ}�C�N��USB�P�[�u�����K�v
- TWEWriter��TWELITE���͂ߍ���(�������ɒ��ӁI�t�����ɐڑ�����ƁA�d�����V���[�g���č��M�ɂȂ���܂�)
- �ȍ~��monostick�̐ݒ�菇�Ɠ���

