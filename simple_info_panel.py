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

class InfoPanel(Frame):
    def __init__(self, master, row, column, width=275, height=590, background='#ADD8E6'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.on_create()

    def on_create(self):
        left_border_frame = Frame(self, width=10, height=275, background='#ADD8E6')
        left_border_frame.grid(row=0, column=0)

        info_box = SimpleInfoBox(self, 0, 1)
        poster_box = SimplePosterBox(self, 0, 2)

        right_border_frame = Frame(self, width=5, height=275, background='#ADD8E6')
        right_border_frame.grid(row=0, column=3)



    def on_load(self):
        pass