#!/usr/bin/python
# -*- coding:utf-8 -*-
# import time
# import json
import struct


BUFF = bytes()
HEADERSIZE = 8
# message Max 4GB


# cmd              code
# exit               0
# exit with log      1
# log in            101
# last chapter      201
# next chapter      202
# download          301
# jump to mark      401

def recv_all(sock):
    global BUFF, HEADERSIZE
    flagh = 0
    flagb = 0
    while True:
        data = sock.recv(2048)
        if data:
            BUFF += data
            while True:
                if flagh == 0:
                    if len(BUFF) < HEADERSIZE:
                        break
                    else:
                        headerpart = struct.unpack('!2I', BUFF[:HEADERSIZE])
                        bodysize = headerpart[0]
                        flagh = 1
                if len(BUFF) < HEADERSIZE + bodysize:
                    break
                bodypart = BUFF[HEADERSIZE:HEADERSIZE + bodysize]
                cmd = headerpart[1]
                BUFF = BUFF[HEADERSIZE + bodysize:]
                flagb = 1
            if flagb == 1:
                break
        if not data:
            raise EOFError('socket closed %d bytes into a %d-byte message' % (len(data), bodysize + HEADERSIZE))
    return {'cmd': cmd, 'bodypart': bodypart}


def send_all(sock, cmd, messagetosend):
    length = len(messagetosend)
    header = [length, cmd]
    headerpart = struct.pack('!2I', *header)
    senddata = headerpart + messagetosend
    sock.sendall(senddata)


def linker(sock, addr):
    print 'Accept new connection from %s:%s ...' % addr
    # sock.send(b'Welcome!')
    with open('content.json', 'rb+') as f:
        contentjson = eval(f.read())
    while True:
        data = recv_all(sock)
        if data['cmd'] == 0:
            # print 'Connection from %s:%s closed...' % addr
            break
        elif data['cmd'] == 1:
            bodypart = data['bodypart']
            with open('log.json', 'wb+') as f:
                f.write(bodypart)
            break
        elif data['cmd'] == 101:
            data_json = eval(data['bodypart'])
            # if data_json['username'] == 'dangerousor' and data_json['password'] == 'network':
            if data_json['username'] == '123' and data_json['password'] == '123':
                userlog = getLog()
                # filepath = str(userlog['bigchapter']) + '/' + str(userlog['chapter']) + '.txt'
                filepath = 'novel/' + contentjson['bigchapter'][userlog['bigchapter']]['bigname'] + '/' + contentjson['bigchapter'][userlog['bigchapter']]['chapter'][userlog['chapter']]['filename'].decode('utf-8') + '.txt'
                with open(filepath, 'rb+') as f:
                    content = f.read()
                send_all(sock, 101, repr({'status': 'success',
                                          'bigchapter': userlog['bigchapter'],
                                          'chapter': userlog['chapter'],
                                          'content': content,
                                          'page': userlog['page'],
                                          'marks': userlog['marks']}))
            else:
                send_all(sock, 101, repr({'status': 'failure'}))
        elif data['cmd'] == 201:
            bodypart = eval(data['bodypart'])
            bigchapter = bodypart['bigchapter']
            chapter = bodypart['chapter']
            if bigchapter == 0 and chapter == 0:
                message = {}
                send_all(sock, 1001, repr(message))
            elif chapter == 0:
                bigchapter -= 1
                chapter = len(contentjson['bigchapter'][bigchapter]['chapter']) - 1
                send_all(sock, 201, repr(makeNovelSendJson(bigchapter, chapter, 1, contentjson)))
            else:
                chapter -= 1
                send_all(sock, 201, repr(makeNovelSendJson(bigchapter, chapter, 1, contentjson)))
        elif data['cmd'] == 202:
            bodypart = eval(data['bodypart'])
            bigchapter = bodypart['bigchapter']
            chapter = bodypart['chapter']
            if bigchapter == contentjson['endBig'] and chapter == contentjson['endCha']:
                message = {}
                send_all(sock, 1002, repr(message))
            elif chapter + 1 == len(contentjson['bigchapter'][bigchapter]['chapter']):
                bigchapter += 1
                chapter = 0
                send_all(sock, 202, repr(makeNovelSendJson(bigchapter, chapter, 1, contentjson)))
            else:
                chapter += 1
                send_all(sock, 201, repr(makeNovelSendJson(bigchapter, chapter, 1, contentjson)))
        elif data['cmd'] == 301:
            bodypart = eval(data['bodypart'])
            bigchapter = bodypart['bigchapter']
            chapter = bodypart['chapter']
            chaptername = contentjson['bigchapter'][bigchapter]['chapter'][chapter]['filename']
            message = makeNovelSendJson(bigchapter, chapter, 1, contentjson)
            send_all(sock, 301, repr({'chaptername': chaptername, 'content': message['content']}))
        elif data['cmd'] == 401:
            bodypart = eval(data['bodypart'])
            bigchapter = bodypart['bigchapter']
            chapter = bodypart['chapter']
            page = bodypart['page']
            message = makeNovelSendJson(bigchapter, chapter, page, contentjson)
            send_all(sock, 401, repr(message))
    sock.close()
    print 'Connection from %s:%s closed...' % addr


def makeNovelSendJson(bc, c, p, conjson):
    filepath = 'novel/' + conjson['bigchapter'][bc]['bigname'] + '/' + conjson['bigchapter'][bc]['chapter'][c]['filename'].decode('utf-8') + '.txt'
    with open(filepath, 'rb+') as f:
        content = f.read()
    return {'bigchapter': bc,
            'chapter': c,
            'content': content,
            'page': p}


def getLog():
    with open('log.json', 'rb+') as f:
        result = eval(f.read())
    return result
