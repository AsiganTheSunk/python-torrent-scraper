from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import os
from torrentscraper import scraper_engine as se
from torrentscraper.datastruct.websearch_instance import WebSearchInstance
from simple_option_menu import SimpleOptionMenu
from simple_list_box import SimpleListBox
from imdbfilmextension import IMDbExtension
from simple_poster_box import SimplePosterBox
from simple_info_box import SimpleInfoBox

class ListBox(Frame):
    def __init__(self, master, row, column, width=275, height=590, background='#ADD8E6'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.on_create()

    def on_create(self):
        list_box = Frame(self, width=590, height=275, background='#F0F8FF')
        list_box.grid(row=0, column=1)

        left_border = Frame(list_box, width=2, height=275, background='#ADD8E6')
        left_border.grid(row=0, column=0)

        left_border = Frame(list_box, width=1, height=275, background='#F0F8FF')
        left_border.grid(row=0, column=1)

        lista = ['[HorribleSubs] Megalobox Episode - 01 1080p.mkv','[HorribleSubs] Megalobox Episode - 01 720.mkv','[HorribleSubs] Megalobox Episode - 01 480p.mkv']
        result_box = SimpleListBox(list_box, lista)
        result_box.configure(borderwidth=1, highlightbackground='white', bg='#DCDCDC', relief='groove')
        result_box.grid(row=0, column=2)

        right_border = Frame(list_box, width=3, height=275, background='#F0F8FF')
        right_border.grid(row=0, column=3)