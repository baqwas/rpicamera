#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  capture_circular_nooutput.py
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
"""
    Note
        RPi3 or older will need to enable Glamor using
        * sudo raspi-config -> Advanced Options -> enable Glamor
        * reboot
        This code is a direct reproduction of the original work 
        at https://github.com/raspberrypi/picamera2/blob/main/examples/capture_circular_nooutput.py
        All rights for that work belong to the original author(s)
        The modifications in this script are for internal use only
    Symbols
        myCamera - instantiation of PiCamera2 object
        frames_per_second -
        duration -
        video_config -
        encoder -
        output -
"""

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
import time

def main(args):
    
    myCamera = Picamera2()
    frames_per_second = 30
    duration = 5
    micro = int((1 / frames_per_second) * 1000000)
    video_config = myCamera.create_video_configuration()
    video_config['controls']['FrameDurationLimits'] = (micro, micro)
    myCamera.configure(video_config)
    encoder = H264Encoder()
    output = CircularOutput(buffersize=int(frames_per_second * 
        (duration + 0.2)), 
        outputtofile=False)
    output.fileoutput = "capture_circular_nooutput.h264"
    myCamera.start_recording(encoder, output)
    time.sleep(duration)
    output.stop()
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
