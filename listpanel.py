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
class ListPanel(Frame):
    def __init__(self, master, row, column, width=275, height=590, background='#ADD8E6'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.on_create()

    def on_create(self):
        list_box = ListBox(self, 0, 0)
        lowerbordera = Frame(self, width=490, height=5, background='#ADD8E6')
        lowerbordera.grid(row=1, column=0)

        lowerborder0 = Frame(self, width=490, height=16, background='#ADD8E6')
        lowerborder0.grid(row=2, column=0)

        rightlowerborder = Frame(lowerborder0, width=2, height=16, background='#ADD8E6')
        rightlowerborder.grid(row=0, column=0)

        rightlowerborder0 = Frame(lowerborder0, width=488, height=16, background='#F0F8FF')
        rightlowerborder0.grid(row=0, column=1)

        lowerborder1 = Frame(self, width=490, height=5, background='#ADD8E6')
        lowerborder1.grid(row=3, column=0)