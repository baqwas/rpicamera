#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  capture_old_request.py
#  capture image and switch to another mode but then revert to earlier mode
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
        at https://github.com/raspberrypi/picamera2/blob/main/examples/capture_motion.py
        All rights for that work belong to the original author(s)
        The modifications in this script are for internal use only
        
               
    Symbols
        myCamera - instantiation of PiCamera2 object
        preview_config - preview configuration entity
        capture_config - image configuration entity
"""

from picamera2 import Picamera2
import time


def main(args):

    myCamera = Picamera2()
    config_capture = myCamera.create_still_configuration()
    myCamera.start(show_preview=True)
    
    time.sleep(1)
    
    request = myCamera.switch_mode_and_capture_request(config_capture) # preview will resume shortly

    time.sleep(1)

    request.save("main", "capture_old_request.jpg")  # save the earlier request and release  resources
    request.release()

    myCamera.stop()
    myCamera.close()

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
