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

class DisplayBox(Frame):
    def __init__(self, master, row, column, width=275, height=300, background='red'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.on_create()

    def on_create(self):
        flag_data_frame = Frame(self, width=200, height=50)
        flag_data_frame.grid(row=0, column=0)

        # loading the image for the poster
        aux0 = Image.open('./48px/1080.png')
        # aux0 = aux0.resize((48, 48), Image.ANTIALIAS)
        quality = ImageTk.PhotoImage(aux0)
        flag_data_frame.quality = quality

        aux1 = Image.open('./48px/2.png')
        acodec = ImageTk.PhotoImage(aux1)
        flag_data_frame.acodec = acodec

        aux2 = Image.open('./48px/Aac.png')
        # aux2 = aux2.resize((48, 48), Image.ANTIALIAS)
        acodec0 = ImageTk.PhotoImage(aux2)
        flag_data_frame.acodec0 = acodec0

        aux3 = Image.open('./48px/16-9.png')
        # aux2 = aux2.resize((48, 48), Image.ANTIALIAS)
        vcodec = ImageTk.PhotoImage(aux3)
        flag_data_frame.vcodec = vcodec

        rightborder = Frame(flag_data_frame, width=35, height=48, background='#ADD8E6')
        rightborder.grid(row=0, column=0)

        rightborder = Frame(flag_data_frame, width=3, height=48, background='#F0F8FF')
        rightborder.grid(row=0, column=1)

        qlabel = Label(flag_data_frame, width=60, height=48, background='#ADD8E6')
        qlabel.configure(borderwidth=0, image=quality)
        qlabel.grid(row=0, column=2)

        rightborder0 = Frame(flag_data_frame, width=3, height=48, background='#F0F8FF')
        rightborder0.grid(row=0, column=3)

        qlabel = Label(flag_data_frame, width=60, height=48)
        qlabel.configure(borderwidth=0, image=vcodec)
        qlabel.grid(row=0, column=4)

        rightborder1 = Frame(flag_data_frame, width=3, height=48, background='#F0F8FF')
        rightborder1.grid(row=0, column=5)

        qlabel = Label(flag_data_frame, width=60, height=48)
        qlabel.configure(borderwidth=0, image=acodec)
        qlabel.grid(row=0, column=6)

        rightborder2 = Frame(flag_data_frame, width=3, height=48, background='#F0F8FF')
        rightborder2.grid(row=0, column=7)

        qlabel = Label(flag_data_frame, width=60, height=48)
        qlabel.configure(borderwidth=0, image= acodec0)
        qlabel.grid(row=0, column=8)

        leftborder = Frame(flag_data_frame, width=3, height=48, background='#F0F8FF')
        leftborder.grid(row=0, column=9)

        qlabel = Label(flag_data_frame, width=60, height=48)
        qlabel.configure(borderwidth=0, image=acodec)
        qlabel.grid(row=0, column=10)

        leftborder = Frame(flag_data_frame, width=3, height=48, background='#F0F8FF')
        leftborder.grid(row=0, column=11)