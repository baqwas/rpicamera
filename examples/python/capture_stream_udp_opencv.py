#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  capture_stream_udp_opencv.py
#  Publish video from camera using a multicast stream
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

    1 Import the libraries
    2 Create a UDP socket
    3 Set the socket to multicast mode
    4 Join the multicast group that will receive the messages
    5 Capture vide camera output using OpenCV
    6 Encode the video camera output using a video encoder such FFmpeg
    7 Send the encoded video stream to the multicast group

"""

import cv2
import socket
import time


def main(args):

        multicast_group = "224.0.0.1"
        # create a UDP socket
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # set the socket to multicast mode
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)

        # join the multicast group
        # convert an IPv4 address from dotted-quad string format (for example, ‘123.45.67.89’) to 32-bit packed binary format,
        # as a bytes object four characters in length.
        mreq = socket.inet_aton(multicast_group)  # create a multicast group structure
        mreq += b'\0'                             # set the multicast group structure to the multicast group that should be joined
        mreq += socket.inet_aton("172.16.0.57")   # set the multicast group structure to the interface that should join the multicast group

        mySocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        
        # capture the video camera output using OpenCV
        video_capture = cv2.VideoCapture(0)
        
        # encode the output using an encoder (e.g. FFmpeg)
        encoder = cv2.VideoWriter_fourcc(*'mp4v')
        output_stream = cv2.VideoWriter("capture_stream_udp_opencv.mp4", encoder, 20, (640, 480))
        
        while True:
                
                # capture a frame from the camera
                return_code, video_frame = video_capture.read()

                # encode the frame
                return_code, encoded_frame = cv2.imencode(".mp4", video_frame)

                # send the encoded frame to the multicast group
                sock.sendto(encoded_frame.tobytes(), (multicast_group, 5000))
                
                # write the frame to the output file
                output_stream.write(video_frame)

                # display the frame
                cv2.imshow("capture_stream_udp_opencv", video_frame)

                # q is to leave the indefinite loop gracefully
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

        video_capture.release()
        output_stream.release()

        mySocket.close()  # close the socket

        return 0


if __name__ == '__main__':
        import sys
        sys.exit(main(sys.argv))
