#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  capture_multiplexer.py
#  capture images with multiple cameras
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

import picamera2


def main(args):

    def take_photo(camera_chosen):

        camera2use = picamera2.Picamera2(camera_num=camera_chosen)
        config_capture = camera2use.create_still_configuration()
        camera2use.start()
        camera2use.switch_mode_and_capture_file(config_capture, f"capture_multiplexer_a_{camera_chosen}.jpg")
        camera2use.stop()
        camera2use.close()
        
        return 0

    camera_max = 1  # number of cameras accessible to the board

    # either
    for camera in range(camera_max):
        take_photo(camera)


    # or
    for camera in range(camera_max):
        myCamera = picamera2.Picamera2(camera_num=camera)
        config_capture = myCamera.create_still_configuration()
        myCamera.start()
        myCamera.switch_mode_and_capture_file(config_capture, f"capture_multiplexer_b_{camera}.jpg")
        myCamera.stop()
        myCamera.close()

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
