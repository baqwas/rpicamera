#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  capture_motion.py
#  capture video upon motion detection
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

import numpy as np
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import time


def main(args):

    width = 320
    height = 240
    lsize = (width, height)
    myCamera = Picamera2()
    
    config_video = myCamera.create_video_configuration(
        main={"size": (1280, 720), "format": "RGB888"},
        lores={"size": lsize, "format": "YUV420"})
    myCamera.configure(config_video)
    encoder = H264Encoder(10000000)
    myCamera.encoder = encoder

    myCamera.start()
    previous = None
    encoding = False
    last_time = 0

    while True:
        current = myCamera.capture_buffer("lores")
        current = current[:width * height].reshape(height, width)
        if previous is not None:
            mean_sq_error = np.square(np.subtract(current, previous)).mean()
            if mean_sq_error > 7:
                if not encoding:
                    encoder.output = FileOutput(f"capture_motion_{int(time.time())}.h264")
                    myCamera.start_encoder()
                    encoding = True
                    print(f"New motion {mean_sq_error}")
                last_time = time.time()
            else:
                if encoding and time.time() - last_time > 2.0:
                    myCamera.stop_encoder()
                    encoding = False
        previous = current

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
