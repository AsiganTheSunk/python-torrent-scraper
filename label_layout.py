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


# INFORMATIONAL FRAME: PRIMER CUADRANTE
info_frame = Frame(root, width=590, height=400, background='#DCDCDC')
info_frame.grid(row=0, column=0)

status_frame = Frame(info_frame, width=590, height=25, background='#ADD8E6')
status_frame.grid(row=0, column=0)

description_frame = Frame(info_frame, width=590, height=375, background='#DCDCDC')
description_frame.grid(row=1, column=0)

# POSTER + FLAGS FRAME: SEGUNDO CUADRANTE
poster_frame = Frame(root, width=210, height=400, background='#DCDCDC')
poster_frame.grid(row=0, column=1)

# status bar
status_frame0 = Frame(poster_frame, width=214, height=25, background='#ADD8E6')
status_frame0.grid(row=0, column=1)

# setting up the frame for the poster image
poster_image_frame = Frame(poster_frame, width=200, height=375, background='gray')
poster_image_frame.grid(row=1, column=1)

# flag section
flag_frame = Frame(poster_frame, width=210, height=100, background='#DCDCDC')
flag_frame.grid(row=2, column=1)

# flag section
fst_flag_frame = Frame(flag_frame, width=204, height=50, background='pink')
fst_flag_frame.grid(row=0, column=0)

fst_flag_frame = Frame(flag_frame, width=204, height=50, background='yellow')
fst_flag_frame.grid(row=1, column=0)

# fill up section
side_flag_frame = Frame(flag_frame, width=10, height=102, background='#ADD8E6')
side_flag_frame.grid(row=0, column=1, rowspan=2)

push_image = Frame(poster_image_frame, width=10, height=274, background='#ADD8E6')
push_image.grid(row=0, column=1)

# setting up the sub frame for the poster
poster_image = Frame(poster_image_frame, width=200, height=270, background='#848482')
poster_image.grid(row=0, column=0)

# loading the image for the poster
aux = Image.open('./megalobox_placeholder.png')
poster = ImageTk.PhotoImage(aux)
poster_image.photo_poster = poster

poster_container = Label(poster_image , width=200, height=270, relief='solid')
poster_container.configure(borderwidth=0, highlightbackground='#848482', image=poster)
poster_container.grid(row=0, column=0, padx=2, pady=2)

# listbox frame
listbox_frame = Frame(root, width=590, height=180, background='#ADD8E6')
listbox_frame.grid(row=1, column=0)

lista = ['[HorribleSubs] Megalobox Episode - 01 1080p.mkv','[HorribleSubs] Megalobox Episode - 01 720.mkv','[HorribleSubs] Megalobox Episode - 01 480p.mkv']
list_box = SimpleListBox(listbox_frame, lista)
list_box.configure(borderwidth=1, highlightbackground='white', bg='#DCDCDC', relief='solid')
list_box.grid(row=0, column=0, padx=2, pady=2)

# botones de descarga y salir
# listbox frame
data_panel_frame = Frame(root, width=214, height=184, background='#A4DDED')
data_panel_frame.grid(row=1, column=1)

# data panel
data_panel = Frame(data_panel_frame, width=204, height=159)
data_panel.grid(row=0, column=0)

# fill up section
side_data_panel = Frame(data_panel_frame, width=10, height=159, background='#ADD8E6')
side_data_panel.grid(row=0, column=1)

side0_data_panel = Frame(data_panel_frame, width=10, height=25, background='#ADD8E6')
side0_data_panel.grid(row=1, column=1)

data_panel = Frame(data_panel_frame, width=204, height=159, background='blue')
data_panel.grid(row=0, column=0)

panedwindow = PanedWindow(data_panel,width=200, height=2, borderwidth=2)
panedwindow.grid(row=0, column=0)

button_panel = Frame(data_panel_frame, width=204, height=25, background='#ADD8E6')
button_panel.grid(row=1, column=0)

B = Button(button_panel, text='DOWNLOAD', width=15,  height=2, relief='groove', borderwidth=2)
B.grid(row=0, column=0, padx='1')

B1 = Button(button_panel, text='EXIT', width=15,  height=2, relief='groove', borderwidth=2)
B1.grid(row=0, column=1, padx='1')


# status bar
lower_status_bar = Frame(root, width=804, height=40, background='#ADD8E6')
lower_status_bar.grid(row=2, column=0, columnspan=2)

# label3a = Label(frame3, text='Torrent Info : magnet:-------------------------------------------------------------------------------------------------------------------------------------')
# label3a.grid(row=0, column=0, columnspan=2)

# cv0 = Canvas(top, width=64, height=50, relief='flat')
# cv0.configure(borderwidth=0)
# cv0.grid(row=1, column=1)
# cv0.create_image(64 * .53, 48 * .55, image=qphoto, anchor='center')
#
# qicon0 = Image.open('./display_flags/2.png')
# qphoto0 = ImageTk.PhotoImage(qicon0)
# top.qphoto0 = qphoto0
#
# cv1 = Label(top, width=64, height=50, relief='flat')
# cv1.configure(borderwidth=0, image=qphoto0)
# cv1.grid(row=1, column=5)
# # cv1.create_image(64*.53, 48*.55, , anchor='center')
#
#
# cv2 = Label(top, width=64, height=50, relief='flat')
# cv2.configure(borderwidth=0, image=qphoto0)
# cv2.grid(row=1, column=0)

root.mainloop()
