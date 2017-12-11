#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import json


def linker(sock, addr):
    print 'Accept new connection from %s:%s ...' % addr
    # sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        if data == 'exit':
            print 'Connection from %s:%s closed...' % addr
            exit(0)
        data_json = json.loads(data, 'utf-8')
        # if data_json['username'] == 'dangerousor' and data_json['password'] == 'network':
        if data_json['username'] == '123' and data_json['password'] == '123':
            sock.send(json.dumps({'status': 'success'}))
            break
        else:
            sock.send(json.dumps({'status': 'failure'}))
            pass
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        print data
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send('Hello, %s!' % data)
    sock.close()
    print 'Connection from %s:%s closed...' % addr
