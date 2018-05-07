from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import os
from torrentscraper import scraper_engine as se
from torrentscraper.datastruct.websearch_instance import WebSearchInstance
from simple_option_menu import SimpleOptionMenu
from simple_list_box import SimpleListBox
from imdbfilmextension import IMDbExtension

class SimpleInfoBox(Frame):
    def __init__(self, master, row, column, width=275, height=590, background='#ADD8E6'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.on_create()

    def on_create(self):
        left_border_frame = Frame(self, width=2, height=262, background='#ADD8E6')
        left_border_frame.grid(row=0, column=0)

        info_box = Frame(self, width=590, height=275, background='#F0F8FF')
        info_box.grid(row=0, column=1)

        inner_info_box = Frame(info_box, width=590, height=275, background='#F0F8FF')
        inner_info_box.grid(row=0, column=0)

        upper_border_info_box = Frame(inner_info_box, width=620, height=2, background='#F0F8FF')
        upper_border_info_box.grid(row=0, column=0)

        info_text = Text(inner_info_box, bg='#DCDCDC', width=88, height=17)
        info_text.grid(row=1, column=0)

        lower_border_info_box = Frame(inner_info_box, width=619, height=2, background='#F0F8FF')
        lower_border_info_box.grid(row=2, column=0)

        scroll_bar = Scrollbar(inner_info_box)
        scroll_bar.grid(row=1, column=1, sticky='nw')

        scroll_bar.configure(relief='groove')
        info_text.configure(relief='flat')

        scroll_bar.config(command=info_text.yview)
        info_text.config(yscrollcommand=scroll_bar.set)

        quote = 'INFO - LOADING'
        info_text.insert(END, quote)
        info_text.config(state=DISABLED)

        lower_border_info_box = Frame(info_box, width=640, height=5, background='#ADD8E6')
        lower_border_info_box.grid(row=3, column=0)


    def on_load(self):
       imdb_extension = IMDbExtension()
       movie_index = imdb_extension.get_movie_index('Rick & Morty')
       year = imdb_extension.get_year(movie_index)
       runtime = imdb_extension.get_runtime(movie_index)
       actors = imdb_extension.get_actors(movie_index)
       director = imdb_extension.get_director(movie_index)
       plot_summary = imdb_extension.get_plot_summary(movie_index)

       info = '[Title]: {0}\n[Year]: {1}\n[Runtime]: {2}\n[Director]: {3}\n[Actors]: {4}\n[Plot Summary]:\n{5}'.format(
           'Rick & Morty', year, runtime, director, actors, plot_summary)
