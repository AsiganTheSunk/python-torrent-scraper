from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import os
from torrentscraper import scraper_engine as se
from torrentscraper.datastruct.websearch_instance import WebSearchInstance
from simple_option_menu import SimpleOptionMenu
from simple_list_box import SimpleListBox
from imdbfilmextension import IMDbExtension

class SimplePosterBox(Frame):
    def __init__(self, master, row, column, width=200, height=275, background='grey'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.on_create()

    def on_create(self):
        left_border_frame = Frame(self, width=5, height=275, background='#ADD8E6')
        left_border_frame.grid(row=0, column=0)

        # right_border_frame = Frame(self, width=5, height=275, background='#ADD8E6')
        # right_border_frame.grid(row=0, column=2)

        # loading the image for the poster
        aux = Image.open('./rickmortyposter.png')
        poster_image = ImageTk.PhotoImage(aux)
        self.poster_image = poster_image

        poster_container = Label(self, width=198, height=271, relief='solid')
        poster_container.configure(borderwidth=0, highlightbackground='#848482', image=poster_image)
        poster_container.grid(row=0, column=1, padx=2, pady=2)

    def on_load(self):
        pass