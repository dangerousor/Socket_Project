#!/usr/bin/python
# -*- coding:utf-8 -*-
import time


def linker(sock, addr):
    print 'Accept new connection from %s:%s ...' % addr
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send('Hello, %s!' % data)
    sock.close()
    print 'Connection from %s:%s closed...' % addr
