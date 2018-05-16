from tkinter import *

class Checkbar(Frame):
    def __init__(self, master, row, column, text):

        Frame.__init__(self, master)
        self.grid(row=row, column=column)
        self.configure(background='#ADD8E6')
        self.var = IntVar()
        self.checkbutton = None
        self.on_create(text, self.var)

    def on_create(self, text, variable):
        Checkbutton(self, text=text, variable=variable).grid(row=0, column=0)
        self.checkbutton = Checkbutton

    def state(self):
        return self.var.get()