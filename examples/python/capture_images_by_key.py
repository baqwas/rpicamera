#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  capture_images_by_key.py
#  capture PNG image in preview mode when key p is pressed and 
#   quit  when key q is pressed
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
        at https://github.com/raspberrypi/picamera2/blob/main/examples/capture_images_by_key.py
        All rights for that work belong to the original author(s)
        The modifications in this script are for internal use only
        
        pynput - https://buildmedia.readthedocs.org/media/pdf/pynput/latest/pynput.pdf
               
    Symbols
        myCamera - instantiation of PiCamera2 object
        preview_config - preview configuration entity
        capture_config - image configuration entity
"""

from picamera2 import Picamera2, Preview
from pynput import keyboard
from sys import stdin
from termios import TCIOFLUSH, tcflush
import time


pressed_p = False
pressed_q = False


"""
The listener callbacks are invoked directly from an operating thread on some platforms, notably Windows.
This means that long running procedures and blocking operations should not be invoked from the callback, as 
this risks freezing input for all processes.
Dispatch incoming messages to a queue and let a separate thread handle them
"""
def on_press(key):

    global pressed_p
    global pressed_q

    # print(f"Detected {key}")

    try:
        # if key == Key.f1:
        if key == 'p':
            pressed_p = True
        # if key == Key.esc:
        if key == 'q':
            pressed_q = True
    except AttributeError:
        print(f"Unhandled key {key}")

with keyboard.Listener(on_press=on_press) as listener:
    try:
        listener.join()
        
    except Exception as e:
        print(f"Listener exception {e}")
            

def main(args):

    global pressed_p
    global pressed_q

            
    print(f".outer loop.")

    myCamera = Picamera2()
    myCamera.start_preview(Preview.QTGL)

    myCamera.start()


    try:
        while True:
            print(f".inner loop.")
            if pressed_p:
                pressed_p = False
                filename = "capture_images_by_key_" + strftime("%Y%m%d-%H%M%S") + ".png"
                myCamera.capture_file(filename, format="png", wait=None)
                # print(f"Captured {filename} successfully\r")
            elif pressed_q:
                # print("All done!")
                break

    finally:
        myCamera.stop_preview()
        myCamera.stop()
        myCamera.close()
        tcflush(stdin, TCIOFLUSH)

    listener.stop() # cannot restart since it is an instance of threading.Thread


    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
