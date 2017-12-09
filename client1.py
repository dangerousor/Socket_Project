#!/usr/bin/python
# -*- coding:utf-8 -*-


import socket
# import time
from Tkinter import *
import tkMessageBox as messageBox

from ui import Application


class Socket(Application):
    def __init__(self, master=None):
        self.mysocket = socket.socket()
        self.myhost = socket.gethostname()
        self.myport = 9000
        self.mysocket.connect((self.myhost, self.myport))
        Application.__init__(self, master)

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


if __name__ == '__main__':
    myclient = Socket()
    myclient.master.title('Hello')
    myclient.mainloop()
