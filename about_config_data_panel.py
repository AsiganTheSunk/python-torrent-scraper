from tkinter import *
from button_box import ButtonBox

class AboutConfigDataPanel(Frame):
    def __init__(self, master, row, column, width=275, height=285, background='#ADD8E6'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.master = master
        self.on_create()

    def on_create(self):
        inner_border_frame3 = Frame(self, width=275, height=285, background='#ADD8E6')
        inner_border_frame3.grid(row=0, column=0)

