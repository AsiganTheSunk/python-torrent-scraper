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

class DataBox(Frame):
    def __init__(self, master, row, column, width=275, height=300, background='#F0F8FF'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.on_create()

    def on_create(self):

        upperborder = Frame(self, width=353, height=3, background='#F0F8FF')
        upperborder.grid(row=0, column=0)

        data_box = Frame(self, width=200, height=185, background='#F0F8FF')
        data_box.grid(row=1, column=0)

        T2 = Text(data_box, bg='#DCDCDC', width=49, height=12)
        T2.grid(row=0, column=0)
        T2.configure(relief='flat')
        quote = '[Hash]: 33e9fe44da218113258d5d2748a3378f18cfe0bb' \
                '\n-------------------------------------------------' \
                '\n[Size]: 881 MB' \
                '\n[Seed]: 15' \
                '\n[Leech]: 18' \
                '\n-------------------------------------------------' \
                '\n[Language]:(EN)' \
                '\n-------------------------------------------------' \
                '\n[AnnounceList]:' \
                '\n\t[HTTPS]: 12\n\t[HTTP]: 5\n\t[UDP]: 0'

        T2.insert(END, quote)
        T2.config(state=DISABLED)

        lowerborder = Frame(self, width=353, height=3, background='#F0F8FF')
        lowerborder.grid(row=2, column=0)
