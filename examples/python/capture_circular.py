#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  capture_circular.py
#  capture images into a circular buffer upon motion detection
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
#  Note
#   RPi3 or older will need to enable Glamor using
#    * sudo raspi-config -> Advanced Options -> enable Glamor
#    * reboot
#   This code is a direct reproduction of the original work at https://github.com/raspberrypi/picamera2/blob/main/examples/capture_circular.py
#   All rights for that work belong to the original author(s)
#   The modifications in this script are for internal use only
#
#   CircularOutput adds the ability to start a recording with video frames that
#   were from several seconds earlier with the following parameters:
#       file (default None) to construct a FileOutput
#       buffersize (default 150)  the number of seconds of video to access before current time
#           150 buffers = 5 secs of video * 30 fps
    H264Encoder:
        bitrate (default None)
        repeat (default False)
        iperiod (default None)
#  Symbols
#   myCamera - instantiation of PiCamera2 object
#   video_config - configuration entity for myCamera
#   images - encoder settings
#   sumcollector - video output file settings
#   image -
"""

import numpy as np
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
from libcamera import Transform
import time

def main(args):
    
    lsize = (320, 240)
    myCamera = Picamera2()
    video_config = myCamera.create_video_configuration(
        main={"size": (1280, 720), "format": "RGB888"},
        lores={"size": lsize, "format": "YUV420"},
        transform=Transform(hflip=True, vflip=True))
    myCamera.configure(video_config)
    myCamera.start_preview()
    encoder = H264Encoder(1000000, repeat=True)
    encoder.output = CircularOutput()
    
    myCamera.encoder = encoder
    myCamera.start()
    myCamera.start_encoder(encoder)

    w, h = lsize
    previous = None
    encoding = False
    last_time = 0

    while True:
        current = myCamera.capture_buffer("lores")
        current = current[:w * h].reshape(h, w)
        if previous is not None:
            mean_sq_error = np.square(np.subtract(current, previous)).mean()
            if mean_sq_error > 7:
                if not encoding:
                    epoch = int(time.time())
                    encoder.output.fileoutput = f"{epoch}.h264"
                    encoder.output.start()
                    encoding = True
                    print(f'New motion {mean_sq_error}')
                last_time = time.time()
            else:
                if encoding and time.time() - last_time > 5.0:
                    encoder.output.stop()
                    encoding = False
                    
        previous = current

    myCamera.stop_encoder()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
