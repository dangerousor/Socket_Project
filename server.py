#!/usr/bin/python
# -*- coding:utf-8 -*-

import socket
# from multiprocessing import Process
from threading import Thread

from func import linker


def runServer():
    s = socket.socket()
    host = socket.gethostname()
    port = 9000
    s.bind((host, port))

    s.listen(4)
    while True:
        conn, addr = s.accept()
        # p = Process(target=linker, args=(conn, addr))
        p = Thread(target=linker, args=(conn, addr))
        p.start()


if __name__ == '__main__':
    runServer()
