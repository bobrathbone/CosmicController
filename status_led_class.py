#!/usr/bin/env python3
# Raspberry Pi IQAudio Cosmic Controller Development Templates
# See IQAudio website at  http://iqaudio.co.uk
#
# $Id: status_led_class.py,v 1.6 2022/09/28 08:24:24 bob Exp $
# IQAudio Cosmic Controller LED
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#

import RPi.GPIO as GPIO
import time


# Status LED class
class StatusLed:
    led1 = None
    led3 = None
    led2 = None

    LED1 = 1
    LED2 = 2
    LED3 = 3

    # The init routine uses default GPIO settings
    #def __init__(self, led1=23, led2=27, led3=22 ):
    def __init__(self, led1=16, led2=15, led3=14 ):
        self.led1 = led1
        self.led2 = led2
        self.led3 = led3

        # Set up status LEDS
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        if self.led1 > 0:
            GPIO.setup(self.led1, GPIO.OUT)
        if self.led2 > 0:
            GPIO.setup(self.led2, GPIO.OUT)
        if self.led3 > 0:
            GPIO.setup(self.led3, GPIO.OUT)
            return

    # Set the status to normal, busy, error or clear
    def set(self,led,onoff):
        # onoff is True or False
        if led == self.LED1:
            GPIO.output(self.led1, onoff)
        elif led == self.LED2:
            GPIO.output(self.led2, onoff)
        elif led == self.LED3:
            GPIO.output(self.led3, onoff)
        return 

    # Switch all LEDs off
    def clear(self):
        GPIO.output(self.led1, False)
        GPIO.output(self.led2, False)
        GPIO.output(self.led3, False)
        return 

    # Get LED configurations
    def getLED1(self):
        return self.led1

    def getLED2(self):
        return self.led2

    def getLED3(self):
        return self.led3

# End of class

if __name__ == "__main__":
    statusLed = StatusLed()
    statusLed.clear()
    time.sleep(1)
    statusLed.set(StatusLed.LED1,True)
    print("LED 1 GPIO",statusLed.getLED1())
    time.sleep(2)
    statusLed.set(StatusLed.LED1,False)
    statusLed.set(StatusLed.LED2,True)
    print("LED 2 GPIO",statusLed.getLED2())
    time.sleep(2)
    statusLed.set(StatusLed.LED2,False)
    statusLed.set(StatusLed.LED3,True)
    print("LED 3 GPIO",statusLed.getLED3())
    time.sleep(2)
    statusLed.clear()
    time.sleep(2)
    statusLed.set(StatusLed.LED1,True)
    statusLed.set(StatusLed.LED2,True)
    statusLed.set(StatusLed.LED3,True)
    print("All LEDs on")
    time.sleep(2)
    statusLed.clear()
    print("All LEDs off")

# set tabstop=4 shiftwidth=4 expandtab
# retab

