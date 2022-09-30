#!/usr/bin/env python3
#
# Raspberry Pi IR remote control class
# $Id: ir_remote_class.py,v 1.7 2022/09/28 16:06:57 bob Exp $
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# This program uses LIRC (Linux Infra Red Control) and python-lirc
# For Raspbian Jessie run:
#       apt-get install lirc python-lirc
#
# For Raspbian Stretch run:
#       wget https://github.com/tompreston/python-lirc/releases/download/v1.2.1/python-lirc_1.2.1-1_armhf.deb
#       sudo dpkg -i python-lirc_1.2.1-1_armhf.deb
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#	   The authors shall not be liable for any loss or damage however caused.
#
# The important configuration files are
#       /etc/lirc/lircrc Program to event registration file
#       /etc/lircd.conf  User generated remote control configuration file
#

import os,sys
import time
import lirc
import socket
import RPi.GPIO as GPIO
from config_class import Configuration

lircrc = '/etc/lirc/lircrc'

config = Configuration()

# IR remote control class
class IRRemote:
	remote_led = 0	# Activity LED

	def __init__(self,callback):
		self.callback = callback
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		self.remote_led = config.getIrActivityLed()

	# The main Remote control listener routine
	def listen(self):
		if self.remote_led > 0:
			GPIO.setup(self.remote_led, GPIO.OUT)
		try:
			socket_name = config.getSocketName()
			sockid = lirc.init(socket_name, lircrc)
			print("Listener on socket " + str(socket) + " established")

			#Listen loop
			while True:
				nextcode =  lirc.nextcode()
				if len(nextcode) > 0:
					if self.remote_led > 0:
						GPIO.output(self.remote_led, True)
					button = nextcode[0]
					self.callback(button)
					if self.remote_led > 0:
						time.sleep(0.1)
						GPIO.output(self.remote_led, False)

		except Exception as e:
			print(str(e))
			mesg = "Possible configuration error, check /etc/lirc/lircd.conf"
			print(mesg)
			mesg = "Activation IR Remote Control failed - Exiting"
			print(mesg)
			sys.exit(1)

	# Get activity led GPIO
	def getActivityLed(self):
		return self.remote_led

# End of IR class
# set tabstop=4 shiftwidth=4 expandtab
# retab
