#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  echo_client_ipv6.py
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
#   https://docs.python.org/3/library/socket.html#timeouts-and-the-accept-method
#  

import socket
import sys

def main(args):

    HOST = "raspbari14.parkcircus.org"  # The remote host
    PORT = 50007                        # The same port as used by the server
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        
        af, socktype, proto, canonname, sa = res
        
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
        
        try:
            s.connect(sa)
        except OSError as msg:
            s.close()
            s = None
            continue
        break
        
    if s is None:
        print("Unable to open socket")
        sys.exit(1)
        
    with s:
        s.sendall(b"Hello, World!")
        data = s.recv(1024)
    print("Received", repr(data))

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
