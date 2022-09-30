#!/usr/bin/env python3
# Raspberry Pi IQAudio Cosmic Controller Configuration Class
# $Id: config_class.py,v 1.7 2022/09/28 19:05:51 bob Exp $
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# This class the configuration parameters for the IQAudio Cosmic controller
# You should not normally need to amend this file unless you are using the 15 pin SIL header
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#            The authors shall not be liable for any loss or damage however caused.
#
class Configuration:

	# The configuration left to right
	_left_switch = 6
	_middle_switch = 5
	_right_switch = 4

	# Rotary encoder
	_encoder_switch = 27
	_encoder_a = 23
	_encoder_b = 24

	# Status LEDs
	_led1 = 14
	_led2 = 15
	_led3 = 16

	_ir_activity_led = _led3 

	# lirc socket name (Must match name in lircd.conf and lircc)
	_lirc_socket_name = 'cosmicd' 

	def __init__(self):
		return

	# Getters
	def getLeftSwitch(self):
		return int(self._left_switch)

	def getMiddleSwitch(self):
		return self._middle_switch

	def getRightSwitch(self):
		return self._right_switch

	def getEncoderSwitch(self):
		return self._encoder_switch

	def getEncoderA(self):
		return self._encoder_a

	def getEncoderB(self):
		return self._encoder_b

	def getLed1(self):
		return self._led1

	def getLed2(self):
		return self._led2

	def getLed3(self):
		return self._led3

	def getIrActivityLed(self):
		return self._ir_activity_led

	def getSocketName(self):
	 	return self._lirc_socket_name

# End of configuration class
# set tabstop=4 shiftwidth=4 expandtab
# retab
