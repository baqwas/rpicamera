#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  capture_circular_stream.py
#  capture video for 5 secs when motion detection
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
        circular_buffer - buffer for video
        encoder - encoding entity
        encoding - flag to indicate encoding status
        lsize - (width, height), default (320, 240)
        myCamera - instantiation of PiCamera2 object
        previous - previous time mark
        server  - helper function to stream the captured video
        t - thread reference
        video_config - video configuration entity
"""

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput, FileOutput
from libcamera import Transform

import numpy as np

import socket
import threading
import time

def main(args):
    
    width = 320
    height = 240
    lsize = (width, height)
    myCamera = Picamera2()
    video_config = myCamera.create_video_configuration(main={"size": (1280, 720), "format": "RGB888"},
                                                     lores={"size": lsize, "format": "YUV420"})
    myCamera.configure(video_config)
    myCamera.start_preview(transform = Transform(hflip=1, vflip=1))
    encoder = H264Encoder(1000000, repeat=True)
    circular_buffer = CircularOutput()
    encoder.output = [circular_buffer]
    myCamera.encoders = encoder
    myCamera.start()
    myCamera.start_encoder()

    #width, height = lsize
    previous = None
    encoding = False
    ltime = 0


    def server():
        global circular_buffer, myCamera
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("0.0.0.0", 10001))
            sock.listen()
            while tup := sock.accept():
                event = threading.Event()
                conn, addr = tup
                stream = conn.makefile("wb")
                filestream = FileOutput(stream)
                filestream.start()
                encoder.output = [circular_buffer, filestream]
                filestream.connectiondead = lambda _: event.set()  # noqa
                event.wait()


    t = threading.Thread(target=server)
    t.setDaemon(True)
    t.start()

    while True:
        current = myCamera.capture_buffer("lores")
        current = current[:width * height].reshape(height, width)
        if previous is not None:
            # Measure pixels differences between current and
            # previous frame
            mean_sq_error = np.square(np.subtract(current, previous)).mean()
            if mean_sq_error > 7:
                if not encoding:
                    epoch = int(time.time())
                    circular_buffer.fileoutput = f"{epoch}.h264"
                    circular_buffer.start()
                    encoding = True
                    print(f"New Motion {mean_sq_error}")
                ltime = time.time()
            else:
                if encoding and time.time() - ltime > 5.0:
                    circular_buffer.stop()
                    encoding = False
        previous = current

    myCamera.stop_encoder()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
