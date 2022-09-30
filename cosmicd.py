#!/usr/bin/env python3 
# Raspberry Pi IQAudio Cosmic Controller Development Templates
# See IQAudio website at http://iqaudio.co.uk
#
# Raspberry Pi IQAudio Cosmic Controller daemon
#
# $Id: cosmicd.py,v 1.15 2022/09/28 19:20:48 bob Exp $
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#      The authors shall not be liable for any loss or damage however caused.
#

import os,sys
import signal
import time,datetime
from time import strftime

from rotary_class import RotaryEncoder
from status_led_class import StatusLed
from config_class import Configuration
from cosmic_class import Button

# This is the Python debugger.  
# Insert pdb.set_trace() at debug point 
import pdb

# Import for the daemon class
from daemon import Daemon

# OLED import
from oled_class import Oled

_version = '1.0'
config = Configuration()

timeformat = " %H:%M:%S"
pidfile = '/var/run/cosmicd.pid'
Run = True

# Rotary event names
Names = ['No event', 'Clockwise', 'Anticlockwise', 'Button down', 'Button up']
NO_EVENT = 0

# Signal SIGTERM handler
def signalHandler(signal,frame):
    global Run
    pid = os.getpid()
    print("signalHandler",signal)
    """
    Do cleanup here
    """
    Run = False

# No interrupt
def no_interrupt():
    return False

myText = "ABCDEFGHIJKLMNOPQRSTUVWXYZ 012345678 abcdefghijklmnopqrstuvwxyz"


# Daemon class (Called from __main__)
class MyDaemon(Daemon):
    global Run
    oled = None
    gotEvent = False
    event = 0

    left_switch = 0
    middle_switch = 0
    right_switch = 0
    encoder_switch = 0
    encoder_a = 0
    encoder_b = 0
    rotaryknob = None

    sliderPosition = -1 # Current slider position 0-100%
    sliderValue = 50    # Current slider value 0-100%

    # The following prevents unecessary display updates
    displayLines = ['','','','','','','','']

    statusLed =  StatusLed()

    def run(self):
        signal.signal(signal.SIGTERM,signalHandler)
        self.oled = Oled()
        self.oled.clear()

        # Change False to True to flip display
        self.oled.flip_display_vertically(True)

        # Draw splash
        self.oled.drawSplash("bitmaps/raspberry-pi-logo.bmp",2)

        # Configure the Cosmic controller routines 
        self.getConfiguration()
        self.statusLed = self.statusLedInitialise(self.statusLed)

        self.process()  # Call main processing loop

    # Interrupt routine for scrolling
    def interrupt(self):
        global Run
        interrupt = self.gotEvent
        self.gotEvent = False
        if not Run:
            interrupt = True
        else:
            self.displayTime()
        return interrupt

    # Main processing loop
    def process(self):
        global Run
        self.displayTime()
        self.displayText(4,"Press button", 1)

        while Run:
            self.displayTime()
            self.drawSlider(self.sliderValue,8)
            self.displayText(6,myText,1,scroll=True)

            # Check for event
            if self.interrupt:
                self.handleEvent(self.event)
            else:
                time.sleep(0.1)

        # Exit program  
        self.oled.clear(update=True)
        self.displayText(3," Bye",4)
        sys.exit(0)

        # End of main processing loop
            
    # Draw slider only if value changes
    def drawSlider(self,value,line_number):
        if value != self.sliderPosition:
            self.sliderPosition = value
            self.oled.drawHorizontalSlider(self.sliderPosition,8)
            self.oled.update()

    # Display time on line 1 only if it has changed
    def displayTime(self):
        sTime = strftime(timeformat)
        self.displayText(1,sTime,2)
        self.oled.setFont(1)

    # Display text only if it has changed on that line
    def displayText(self,line_number,text,fontSize,scroll=False):
        idx = line_number - 1
        if text != self.displayLines[idx]:
            self.oled.setFont(fontSize)
            self.oled.out(line_number,text,self.interrupt)
            self.oled.update()
            if scroll:
                self.displayLines[idx] = ''
            else:
                self.displayLines[idx] = text

    # Button event callback routine
    def button_event(self,button):
        self.event = button
        self.gotEvent = True

    # Handle event (Buttons in this case) 
    def handleEvent(self,event):
        sButton = ''
        action = 'down'
        self.statusLed.clear()

        # Determine which button was pessed
        if event == self.left_switch:
            sButton = 'Left switch'
            self.statusLed.set(self.statusLed.LED1,True)

        elif event == self.middle_switch:
            sButton = 'Middle switch'
            self.statusLed.set(self.statusLed.LED2,True)

        elif event == self.right_switch:
            sButton = 'Right switch'
            self.statusLed.set(self.statusLed.LED3,True)

        elif event == self.encoder_switch:
            self.statusLed.set(StatusLed.LED2,True)
            sButton = "Rotary button"

        elif event == self.encoder_b:
            sButton = "CLOCKWISE"
            action = 'turn'
            self.statusLed.set(StatusLed.LED3,True)
            self.sliderValue += 5
            if self.sliderValue > 100:
                self.sliderValue = 100

        elif event == self.encoder_a:
            sButton = "ANTI-CLOCKWISE"
            action = 'turn'
            self.statusLed.set(StatusLed.LED1,True)
            self.sliderValue -= 5
            if self.sliderValue < 0:
                self.sliderValue = 0

        # Display message on OLED line 4, fontsize 1
        if len (sButton) > 0:
            self.displayText(4,sButton + " " + action, 1)

        self.gotEvent = False
        self.event = NO_EVENT 

    # Rotary encoder event callback routine
    def rotary_event(self,event):
        name = ''
        try:
            name = Names[event]
        except:
            name = 'ERROR'

        self.statusLed.clear()
        if event == RotaryEncoder.CLOCKWISE:
            self.event = self.encoder_b

        elif event == RotaryEncoder.ANTICLOCKWISE:
            self.event = self.encoder_a

        # Pass the button event to handleEvent()
        elif event == RotaryEncoder.BUTTONDOWN:
            self.event = self.encoder_switch
        else:
            self.statusLed.clear()
        
        self.gotEvent = True
            
    # Get configuration details from configuration class
    def getConfiguration(self):
        global left_switch,middle_switch,right_switch
        global encoder_a,encoder_b,encoder_switch

        # Button configuration
        self.left_switch = config.getLeftSwitch()
        self.middle_switch = config.getMiddleSwitch()
        self.right_switch = config.getRightSwitch()

        # Rotary encoder configuration
        self.encoder_switch = config.getEncoderSwitch()
        self.encoder_a = config.getEncoderA()
        self.encoder_b = config.getEncoderB()

        # Set up rotary encoder with rotary_event() as the callback routine
        self.rotaryknob = RotaryEncoder(self.encoder_a,self.encoder_b,
                self.encoder_switch,self.rotary_event)

        # Set up buttons
        Button(self.left_switch, self.button_event)
        Button(self.middle_switch, self.button_event)
        Button(self.right_switch, self.button_event)
            
    # Configure status LEDs
    def statusLedInitialise(self,statusLed):
        led1 = config.getLed1()
        led2 = config.getLed2()
        led3 = config.getLed3()
        statusLed = StatusLed(led1,led2,led3)
        return statusLed

    # Return program version
    def getVersion(self):   
        return _version

    def status(self):
        pid = self.getPid()
        if pid != None:
            print("cosmicd running pid:", pid)
        else:
            print("cosmicd not running")

    # Get process ID
    def getPid(self):
        pid = None
        if os.path.exists(pidfile):
            pf = open(pidfile,'r')
            pid = int(pf.read().strip())
        return pid

def usage():
    print("usage: %s start|stop|restart|status|version|nodaemon" % sys.argv[0])

### Main routine ###
if __name__ == "__main__":

    import pwd

    if pwd.getpwuid(os.geteuid()).pw_uid > 0:
        print("This program must be run with sudo or root permissions!")
        sys.exit(1)

    daemon = MyDaemon('/var/run/cosmicd.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            os.system("service mpd stop")
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        elif 'nodaemon' == sys.argv[1]:
            daemon.nodaemon()
        elif 'version' == sys.argv[1]:
            print('Version',daemon.getVersion())
        else:
            print("Unknown command: " + sys.argv[1])
            usage()
            sys.exit(2)
        sys.exit(0)
    else:
        usage()
        sys.exit(2)

# End of script

# set tabstop=4 shiftwidth=4 expandtab
# retab
