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
        at https://github.com/raspberrypi/picamera2/blob/main/examples/capture_stream.py
        All rights for that work belong to the original author(s)
        The modifications in this script are for internal use only
        
        https://docs.python.org/3/library/socket.html#timeouts-and-the-accept-method
        
               
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
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(False)  # = sock.settimeout(0.0)
        sock.bind(("0.0.0.0", 10001))
        sock.listen()

        myCamera.encoders = encoder

        """
        Accept a connection
        The socket must be bound to an address and listening for connections
        The return value is a pair (conn, address) 
        where 
            conn is a new socket object usable to send and receive data on the connection, and 
            address is the address bound to the socket on the other end of the connection
            
        If the system call is interrupted and the signal handler does not raise an exception,
        the method now retries the system call instead of raising an InterruptedError exception
        
        accept() will block until a client sends a SYN packet to the open socket to start the 3-way handshake
        
        If no pending connections are present on the queue, and the
        socket is not marked as nonblocking, accept() blocks the caller
        until a connection is present.  If the socket is marked
        nonblocking and no pending connections are present on the queue,
        accept() fails with the error EAGAIN or EWOULDBLOCK.
        """

        connection, address = sock.accept()  # BlockingIOError [Errno 11] Resource temporarily unavailable if no prior client connection

        print("debug 6 ...")
        stream = connection.makefile("wb")
        print("debug 7 ...")
        encoder.output = FileOutput(stream)
        print("debug 8 ...")
        
        myCamera.start_encoder()
        print("debug 8 ...")
        myCamera.start()
        print("sleeping...")
        time.sleep(20)
        print("awake...")
        myCamera.stop()
        myCamera.stop_encoder()
        myCamera.close()

        connection.close()

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
