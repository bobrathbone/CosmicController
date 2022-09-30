#!/usr/bin/env python3
#
# Raspberry Pi Test IR remote control class
# $Id: test_remote.py,v 1.2 2022/09/28 16:06:57 bob Exp $
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
from ir_remote_class import IRRemote

# Callback routine
def ir_callback(button):
	print("Callback got button:", button)

# Test routine
if __name__ == "__main__":
	pid = os.getpid()
	print("Test remote control pid",pid)

	from ir_remote_class import IRRemote
	ir_remote = IRRemote(ir_callback)

	print("Activity LED on GPIO",ir_remote.getActivityLed())
	print("Press Ctl-C to exit")

	try:
		ir_remote.listen()

	except KeyboardInterrupt:
		print(" Exiting")
		sys.exit(0)

# End of test routines
# set tabstop=4 shiftwidth=4 expandtab
# retab

