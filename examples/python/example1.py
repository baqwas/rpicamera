#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  example1.py
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
#  Note
#   RPi3 or older will need to enable Glamor using
#    * sudo raspi-config -> Advanced Options -> enable Glamor
#    * reboot
from picamera2 import Picamera2, Preview
import time

def main(args):
    picam2 = Picamera2()
    camera_config = picam2.create_preview_configuration()
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)
    # picam2.start_preview(Preview.DRM) # non-X-Windows use
    picam2.start()
    time.sleep(2)
    picam2.capture_file("example1_test.jpg")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))