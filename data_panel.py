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
from list_box import ListBox
from data_box import DataBox
from display_box import DisplayBox
from button_box import ButtonBox
class DataPanel(Frame):
    def __init__(self, master, row, column, width=275, height=300, background='#ADD8E6'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.on_create()

    def on_create(self):
        inner_border_frame3 = Frame(self, width=275, height=3, background='#ADD8E6')
        inner_border_frame3.grid(row=0, column=0)

        display_box = DisplayBox(self, 1, 0)

        inner_border_frame2 = Frame(self, width=275, height=18, background='#ADD8E6')
        inner_border_frame2.grid(row=2, column=0)

        data_box = DataBox(self, 3, 0)

        inner_border_frame1 = Frame(self, width=275, height=17, background='#ADD8E6')
        inner_border_frame1.grid(row=4, column=0)

        button_box = ButtonBox(self, 5, 0)

        inner_border_frame0 = Frame(self, width=275, height=3, background='#ADD8E6')
        inner_border_frame0.grid(row=6, column=0)