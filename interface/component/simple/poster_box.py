from tkinter import *
from PIL import ImageTk, Image
from os import listdir
from os.path import isfile, join
import threading
from google_images_download import google_images_download

class SimplePosterBox(Frame):
    def __init__(self, master, row, column, width=200, height=275, background='grey'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.poster_container = None
        self.image_path = ''

        self.on_create()

    def on_create(self):
        aux = Image.open('./interface/resources/placeholders/poster_placeholder.png')
        poster_image = ImageTk.PhotoImage(aux)
        self.poster_image = poster_image

        poster_container = Label(self, width=198, height=271, relief='solid')
        poster_container.configure(borderwidth=0, highlightbackground='#848482', image=poster_image)
        poster_container.grid(row=0, column=1, padx=2, pady=2)
        self.poster_container = poster_container
