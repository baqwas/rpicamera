#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  capture_average.py
#  capture multiple images and average to reduce noise
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
#   This code is a direct reproduction of the original work at https://github.com/raspberrypi/picamera2/blob/main/examples/capture_average.py
#   All rights for that work belong to the original author(s)
#   The modifications in this script are for internal use only
#  Symbols
#   myCamera - instantiation of PiCamera2 object
#   video_config - configuration entity for myCamera
#   images - encoder settings
#   sumcollector - video output file settings
#   image -

import numpy as np
from picamera2 import Picamera2, Preview
from PIL import Image
from libcamera import Transform
import time

def main(args):
    
    myCamera = Picamera2()
    """
        for RPi camera modules, flipping may be required
        Transforms can be passed to all the configuration-generating methods 
        using the transform keyword parameter
    """
    myCamera.start_preview(Preview.NULL)
    image_config = myCamera.create_still_configuration(
        transform=Transform(hflip=True, vflip=True))
    myCamera.configure(image_config)
    
    myCamera.start()
    time.sleep(2)

    with myCamera.controls as ctrl:
        ctrl.AnalogueGain = 1.0
        ctrl.ExposureTime = 400000
    time.sleep(2)

    images = 25
    sumval = None
    for _ in range(images):
        if sumval is None:
            sumval = np.longdouble(myCamera.capture_array())
            image1 = Image.fromarray(np.uint8(sumval))
            image1.save("capture_average_original.jpg")
        else:
            sumval += np.longdouble(myCamera.capture_array())

    image1 = Image.fromarray(np.uint8(sumval / images))
    image1.save("capture_average_averaged.jpg")

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
