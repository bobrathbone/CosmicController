#!/usr/bin/env python3
# Raspberry Pi IQAudio Cosmic Controller Development Templates
# See IQAudio website at  http://iqaudio.co.uk
#
# Raspberry Pi OLED 128x64 test program
# Animation example
#
# $Id: test_graphics.py,v 1.2 2022/09/28 08:20:17 bob Exp $
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#      The authors shall not be liable for any loss or damage however caused.
#
# Adapted from the clowns test program from Olimex Limited, www.olimex.com
# See https://github.com/SelfDestroyer/pyMOD-OLED.git
# 

import sys,time

# Import OLED routines
from oled_class import Oled

# Class test routine
if __name__ == "__main__":

    try:
        oled = Oled()
        oled.clear()

        # Change False to True to flip display
        oled.flip_display_vertically(True)

        # Draw splash
        oled.drawSplash("bitmaps/raspberry-pi-logo.bmp",2)

        fill = False
        oled.drawCircle(35,32,25,fill)

        oled.drawRectangle(80,10,120,55,fill)
        oled.drawLine(0,0,127,63)

        oled.update()

        time.sleep(1)
        fill = True
        oled.drawRectangle(80,10,120,55,fill)
        oled.drawCircle(35,32,25,fill)

        oled.update()
        time.sleep(1)
        oled.clear()

        # A bit of animation
        x = 35  # X position
        y = 0   # y position

        print("Press CTL-C to exit")
        while True:
            for i in range(1,8):
                image = "bitmaps/clown" + str(i) + ".bmp"
                oled.drawImage(image,x,y)
                oled.drawLine(0,63,127,63)
                oled.update()
                time.sleep(0.02)

    # Press CTL-C to interrupt
    except KeyboardInterrupt:
        print("\nExit")
        sys.exit(0)

# End of test code
# set tabstop=4 shiftwidth=4 expandtab
# retab
