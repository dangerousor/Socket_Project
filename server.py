#!/usr/bin/python
# -*- coding:utf-8 -*-

import socket
# from multiprocessing import Process
# from threading import Thread

from func import linker


HOST = 'localhost'
PORT = 9001


def runServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = HOST
    port = PORT
    s.bind((host, port))

    s.listen(1)
    while True:
        conn, addr = s.accept()
        # p = Process(target=linker, args=(conn, addr))
        # p = Thread(target=linker, args=(conn, addr))
        # p.start()
        linker(conn, addr)


if __name__ == '__main__':
    runServer()
