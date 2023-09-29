#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  capture_png.py
#  capture a PNG image while still running in preview mode
#  
#  Copyright 2023  <chowkidar@raspbari14>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
"""
    Note
        RPi3 or older will need to enable Glamor using
        * sudo raspi-config -> Advanced Options -> enable Glamor
        * reboot
        This code is a direct reproduction of the original work 
        at https://github.com/raspberrypi/picamera2/blob/main/examples/capture_png.py
        All rights for that work belong to the original author(s)
        The modifications in this script are for internal use only
        
               
    Symbols
        myCamera - instantiation of PiCamera2 object
        preview_config - preview configuration entity
        capture_config - image configuration entity
"""

from picamera2 import Picamera2, Preview
import time


def main(args):

    width = 800
    height = 600
    preview_window = (width, height)

    myCamera = Picamera2()
    myCamera.start_preview(Preview.QTGL)

    config_preview = myCamera.create_preview_configuration(main={"size": preview_window})
    myCamera.configure(config_preview)
    
    myCamera.start()
    time.sleep(2)

    myCamera.capture_file("capture_png.png")

    myCamera.stop()
    myCamera.close()

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
