# Import Interface Libraries
from tkinter import *

# Import Custom Interface Components
from interface.component.result_frame.simple.list_box import SimpleListBox

class ListBox(Frame):
    def __init__(self, master,  row, column, databox, displaybox, buttonbox, width=275, height=590, background='#ADD8E6'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.result_box = None
        self.databox = databox
        self.displaybox = displaybox
        self.buttonbox = buttonbox
        self.master = master
        self.on_create()

    def on_create(self):
        list_box = Frame(self, width=590, height=275, background='#F0F8FF')
        list_box.grid(row=0, column=1)

        left_border = Frame(list_box, width=2, height=275, background='#ADD8E6')
        left_border.grid(row=0, column=0)

        left_border = Frame(list_box, width=2, height=275, background='#F0F8FF')
        left_border.grid(row=0, column=1)

        result_box = SimpleListBox(list_box, [], self.databox, self.displaybox, self.buttonbox)
        result_box.configure(borderwidth=1, highlightbackground='white', bg='#DCDCDC', relief='groove')
        result_box.grid(row=0, column=2)
        self.result_box = result_box

        right_border = Frame(list_box, width=2, height=275, background='#F0F8FF')
        right_border.grid(row=0, column=3)