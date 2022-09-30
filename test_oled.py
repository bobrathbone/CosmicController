#!/usr/bin/env python3
# Raspberry Pi IQAudio Cosmic Controller Development Templates
# See IQAudio website at  http://iqaudio.co.uk
#
# Raspberry Pi OLED 128x64 test program
# This class drives the SDolomon Systech SSD1306 128 by 64 pixel OLED
#
# $Id: test_oled.py,v 1.8 2022/09/28 18:29:54 bob Exp $
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#	   The authors shall not be liable for any loss or damage however caused.
#
# Adapted from hello world program from Olimex Limited, www.olimex.com
# See https://github.com/SelfDestroyer/pyMOD-OLED.git
# 
# Line addresses
# 	 1 2  3  4  5  
Lines = [0,16,32,48,56]

from oled_class import Oled
import time,datetime
from time import strftime
import sys
import pdb

def no_interrupt():
	return False

# Class test routine
if __name__ == "__main__":
	dateformat = "%H:%M %d%m"
	mesg = "IQAudio abcdefghijklmonopqrstuvwxyz 123456789 ABCDE"

	try:
		#pdb.set_trace()
		oled = Oled()
		oled.clear()

		# Change False to True to flip display
		oled.flip_display_vertically(True)

		# Draw splash
		oled.drawSplash("bitmaps/raspberry-pi-logo.bmp",2)

		oled.setFont(2)
		sDate = strftime(dateformat)
		oled.out(1,sDate,no_interrupt)
		oled.setFont(1)
		oled.out(3,"abcdefghijklmonopqrstuvwxyz",no_interrupt)
		oled.out(4,mesg,no_interrupt)
		oled.setFont(3)
		oled.out(5,"Hello",no_interrupt)
		oled.drawHorizontalSlider(50,8)
		oled.update()

	except KeyboardInterrupt:
		print("\nExit")
		sys.exit(0)

# End of test code
# set tabstop=4 shiftwidth=4 expandtab
# retab

