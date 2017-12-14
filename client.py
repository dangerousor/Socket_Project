#!/usr/bin/python
# -*- coding:utf-8 -*-


import socket
# import time
from Tkinter import *
import tkMessageBox as messageBox
from tkFont import Font
# import json
import textwrap
from win32api import GetSystemMetrics
import struct
import os


WIDTH = GetSystemMetrics(0)
HEIGHT = GetSystemMetrics(1)
HOST = 'localhost'
PORT = 9001
BUFF = bytes()
HEADERSIZE = 8
# message Max 4GB


#       cmd                     code
# no last chapter               1001
# no next chapter               1002


# class Socket(Frame):
#     def __init__(self, master=None):
#         self.mysocket = socket.socket()
#         self.myhost = socket.gethostname()
#         self.myport = 9000
#         self.mysocket.connect((self.myhost, self.myport))
#         Frame.__init__(self, master)
#         self.pack()
#         self.createWidgets()
#
#     def createWidgets(self):
#         self.welcomeLabel = Label(self, text=self.mysocket.recv(1024))
#         self.welcomeLabel.pack()
#         self.nameInput = Entry(self)
#         self.nameInput.pack()
#         self.alertButton = Button(self, text='Send', command=self.sendName)
#         self.alertButton.pack()
#         self.quitButton = Button(self, text='Quit', command=self.myQuit)
#         self.quitButton.pack()
#
#     def sendName(self):
#         name = self.nameInput.get() or 'Nobody'
#         self.mysocket.send(name.encode('utf-8'))
#         message = self.mysocket.recv(1024)
#         messageBox.showinfo('Name', '%s' % message)
#
#     def myQuit(self):
#         self.mysocket.send('exit')
#         self.mysocket.close()
#         self.quit()


class signFrame(Frame):
    def __init__(self, master=None, socketin=None):
        Frame.__init__(self, master)
        self.mySocket = socketin
        self.createWidgets()

    def createWidgets(self):
        # self.empytyLabel = Label(self)
        # self.empytyLabel.grid(row=0, stick=W, pady=10)
        self.userLabel = Label(self, text='账户: ')
        self.userLabel.grid(row=1, stick=W, pady=10)
        self.userInput = Entry(self)
        self.userInput.grid(row=1, column=1, stick=E)
        self.passwordLabel = Label(self, text='密码: ')
        self.passwordLabel.grid(row=2, stick=W, pady=10)
        self.passwordInput = Entry(self, show='*')
        self.passwordInput.grid(row=2, column=1, stick=E)
        self.passwordInput.bind('<Key-Return>', self.signIn)
        self.signInButton = Button(self, text='登陆', command=self.signIn)
        self.signInButton.grid(row=3, stick=W, pady=10)
        self.quitButton = Button(self, text='退出', command=self.myQuit)
        self.quitButton.grid(row=3, column=1, stick=E)

    def signIn(self, key=None):
        username = self.userInput.get()
        password = self.passwordInput.get()
        if username == '' or password == '':
            messageBox.showwarning('提示', '用户名和密码不能为空！')
            return 1
        message = repr({'username': username, 'password': password})
        send_all(self.mySocket, 101, message)
        result = recv_all(self.mySocket)
        self.buff = result
        if eval(result['bodypart'])['status'] == 'success':
            messageBox.showinfo('提示', '登陆成功，自动从上次停止地方开始阅读。')
            # self.destroy()
            self.quit()
        else:
            messageBox.showerror('提示', '用户名或密码错误。')

    def myQuit(self, key=None):
        send_all(self.mySocket, 0, repr({}))
        self.mySocket.close()
        self.quit()
        exit(0)


class mainFrame(Frame):
    def __init__(self, master=None, socketin=None, packet=None, bg=None):
        self.mySocket = socketin
        self.buff = packet
        self.bodypart = eval(self.buff['bodypart'])
        self.marks = self.bodypart['marks']
        self.bigchapter = self.bodypart['bigchapter']
        self.chapter = self.bodypart['chapter']
        self.currentPage = IntVar()
        self.currentPage.set(self.bodypart['page'])
        self.thisPage = StringVar()
        self.totalPage = IntVar()
        self.novel = self.getNovel()
        Frame.__init__(self, master, bg=bg)
        # self.createFrames()
        self.createWidgets()
        self.bind('<Key-Up>', self.jumpLast)
        self.bind('<Key-Left>', self.jumpLast)
        self.bind('<Key-Right>', self.jumpNext)
        self.bind('<Key-Down>', self.jumpNext)
        self.bind('<Key-Escape>', self.myQuit)
        self.focus_set()
    #
    # def createFrames(self):
    #     self.menuFrame = Frame(self, height=HEIGHT/30, bg='blue')
    #     self.createMenuWidgets()
    #     self.novelFrame = Frame(self, bg='red')
    #     self.createNovelWidgets()
    #     self.jumpFrame = Frame(self, height=HEIGHT/30, bg='green')
    #     self.createJumpWidgets()
    #     self.menuFrame.grid(row=0, column=0)
    #     self.novelFrame.grid(row=1, column=0)
    #     self.jumpFrame.grid(row=2, column=0)

    def createWidgets(self):
        self.checkButton = Button(self, text='查看书签', command=self.checkMark)
        # self.unlikeButton.grid(in_=self, row=0, column=1, ipady=5)
        self.checkButton.place(x=10, y=5, width=60, height=30)
        self.likeButton = Button(self, text='添加书签并添加后面的备注：', command=self.addMark)
        # self.likeButton.grid(in_=self, row=0, column=0, ipady=5)
        self.likeButton.place(x=80, y=5, width=230, height=30)
        self.commentMark = Entry(self)
        self.commentMark.place(x=320, y=5, width=200, height=30)
        self.jumpButton = Button(self, text='跳转书签号：', command=self.jumpMark)
        # self.unlikeButton.grid(in_=self, row=0, column=1, ipady=5)
        self.jumpButton.place(x=530, y=5, width=120, height=30)
        self.jumpNumb = Entry(self)
        # self.unlikeButton.grid(in_=self, row=0, column=1, ipady=5)
        self.jumpNumb.place(x=660, y=5, width=50, height=30)
        self.unlikeButton = Button(self, text='删除书签号：', command=self.delMark)
        # self.unlikeButton.grid(in_=self, row=0, column=1, ipady=5)
        self.unlikeButton.place(x=720, y=5, width=120, height=30)
        self.delNumb = Entry(self)
        # self.unlikeButton.grid(in_=self, row=0, column=1, ipady=5)
        self.delNumb.place(x=850, y=5, width=50, height=30)
        self.freelikeButton = Button(self, text='清空书签', command=self.freeMark)
        # self.unlikeButton.grid(in_=self, row=0, column=1, ipady=5)
        self.freelikeButton.place(x=910, y=5, width=60, height=30)
        self.jumpPageButton = Button(self, text='跳转页号：', command=self.jumpPage)
        # self.unlikeButton.grid(in_=self, row=0, column=1, ipady=5)
        self.jumpPageButton.place(x=1000, y=5, width=120, height=30)
        self.jumpPageNumb = Entry(self)
        # self.unlikeButton.grid(in_=self, row=0, column=1, ipady=5)
        self.jumpPageNumb.place(x=1130, y=5, width=50, height=30)
        self.downloadButton = Button(self, text='下载此章', command=self.downloadChapter)
        # self.likeButton.grid(in_=self, row=0, column=5, ipady=5)
        self.downloadButton.place(x=1690, y=5, width=60, height=30)
        # self.likeButton = Button(self.menuFrame, text='添加书签', command=self.addMark)
        # self.likeButton.grid(row=0, column=3, pady=5)
        # self.likeButton = Button(self.menuFrame, text='添加书签', command=self.addMark)
        # self.likeButton.grid(row=0, column=4, pady=5)
        self.quitButton = Button(self, text='退出/Esc', command=self.myQuit)
        # self.quitButton.grid(in_=self, row=0, column=6, ipady=5)
        self.quitButton.place(x=1760, y=5, width=150, height=30)
        self.thisPage.set(self.novel[self.currentPage.get()-1])
        self.FT = Font(family='system', size=20, weight=NORMAL)
        self.novelPage = Label(self, textvariable=self.thisPage, font=self.FT, justify=LEFT, bg='brown')
        # self.novelPage.grid(row=1, column=3)
        self.novelPage.place(x=10, y=40, width=1900, height=1000)
        self.lastChapter = Button(self, text='上一章', command=self.jumpLastChapter, width=30)
        # self.lastPage.grid(in_=self, row=6, column=3)
        self.lastChapter.place(x=400, y=1045, width=150, height=30)
        self.lastPage = Button(self, text='上一页 ↑/←', command=self.jumpLast, width=30)
        # self.lastPage.grid(in_=self, row=6, column=3)
        self.lastPage.place(x=700, y=1045, width=150, height=30)
        self.currentPageLabel = Label(self, textvariable=self.currentPage)
        self.currentPageLabel.place(x=880, y=1045, width=30, height=30)
        self.separateLabel = Label(self, text='/')
        self.separateLabel.place(x=910, y=1045, width=20, height=30)
        self.totalPageLabel = Label(self, textvariable=self.totalPage)
        self.totalPageLabel.place(x=930, y=1045, width=30, height=30)
        self.nextPage = Button(self, text='下一页 ↓/→', command=self.jumpNext, width=30)
        # self.lastPage.grid(in_=self, row=6, column=3)
        self.nextPage.place(x=1070, y=1045, width=150, height=30)
        self.nextChapter = Button(self, text='下一章', command=self.jumpNextChapter, width=30)
        # self.lastPage.grid(in_=self, row=6, column=3)
        self.nextChapter.place(x=1370, y=1045, width=150, height=30)

    def addMark(self):
        comment = self.commentMark.get()
        check = messageBox.askquestion('添加书签', '添加本页到书签？\n备注：%s' % comment.encode('utf-8'))
        if check == 'yes':
            pass
        else:
            return
        markinfo = {'bigchapter': self.bigchapter, 'chapter': self.chapter, 'page': self.currentPage.get(), 'comment': comment}
        self.marks.append(markinfo)
        self.focus_set()

    def delMark(self):
        number = self.delNumb.get()
        if number == '':
            return
        else:
            number = int(number)
        if 0 < number <= len(self.marks):
            check = messageBox.askyesno('删除书签', '是否删除书签%d：%s' % (number, self.marks[number-1]['comment'].encode('utf-8')))
            if check is False:
                return
            del self.marks[number - 1]
        else:
            messageBox.showerror('错误', '请输入正确的数字')
            return
        messageBox.showinfo('删除书签', '已经删除第%d个书签' % number)
        self.focus_set()

    def checkMark(self):
        # self.thisPage.set('\n'.join(self.novel[30:60]))
        marks = []
        for i in range(len(self.marks)):
            marks.append('No.%d     备注：%s' % (i + 1, self.marks[i]['comment'].encode('utf-8')))
        messageBox.showinfo('书签', '\n'.join(marks))
        self.focus_set()

    def freeMark(self):
        check = messageBox.askyesno('清空书签', '是否要清空所有书签？')
        if check is False:
            return
        self.marks = []
        messageBox.showinfo('清除书签', '已经清空所有书签')
        self.focus_set()

    def jumpMark(self):
        number = self.jumpNumb.get()
        if number == '':
            return
        else:
            number = int(number)
        if 0 < number <= len(self.marks):
            check = messageBox.askyesno('跳转书签', '是否跳转到书签%d：%s' % (number, self.marks[number - 1]['comment'].encode('utf-8')))
            if check is False:
                return
            if self.marks[number - 1]['bigchapter'] == self.bigchapter and self.marks[number - 1]['chapter'] == self.chapter:
                self.jumpPage(self.marks[number - 1]['page'])
            else:
                message = {'bigchapter': self.marks[number - 1]['bigchapter'], 'chapter': self.marks[number - 1]['chapter'], 'page': self.marks[number - 1]['page']}
                send_all(self.mySocket, 401, repr(message))
                result = recv_all(self.mySocket)
                self.bodypart = eval(result['bodypart'])
                self.novel = self.getNovel()
                self.bigchapter = self.bodypart['bigchapter']
                self.chapter = self.bodypart['chapter']
                self.currentPage.set(self.bodypart['page'])
                self.thisPage.set(self.novel[self.currentPage.get() - 1])
        else:
            messageBox.showerror('错误', '请输入正确的数字')
            return
        self.focus_set()

    def jumpPage(self, page=None):
        if page is None:
            page = self.jumpPageNumb.get()
            if page == '':
                return
            else:
                page = int(page)
        if 0 < page <= self.totalPage.get():
            self.thisPage.set(self.novel[page - 1])
            self.currentPage.set(page)
        else:
            messageBox.showerror('错误', '请输入正确的数字')
        self.focus_set()

    def jumpLast(self, event=None):
        if self.currentPage.get() == 1:
            answer = messageBox.askyesno('返回上一章', '已经是第一页了，是否阅读上一章？')
            if answer is True:
                self.jumpLastChapter()
                return
            else:
                return
        self.currentPage.set(self.currentPage.get() - 1)
        self.thisPage.set(self.novel[self.currentPage.get()-1])

    def jumpNext(self, event=None):
        if self.currentPage.get() == self.totalPage.get():
            answer = messageBox.askyesno('进入下一章', '已经是最后一页了，是否阅读下一章？')
            if answer is True:
                self.jumpNextChapter()
                return
            else:
                return
        self.currentPage.set(self.currentPage.get() + 1)
        self.thisPage.set(self.novel[self.currentPage.get()-1])

    def jumpLastChapter(self):
        message = {'bigchapter': self.bigchapter, 'chapter': self.chapter}
        send_all(self.mySocket, 201, repr(message))
        result = recv_all(self.mySocket)
        if result['cmd'] == 1001:
            messageBox.showinfo('提示', '这已经是第一章了，没有上一章啦。')
        else:
            self.bodypart = eval(result['bodypart'])
            self.novel = self.getNovel()
            self.bigchapter = self.bodypart['bigchapter']
            self.chapter = self.bodypart['chapter']
            self.currentPage.set(self.bodypart['page'])
            self.thisPage.set(self.novel[self.currentPage.get() - 1])

    def jumpNextChapter(self):
        message = {'bigchapter': self.bigchapter, 'chapter': self.chapter}
        send_all(self.mySocket, 202, repr(message))
        result = recv_all(self.mySocket)
        if result['cmd'] == 1002:
            messageBox.showinfo('提示', '这已经是最后一章了，没有下一章啦。')
        else:
            self.bodypart = eval(result['bodypart'])
            self.novel = self.getNovel()
            self.bigchapter = self.bodypart['bigchapter']
            self.chapter = self.bodypart['chapter']
            self.currentPage.set(self.bodypart['page'])
            self.thisPage.set(self.novel[self.currentPage.get() - 1])

    def getNovel(self):
        x = self.bodypart['content'].decode('utf-8').splitlines()
        xall = []
        yall = []
        for each in x:
            xall.extend(textwrap.wrap(each, 70))
        if len(xall) % 30 == 0:
            length = len(xall) / 30
        else:
            length = len(xall) / 30 + 1
        for i in range(length):
            yall.append('\n'.join(xall[i * 30: (i + 1) * 30]))
        self.totalPage.set(length)
        return yall

    def downloadChapter(self):
        message = {'bigchapter': self.bigchapter, 'chapter': self.chapter}
        send_all(self.mySocket, 301, repr(message))
        novel = eval(recv_all(self.mySocket)['bodypart'])
        if os.path.exists('download'):
            pass
        else:
            os.mkdir('download')
        with open('download/' + novel['chaptername'].decode('utf-8') + '.txt', 'wb+') as f:
            f.write(novel['content'])
        messageBox.showinfo('Finished', '本章已下载，请查看"download/%s.txt"' % novel['chaptername'])

    def myQuit(self, event=None):
        message = {'bigchapter': self.bigchapter, 'chapter': self.chapter, 'page': self.currentPage.get(), 'marks': self.marks}
        send_all(self.mySocket, 1, repr(message))
        self.mySocket.close()
        self.quit()
        exit(0)


class myTk(object):
    def __init__(self):
        self.myTk = Tk()
        self.myTk.minsize(WIDTH, HEIGHT)
        # self.myTk.maxsize(1000, 850)
        self.myTk.geometry('%sx%s' % (WIDTH, HEIGHT))
        self.myTk.attributes("-fullscreen", True)
        self.myTk.title('Reader')
        self.myTk.iconbitmap('favicon.ico')
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.myHost = HOST
        self.myPort = PORT
        self.mySocket.connect((self.myHost, self.myPort))
        self.signinFrame = signFrame(master=self.myTk, socketin=self.mySocket)
        # self.signinFrame.bind('<Key-q>', self.myQuit)
        self.signinFrame.pack(pady=300, padx=80)
        # self.signinFrame.focus_set()

    def myPrint(self, key=None):
        print key.char

    def start(self):
        self.myTk.mainloop()
        self.buff = self.signinFrame.buff
        self.signinFrame.destroy()
        self.mainFrame = mainFrame(master=self.myTk, socketin=self.mySocket, packet=self.buff, bg='brown')
        self.mainFrame.place(x=0, y=0, width=1980, height=1080)
        self.myTk.mainloop()
        self.myTk.quit()

    def myQuit(self, key=None):
        send_all(self.mySocket, 0, repr({}))
        self.mySocket.close()
        self.myTk.quit()
        exit(0)


def recv_all(sock):
    global BUFF, HEADERSIZE
    flag = 0
    while True:
        data = sock.recv(2048)
        if data:
            BUFF += data
            if flag == 0:
                if len(BUFF) < HEADERSIZE:
                    continue
                else:
                    headerpart = struct.unpack('!2I', BUFF[:HEADERSIZE])
                    bodysize = headerpart[0]
                    cmd = headerpart[1]
                    flag = 1
            if len(BUFF) < HEADERSIZE + bodysize:
                continue
            bodypart = BUFF[HEADERSIZE:HEADERSIZE + bodysize]
            BUFF = BUFF[HEADERSIZE + bodysize:]
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


if __name__ == '__main__':
    # myclient = Socket()
    # myclient.master.title('Hello')
    # myclient.mainloop()
    # client = Tk()
    # client.geometry('500x300+500+200')
    # client.title('Reader')
    # client.iconbitmap('favicon.ico')
    # SignF = signFrame(master=client)
    # SignF.mainloop()
    # SignF.pack()
    # client.mainloop()
    # client.destroy()
    print WIDTH
    print HEIGHT
    if WIDTH != 1920 or HEIGHT != 1080:
        print '显示器分辨率不支持！'
        exit(1)
    client = myTk()
    client.start()
