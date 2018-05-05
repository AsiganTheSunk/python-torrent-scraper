#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from simple_option_menu import SimpleOptionMenu
from simple_list_box import SimpleListBox
from PIL import ImageTk, Image

root = Tk()
root.geometry("800x600")
root.configure(bg='#DCDCDC')
root.iconbitmap('./cat-grumpy.ico')
root.title("python-torrent-scraper-v0.3.2")

# DEFINICION DE FRAMES PRINCIPALES
# Fill Upper Frame
fill_upper_frame = Frame(root, width=806, height=25, background='#ADD8E6')
fill_upper_frame.grid(row=0, column=0)

info_frame = Frame(root, width=800, height=275, background='#A3C1AD')
info_frame.grid(row=1, column=0)

info_fill_left_frame = Frame(info_frame, width=16, height=275, background='#ADD8E6')
info_fill_left_frame.grid(row=1, column=0)

description_frame = Frame(info_frame, width=590, height=275, background='#F0F8FF')
description_frame.grid(row=1, column=1)

T = Text(description_frame, bg='#DCDCDC',width=79, height=18)
T.grid(row=0,column=0)
T.configure(relief='groove')

S = Scrollbar(description_frame,orient=VERTICAL)
S.grid(row=0,column=1, sticky='nw')

S.config(command=T.yview)
T.config(yscrollcommand=S.set)
quote = """HAMLET: To be, or not to be--that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune
Or to take arms against a sea of troubles
And by opposing end them. To die, to sleep--
No more--and by a sleep to say we end
The heartache, and the thousand natural shocks
That flesh is heir to. 'Tis a consummation
Devoutly to be wished.

HAMLET: To be, or not to be--that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune
Or to take arms against a sea of troubles
And by opposing end them. To die, to sleep--
No more--and by a sleep to say we end
The heartache, and the thousand natural shocks
That flesh is heir to. 'Tis a consummation
Devoutly to be wished.

HAMLET: To be, or not to be--that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune
Or to take arms against a sea of troubles
And by opposing end them. To die, to sleep--
No more--and by a sleep to say we end
The heartache, and the thousand natural shocks
That flesh is heir to. 'Tis a consummation
Devoutly to be wished.

HAMLET: To be, or not to be--that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune
Or to take arms against a sea of troubles
And by opposing end them. To die, to sleep--
No more--and by a sleep to say we end
The heartache, and the thousand natural shocks
That flesh is heir to. 'Tis a consummation
Devoutly to be wished.

HAMLET: To be, or not to be--that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune
Or to take arms against a sea of troubles
And by opposing end them. To die, to sleep--
No more--and by a sleep to say we end
The heartache, and the thousand natural shocks
That flesh is heir to. 'Tis a consummation
Devoutly to be wished."""
T.insert(END, quote)
T.config(state=DISABLED)

info_fill_inner_frame = Frame(info_frame, width=7, height=275, background='#ADD8E6')
info_fill_inner_frame.grid(row=1, column=2)

poster_frame = Frame(info_frame, width=200, height=275, background='gray')
poster_frame.grid(row=1, column=3)

# loading the image for the poster
aux = Image.open('./megalobox_placeholder.png')
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

lista = ['[HorribleSubs] Megalobox Episode - 01 1080p.mkv','[HorribleSubs] Megalobox Episode - 01 720.mkv','[HorribleSubs] Megalobox Episode - 01 480p.mkv']
list_box = SimpleListBox(result_frame, lista)
list_box.configure(borderwidth=1, highlightbackground='white', bg='#DCDCDC', relief='groove')
list_box.grid(row=0, column=1)

fill_vleft_inner_frame = Frame(result_frame, width=7, height=285, background='#ADD8E6')
fill_vleft_inner_frame.grid(row=0, column=2)
#
data_frame = Frame(result_frame, width=200, height=285, background='blue')
data_frame.grid(row=0, column=3)

info_data_frame = Frame(data_frame, width=200, height=250, background='#F0F8FF')
info_data_frame.grid(row=0, column=0)

button_frame = Frame(data_frame, width=200, height=40, background='green')
button_frame.grid(row=1, column=0)

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
