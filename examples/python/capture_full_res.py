#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  capture_full_res.py
#  capture image in JPEG format while running preview
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
        at https://github.com/raspberrypi/picamera2/blob/main/examples/capture_circular_nooutput.py
        All rights for that work belong to the original author(s)
        The modifications in this script are for internal use only
        
        DNG contains the raw image data and the associated metadata to render the image
        https://helpx.adobe.com/camera-raw/digital-negative.html
        JPEG XL
        https://en.wikipedia.org/wiki/JPEG_XL
        
        The preview and capture config modes are different.
        
    Symbols
        myCamera - instantiation of PiCamera2 object
        preview_config - preview configuration entity
        capture_config - image configuration entity
"""

from picamera2 import Picamera2, Preview
import time

def main(args):

    myCamera = Picamera2()
    myCamera.start_preview(Preview.QTGL)

    preview_config = myCamera.create_preview_configuration()
    capture_config = myCamera.create_still_configuration(raw={})
    myCamera.configure(preview_config)

    myCamera.start()
    time.sleep(2)

    myCamera.switch_mode_and_capture_file(capture_config, "capture_full_res.jpg")

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
