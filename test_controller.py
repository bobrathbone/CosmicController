#!/usr/bin/env python3
# Raspberry Pi IQAudio Cosmic Controller Development Templates
# See IQAudio website at  http://iqaudio.co.uk
#
# Raspberry Pi Cosmic Controller (IQAudio) Class
# $Id: test_controller.py,v 1.8 2022/09/28 19:05:51 bob Exp $
#
# Author: Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# This class uses one standard rotary encoder with push switch
# and three push to make buttons. It also has three status LEDs and option IR sensor
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#            The authors shall not be liable for any loss or damage however caused.
#
#

import sys,os,pwd
import time
import pdb
#pdb.set_trace()

from rotary_class import RotaryEncoder
from status_led_class import StatusLed
from config_class import Configuration
from cosmic_class import Button

config = Configuration()

### Test routines ###
left_switch = 0
middle_switch = 0
right_switch = 0
encoder_switch = 0
encoder_a = 0
encoder_b = 0

statusLed = None
Names = ['NO_EVENT', 'CLOCKWISE', 'ANTICLOCKWISE', 'BUTTON DOWN', 'BUTTON UP']

def button_event(gpio):
        global encoder_switch,left_switch,middle_switch
        print("Button pressed on GPIO", gpio)

        statusLed.clear()
        if gpio == left_switch:
            statusLed.set(StatusLed.LED3,True)
        elif gpio == middle_switch:
            statusLed.set(StatusLed.LED2,True)
        elif gpio == right_switch:
            statusLed.set(StatusLed.LED1,True)

        return

# Test only - No event sent
def rotary_event(event):
        name = ''
        try:
            name = Names[event]
        except:
            name = 'ERROR'

        statusLed.clear()
        if event == RotaryEncoder.CLOCKWISE:
            statusLed.set(StatusLed.LED3,True)

        elif event == RotaryEncoder.ANTICLOCKWISE:
            statusLed.set(StatusLed.LED1,True)
        else:
            # Handle button up/down
            statusLed.clear()

        print("Rotary event ", event, name)
        return

# Configure status LED
def statusLedInitialise(statusLed):
    led1 = config.getLed1()
    led2 = config.getLed2()
    led3 = config.getLed3()
    statusLed = StatusLed(led1,led2,led3)
    print("statusLed",led1,led2,led3)
    return statusLed


if __name__ == "__main__":

    print("Test Cosmic Controller Class")
    print("============================")

    # Get configuration
    left_switch = config.getLeftSwitch()
    middle_switch = config.getMiddleSwitch()
    right_switch = config.getRightSwitch()
    encoder_switch = config.getEncoderSwitch()
    encoder_a = config.getEncoderA()
    encoder_b = config.getEncoderB()

    print("Left switch GPIO", left_switch)
    print("Middle switch GPIO", middle_switch)
    print("Right switch GPIO", right_switch)
    print("Encoder A GPIO", encoder_a)
    print("Encoder B GPIO", encoder_b)
    print("Encoder switch GPIO", encoder_switch)

    Button(left_switch, button_event)
    Button(middle_switch, button_event)
    Button(right_switch, button_event)

    rotaryknob = RotaryEncoder(encoder_a,encoder_b,encoder_switch,rotary_event)

    statusLed = statusLedInitialise(statusLed)
    statusLed.set(StatusLed.LED1,True)
    time.sleep(1)
    statusLed.clear()
    statusLed.set(StatusLed.LED2,True)
    time.sleep(1)
    statusLed.clear()
    statusLed.set(StatusLed.LED3,True)
    time.sleep(1)
    statusLed.clear()
    time.sleep(1)

    # Main wait loop
    try:
        while True:
            time.sleep(0.2)

    except KeyboardInterrupt:
        print(" Stopped")
        sys.exit(0)

    # End of script

# set tabstop=4 shiftwidth=4 expandtab
# retab

