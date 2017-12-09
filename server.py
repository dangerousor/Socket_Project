#!/usr/bin/python
# -*- coding:utf-8 -*-

import socket
from multiprocessing import Process

from func import linker

s = socket.socket()
host = socket.gethostname()
port = 9000
s.bind((host, port))

s.listen(4)
while True:
    conn, addr = s.accept()
    p = Process(target=linker, args=(conn, addr))
    p.start()
