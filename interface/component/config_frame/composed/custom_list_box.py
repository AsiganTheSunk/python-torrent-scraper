# Import Interface Libraries
from tkinter import *

# Import Custom Interface Components

from interface.component.config_frame.simple.vertical_list_box import SimpleVerticalListBox

class CustomListBox(Frame):
    def __init__(self, master, row, column, cmmndClose, background='#ADD8E6'):
        Frame.__init__(self, master, background=background)
        self.grid(row=row, column=column)

        self.main_theme = '#ADD8E6'
        self.highlight_theme = '#F0F8FF'
        self.choice_box = None
        self.cmmndClose = cmmndClose
        self.master = master
        self.right_block = None
        self.on_create()

    # Color Scheme Highlight #F0F8FF, Main Color #ADD8E6'
    def on_create(self):
        list_box = Frame(self, background=self.highlight_theme)
        list_box.grid(row=0, column=0)

        left_border0 = Frame(list_box, width=3, height=280, background= self.main_theme)
        left_border0.grid(row=0, column=0)

        left_border1 = Frame(list_box, width=2, height=280, background=self.highlight_theme)
        left_border1.grid(row=0, column=1)

        left_border2 = Frame(list_box, width=2, height=280, background=self.highlight_theme)
        left_border2.grid(row=0, column=3)

        left_border4 = Frame(list_box, width=3, height=280, background= self.main_theme)
        left_border4.grid(row=0, column=4)

        self.right_block = Frame(list_box, width=278, height=280, background= self.main_theme)
        self.right_block.grid(row=0, column=5)

        self.choice_box = SimpleVerticalListBox(list_box, [' [ General ]', ' [ ScraperEngine ]', ' [ Qbittorrent ]',  ' [ About ]'], self.right_block, self.cmmndClose)
        self.choice_box.configure(borderwidth=1, highlightbackground='white', bg='#DCDCDC', relief='groove')
        self.choice_box.grid(row=0, column=2)

        left_border4 = Frame(list_box, width=3, height=280, background= self.main_theme)
        left_border4.grid(row=0, column=6)