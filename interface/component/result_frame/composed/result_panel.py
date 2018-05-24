from tkinter import *
from .data_panel import DataPanel
from .list_panel import ListPanel

class ResultPanel(Frame):
    def __init__(self, master, row, column, cmmndClose, background='#ADD8E6'):
        Frame.__init__(self, master, background=background)
        self.grid(row=row, column=column)
        self.list_panel = None
        self.data_panel = None
        self.cmmndClose = cmmndClose
        self.master = master

        self.main_theme = '#ADD8E6'
        self.highlight_theme = '#91B6CE'

        self.on_create()

    def on_create(self):
        left_border_frame = Frame(self, width=10, height=275, background= self.main_theme)
        left_border_frame.grid(row=0, column=0)

        #ListBox

        inner_border_frame = Frame(self, width=11, height=275, background= self.main_theme)
        inner_border_frame.grid(row=0, column=2)

        data_panel = DataPanel(self, 0, 3, self.cmmndClose)
        self.data_panel = data_panel

        right_border_frame = Frame(self, width=6, height=275, background= self.main_theme)
        right_border_frame.grid(row=0, column=4)

        #Moved Here!
        list_panel = ListPanel(self, 0, 1, data_panel.data_box, data_panel.display_box, data_panel.button_box)
        self.list_panel = list_panel


