#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  example2_image.py
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
#  
from picamera2 import Picamera2, Preview
from libcamera import Transform

def main(args):
    picam2 = Picamera2()
    picam2.start_preview(Preview.QTGL, width=640, height=480,
        transform = Transform(hflip=1, vflip=1))
    picam2.start_and_capture_file("example2_image.jpg")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
