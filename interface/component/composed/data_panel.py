from tkinter import *
from interface.component.simple.data_box import SimpleDataBox
from interface.component.composed.display_box import DisplayBox
from interface.component.composed.button_box import ButtonBox

class DataPanel(Frame):
    def __init__(self, master, row, column, width=275, height=300, background='#ADD8E6'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.display_box = None
        self.data_box = None
        self.button_box = None
        self.master = master
        self.on_create()

    def on_create(self):
        inner_border_frame3 = Frame(self, width=275, height=3, background='#ADD8E6')
        inner_border_frame3.grid(row=0, column=0)

        display_box = DisplayBox(self, 1, 0)
        self.display_box = display_box

        inner_border_frame2 = Frame(self, width=275, height=18, background='#ADD8E6')
        inner_border_frame2.grid(row=2, column=0)

        data_box = SimpleDataBox(self, 3, 0)
        self.data_box = data_box

        inner_border_frame1 = Frame(self, width=275, height=17, background='#ADD8E6')
        inner_border_frame1.grid(row=4, column=0)

        button_box = ButtonBox(self, 5, 0)
        self.button_box = button_box

        inner_border_frame0 = Frame(self, width=275, height=3, background='#ADD8E6')
        inner_border_frame0.grid(row=6, column=0)