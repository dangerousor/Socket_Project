#!/usr/bin/python
# -*- coding:utf-8 -*-


import socket
# import time
from Tkinter import *
import tkMessageBox as messageBox
from tkFont import Font
import json


class Socket(Frame):
    def __init__(self, master=None):
        self.mysocket = socket.socket()
        self.myhost = socket.gethostname()
        self.myport = 9000
        self.mysocket.connect((self.myhost, self.myport))
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.welcomeLabel = Label(self, text=self.mysocket.recv(1024))
        self.welcomeLabel.pack()
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertButton = Button(self, text='Send', command=self.sendName)
        self.alertButton.pack()
        self.quitButton = Button(self, text='Quit', command=self.myQuit)
        self.quitButton.pack()

    def sendName(self):
        name = self.nameInput.get() or 'Nobody'
        self.mysocket.send(name.encode('utf-8'))
        message = self.mysocket.recv(1024)
        messageBox.showinfo('Name', '%s' % message)

    def myQuit(self):
        self.mysocket.send('exit')
        self.mysocket.close()
        self.quit()


class signFrame(Frame):
    def __init__(self, master=None, socketin=None):
        Frame.__init__(self, master)
        self.mySocket = socketin
        self.createWidgets()

    def createWidgets(self):
        self.empytyLabel = Label(self)
        self.empytyLabel.grid(row=0, stick=W, pady=10)
        self.userLabel = Label(self, text='账户: ')
        self.userLabel.grid(row=1, stick=W, pady=10)
        self.userInput = Entry(self)
        self.userInput.grid(row=1, column=1, stick=E)
        self.passwordLabel = Label(self, text='密码: ')
        self.passwordLabel.grid(row=2, stick=W, pady=10)
        self.passwordInput = Entry(self, show='*')
        self.passwordInput.grid(row=2, column=1, stick=E)
        self.signInButton = Button(self, text='登陆', command=self.signIn)
        self.signInButton.grid(row=3, stick=W, pady=10)
        self.QuitButton = Button(self, text='退出', command=self.myQuit)
        self.QuitButton.grid(row=3, column=1, stick=E)

    def signIn(self):
        username = self.userInput.get()
        password = self.passwordInput.get()
        print username
        if username == '' or password == '':
            messageBox.showwarning('提示', '用户名和密码不能为空！')
            return 1
        message = json.dumps({'username': username, 'password': password})
        self.mySocket.send(message)
        result = json.loads(self.mySocket.recv(1024))
        if result['status'] == 'success':
            messageBox.showinfo('提示', '登陆成功，自动从上次停止地方开始阅读。')
            self.destroy()
        else:
            messageBox.showerror('提示', '用户名或密码错误。')

    def myQuit(self):
        self.mySocket.send('exit')
        self.mySocket.close()
        self.quit()


class novelSelect(Frame):
    def __init__(self, master=None, socketin=None):
        self.mySocket = socketin
        Frame.__init__(self, master)
        self.createWidgets()

    def createWidgets(self):
        pass


class myTk(object):
    def __init__(self):
        self.myTk = Tk()
        self.myTk.minsize(500, 425)
        self.myTk.minsize(1000, 850)
        self.myTk.geometry('500x425+740+300')
        self.myTk.title('Reader')
        self.myTk.iconbitmap('favicon.ico')
        self.mySocket = socket.socket()
        self.myHost = socket.gethostname()
        self.myPort = 9000
        self.mySocket.connect((self.myHost, self.myPort))
        self.signinFrame = signFrame(master=self.myTk, socketin=self.mySocket)
        self.selectnovelFrame = novelSelect(master=self.myTk, socketin=self.mySocket)

    def myQuit(self):
        self.mySocket.send('exit')
        self.mySocket.close()
        self.myTk.quit()

if __name__ == '__main__':
    # myclient = Socket()
    # myclient.master.title('Hello')
    # myclient.mainloop()
    client = Tk()
    client.geometry('500x300+500+200')
    client.title('Reader')
    client.iconbitmap('favicon.ico')
    SignF = signFrame(master=client)
    SignF.mainloop()
    # SignF.pack()
    # client.mainloop()
    client.destroy()
