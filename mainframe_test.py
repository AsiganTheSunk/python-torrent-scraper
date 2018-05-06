from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import os
from torrentscraper import scraper_engine as se
from torrentscraper.datastruct.websearch_instance import WebSearchInstance
from simple_option_menu import SimpleOptionMenu
from simple_list_box import SimpleListBox

def label(row, column, text):
    L = Label(root, text=text, anchor='w')
    L.grid(row=row,column=column,sticky="nw",pady=2,padx=3)

def button(root, row, column, text, command):
    B = Button(root, text=text, command=command, height=2, width=15, relief='groove', borderwidth=2, bg='#DCDCDC', highlightbackground='#848482')
    B.grid(row=row, column=column, sticky="es", pady=2, padx=2)

def entry(root, row, column, insert="", show="", width=32):
    E = Entry(root, width=width)
    E.insert(0, insert)
    E.config(show=show)
    E.grid(row=row, column=column, padx=2, pady=2)
    return E

def scrap():
    pass

root = Tk()
root.geometry("800x300")
root.style = ttk.Style()
root.style.theme_use("clam")
root.iconbitmap('./cat-grumpy.ico')
root.title("python-torrent-scraper-v0.3.2")

upper_fill_frame = Frame(root, width=804, height=25, background='#ADD8E6')
upper_fill_frame.grid(row=0, column=0)

input_frame = Frame(root, width=800, height=250, background='#ADD8E6')
input_frame.grid(row=1, column=0)

left_fill_input_frame = Frame(input_frame, width=10, height=235, background='#ADD8E6')
left_fill_input_frame.grid(row=0, column=0)

inner_left_fill_input_frame = Frame(input_frame, width=8, height=235, background='#ADD8E6')
inner_left_fill_input_frame.grid(row=0, column=1)

input_box = Frame(input_frame, width=780, height=235, background='#F0F8FF')
input_box.grid(row=0, column=2)

inner_right_fill_frame = Frame(input_frame, width=9, height=235, background='#ADD8E6')
inner_right_fill_frame.grid(row=0, column=3)

right_fill_input_frame = Frame(input_frame, width=10, height=235, background='#ADD8E6')
right_fill_input_frame.grid(row=0, column=4)

lower_fill_frame = Frame(root, width=804, height=50, background='#ADD8E6')
lower_fill_frame.grid(row=2, column=0)

push_to_left_frame = Frame(lower_fill_frame, width=589, height=40, background='#ADD8E6')
push_to_left_frame.grid(row=0, column=0)

button_box = Frame(lower_fill_frame, width=214, height=50, background='#ADD8E6')
button_box.grid(row=0, column=1)

push_to_rigth_frame = Frame(lower_fill_frame, width= 7, height=40, background='#ADD8E6')
push_to_rigth_frame.grid(row=0, column=2)

header = {'[HorribleSubs]':'HorribleSubs'}
popupMenu0 = SimpleOptionMenu(input_box, '[Header]', *header)
popupMenu0.grid(row=0, column=0, sticky='W', padx=2, pady=2)

var0 = entry(root=input_box, row=0, column=1,  insert='Rick & Morty',width= 40)
var1 = entry(root=input_box, row=0, column=2,  insert='Year', width=8)
var2 = entry(root=input_box, row=0, column=3,  insert='03', width=4)
var3 = entry(root=input_box, row=0, column=4,  insert='08', width=4)

quality = {'1080p':'1080p', '720p':'720p', 'HDTV':'HDTV', 'WEBRip': 'WEBRip'}
popupMenu = SimpleOptionMenu(input_box, '[Quality]', *quality)
popupMenu.grid(row=0, column=5, sticky='W', padx=2, pady=2)

search_type = {'SHOW':'SHOW', 'MOVIE':'MOVIE', 'ANIME':'ANIME'}
popupMenu1 = SimpleOptionMenu(input_box, '[Search Type]', *search_type)
popupMenu1.grid(row=0, column=6, sticky='W', padx=2, pady=2)

button(button_box, 0, 0, 'Scrap', scrap)
button(button_box, 0, 1, 'Quit', root.quit)
root.mainloop()