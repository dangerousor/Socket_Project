#!/usr/bin/python
# -*- coding:utf-8 -*-


from Tkinter import *
import tkMessageBox as messageBox


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertButton = Button(self, text='Send', command=self.sendName)
        self.alertButton.pack()

    def sendName(self):
        name = self.nameInput.get() or 'Nobody'
        messageBox.showinfo('Name', 'Hello, %s' % name)


if __name__ == '__main__':
    app = Application()
    app.master.title('Hello World!')
    app.mainloop()
