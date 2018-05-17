from tkinter import *
from .data_panel import DataPanel
from .list_panel import ListPanel

class ResultPanel(Frame):
    def __init__(self, master, row, column, root, width=275, height=590, background='#ADD8E6'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.list_panel = None
        self.data_panel = None
        self.root = root
        self.master = master

        self.on_create()

    def on_create(self):
        left_border_frame = Frame(self, width=10, height=275, background='#ADD8E6')
        left_border_frame.grid(row=0, column=0)

        inner_border_frame = Frame(self, width=6, height=275, background='#ADD8E6')
        inner_border_frame.grid(row=0, column=2)

        data_panel = DataPanel(self, 0, 3, self.root)
        self.data_panel = data_panel

        list_panel = ListPanel(self, 0, 1, data_panel.data_box, data_panel.display_box, data_panel.button_box)
        self.list_panel = list_panel

        right_border_frame = Frame(self, width=5, height=275, background='#ADD8E6')
        right_border_frame.grid(row=0, column=4)
