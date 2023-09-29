#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  capture_stream.py
#  Stream video from camera using a socket connection
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
        at https://github.com/raspberrypi/picamera2/blob/main/examples/capture_stream_udp.py
        All rights for that work belong to the original author(s)
        The modifications in this script are for internal use only
        
        socket - https://docs.python.org/3/library/socket.html
               
    Symbols
        myCamera - instantiation of PiCamera2 object
        preview_config - preview configuration entity
        capture_config - image configuration entity
"""

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import socket
import time


def main(args):

    width = 1280
    height = 720
    window_config = (width, height)

    myCamera = Picamera2()
    config_video = myCamera.create_video_configuration(main={"size": window_config})
    myCamera.configure(config_video)
    encoder = H264Encoder(1000000)
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:  # UDP socket
        # set the socket to multicast mode
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        
        # join the multicast group
        multicast_request = socket.inet_aton("224.0.0.1")
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicast_request + b'\0')
        
        # send camera output?
        sock.sendto(???, ("224.0.0.1", 10001))
        
        stream = sock.makefile("wb")
        
        picam2.start_recording(encoder, FileOutput(stream))
        time.sleep(20)

        myCamera.stop_recording()
        myCamera.stop()
        myCamera.close()

        sock.close()

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
