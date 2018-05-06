#!/usr/bin/python3
# -*- coding: utf-8 -*-

from imdbfilmextension import IMDbExtension
from tkinter import *
from tkinter import ttk
from simple_option_menu import SimpleOptionMenu
from simple_list_box import SimpleListBox
from PIL import ImageTk, Image

from torrentscraper import scraper_engine as se
from torrentscraper.datastruct.websearch_instance import WebSearchInstance

root = Tk()
root.geometry("800x600")
root.configure(bg='#DCDCDC')
root.iconbitmap('./cat-grumpy.ico')
root.title("python-torrent-scraper-v0.3.2")

# DEFINICION DE FRAMES PRINCIPALES
# Fill Upper Frame
fill_upper_frame = Frame(root, width=806, height=25, background='#ADD8E6')
fill_upper_frame.grid(row=0, column=0)

info_frame = Frame(root, width=800, height=275, background='#ADD8E6')
info_frame.grid(row=1, column=0)

info_fill_left_frame = Frame(info_frame, width=16, height=275, background='#ADD8E6')
info_fill_left_frame.grid(row=1, column=0)

description_frame = Frame(info_frame, width=590, height=275, background='#F0F8FF')
description_frame.grid(row=1, column=1)

T = Text(description_frame, bg='#DCDCDC',width=79, height=17)
T.grid(row=0,column=0)
T.configure(relief='groove')

S = Scrollbar(description_frame)
S.grid(row=0,column=1, sticky='nw')
S.configure(relief='flat')
#
S.config(command=T.yview)
T.config(yscrollcommand=S.set)

imdb_extension = IMDbExtension()
movie_index = imdb_extension.get_movie_index('Rick & Morty')
year = imdb_extension.get_year(movie_index)
runtime = imdb_extension.get_runtime(movie_index)
actors = imdb_extension.get_actors(movie_index)
director = imdb_extension.get_director(movie_index)
plot_summary = imdb_extension.get_plot_summary(movie_index)

# info = 'INFO - LOADING'

info = '[Title]: {0}\n[Year]: {1}\n[Runtime]: {2}\n[Director]: {3}\n[Actors]: {4}\n[Plot Summary]:\n{5}'.format(
    'Rick & Morty', year, runtime, director, actors, plot_summary)

quote = info
T.insert(END, quote)
T.config(state=DISABLED)

info_fill_inner_frame = Frame(info_frame, width=7, height=275, background='#ADD8E6')
info_fill_inner_frame.grid(row=1, column=2)

poster_frame = Frame(info_frame, width=200, height=275, background='gray')
poster_frame.grid(row=1, column=3)

# loading the image for the poster
aux = Image.open('./rickmortyposter.png')
#aux = Image.open('./megalobox_placeholder.png')
poster = ImageTk.PhotoImage(aux)
poster_frame.photo_poster = poster

poster_container = Label(poster_frame , width=198, height=270, relief='solid')
poster_container.configure(borderwidth=0, highlightbackground='#848482', image=poster)
poster_container.grid(row=0, column=0, padx=2, pady=2)

info_fill_right_frame = Frame(info_frame, width=10, height=275, background='#ADD8E6')
info_fill_right_frame.grid(row=1, column=4)

fill_horizontal_inner_frame = Frame(root, width=806, height=10, background='#ADD8E6')
fill_horizontal_inner_frame.grid(row=2, column=0)

result_frame = info_frame = Frame(root, width=800, height=275, background="bisque")
result_frame.grid(row=3, column=0)

fill_leftouter_frame = Frame(result_frame, width=16, height=285, background='#ADD8E6')
fill_leftouter_frame.grid(row=0, column=0)

list_frame = Frame(result_frame, width=590, height=285, background='#ADD8E6')
list_frame.grid(row=0, column=1)

websearch = WebSearchInstance('Rick & Morty', '', '03', '09', '1080p', '', 'SHOW')
scraper_engine = se.ScraperEngine()
p2p_instance_list = scraper_engine.search(websearch)
dataframe = scraper_engine.create_magnet_dataframe(p2p_instance_list)
dataframe = scraper_engine.unique_magnet_dataframe(dataframe)
dataframe = scraper_engine.get_dataframe(dataframe, 10)
magnet = ''
lista = []
for index in dataframe.index.tolist():
    dn = dataframe.iloc[int(index)]['name']
    _hash = dataframe.iloc[int(index)]['hash']
    magnet = dataframe.iloc[int(index)]['magnet']
    size = dataframe.iloc[int(index)]['size']
    seed = dataframe.iloc[int(index)]['seed']
    leech = dataframe.iloc[int(index)]['leech']
    ratio = dataframe.iloc[int(index)]['ratio']
    formato = '{0:40}\t{1:>4}/{2:4}'.format(dn, str(seed), str(leech))
    lista.append(formato)

# lista = ['[HorribleSubs] Megalobox Episode - 01 1080p.mkv','[HorribleSubs] Megalobox Episode - 01 720.mkv','[HorribleSubs] Megalobox Episode - 01 480p.mkv']
list_box = SimpleListBox(list_frame, lista)
list_box.configure(borderwidth=1, highlightbackground='white', bg='#DCDCDC', relief='groove')
list_box.grid(row=0, column=0)

status_frame = Frame(list_frame, width=574, height=6, background='#ADD8E6')
status_frame.grid(row=1, column=0)

status_frame = Frame(list_frame, width=574, height=22, background='#F0F8FF')
status_frame.grid(row=2, column=0)

fill_vleft_inner_frame = Frame(result_frame, width=7, height=285, background='#ADD8E6')
fill_vleft_inner_frame.grid(row=0, column=2)
#
data_frame = Frame(result_frame, width=200, height=285, background='blue')
data_frame.grid(row=0, column=3)

flag_data_frame = Frame(data_frame, width=200, height=50, background='#F0F8FF')
flag_data_frame.grid(row=0, column=0)

# loading the image for the poster
aux0 = Image.open('./1080p-48.png')
#aux = Image.open('./megalobox_placeholder.png')
quality = ImageTk.PhotoImage(aux0)
flag_data_frame.quality = quality

qlabel = Label(flag_data_frame, width=48, height=48)
qlabel.configure(borderwidth=0, image=quality)
qlabel.grid(row=0, column=0, padx='1', pady='1')

qlabel = Label(flag_data_frame, width=48, height=48)
qlabel.configure(borderwidth=0, image=quality)
qlabel.grid(row=0, column=1, padx='1', pady='1')

qlabel = Label(flag_data_frame, width=48, height=48)
qlabel.configure(borderwidth=0, image=quality)
qlabel.grid(row=0, column=2, padx='1', pady='1')

qlabel = Label(flag_data_frame, width=48, height=48)
qlabel.configure(borderwidth=0, image=quality)
qlabel.grid(row=0, column=3, padx='1', pady='1')

inner_fill_data_frame = Frame(data_frame, width=200, height=10, background='#ADD8E6')
inner_fill_data_frame.grid(row=1, column=0)

info_data_frame = Frame(data_frame, width=200, height=185, background='#F0F8FF')
info_data_frame.grid(row=2, column=0)

T2 = Text(info_data_frame, bg='#DCDCDC',width=28, height=12)
T2.grid(row=0,column=0)
T2.configure(relief='groove')
quote = '[Hash]: 33e9fe44da218113258d5d2748a3378f18cfe0bb\n[Size]: 881 MB'
T2.insert(END, quote)
T2.config(state=DISABLED)

lower_fill_data_frame = Frame(data_frame, width=200, height=5, background='#ADD8E6')
lower_fill_data_frame.grid(row=3, column=0)

button_frame = Frame(data_frame, width=200, height=40, background='green')
button_frame.grid(row=4, column=0)

B = Button(button_frame, text='DOWNLOAD', width=15,  height=2, relief='groove', borderwidth=2)
B.grid(row=0, column=0)

B1 = Button(button_frame, text='EXIT', width=15,  height=2, relief='groove', borderwidth=2)
B1.grid(row=0, column=1)
#
fill_vright_frame = Frame(result_frame, width=10, height=285, background='#ADD8E6')
fill_vright_frame.grid(row=0, column=4)

fill_lower_frame = Frame(root, width=806, height=15, background='#ADD8E6')
fill_lower_frame.grid(row=4, column=0)

root.resizable(width=False, height=False)
root.mainloop()
