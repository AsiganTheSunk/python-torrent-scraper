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
        self.loaded = False
        self.image_path = ''
        self.on_create()

        # self.poster_thread = myThread(1, "Thread-1", 'Rick & Morty')
        # self.poster_thread.start()
        # self.update_idletasks()  # Actualizate FRAME!
        # self.after(200, self.on_load()) # Se pone la actualizacion 200ms despues de pintar el frame por defecto?

    def on_create(self):
        # right_border_frame = Frame(self, width=5, height=275, background='#ADD8E6')
        # right_border_frame.grid(row=0, column=2)

        # loading the image for the poster
        aux = Image.open('./interface/placeholder/poster_placeholder.png')
        poster_image = ImageTk.PhotoImage(aux)
        self.poster_image = poster_image

        poster_container = Label(self, width=198, height=271, relief='solid')
        poster_container.configure(borderwidth=0, highlightbackground='#848482', image=poster_image)
        poster_container.grid(row=0, column=1, padx=2, pady=2)
        self.poster_container = poster_container

    def on_load(self):
        pass
        # self.poster_thread.join()
        # self.image_path = self.poster_thread.image_path[1]
        # if self.loaded is False:
        #     aux = Image.open(self.image_path)
        #     poster_image = ImageTk.PhotoImage(aux)
        #     self.poster_image = poster_image
        #     self.poster_container.configure(borderwidth=0, highlightbackground='#848482', image=poster_image)
        #
        #     self.loaded = True


class myThread (threading.Thread):
    def __init__(self, threadID, name, name_search):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.name_search = name_search
        self.image_path =''

    def run(self):
        print ("Starting " + self.name)
        self.image_path = self.get_movie_poster(self.name_search)
        print ("Exiting " + self.name)

    def get_movie_poster(self, name):
        response = google_images_download.googleimagesdownload()

        keywords = '{0} cover poster'.format(name)

        arguments = {"keywords": '{0} cover poster'.format(name), "limit": 1}
        d = response.download(arguments)
        onlyfiles = [f for f in listdir('./downloads/' + keywords + '/') if isfile(join('./downloads/' + keywords + '/', f))]

        img_temp = Image.open('./downloads/' + keywords + '/' + onlyfiles[0])
        img_temp = img_temp.resize((200, 272), Image.ANTIALIAS)
        img_temp.save(('./downloads/' + keywords + '/' + 'test-image-cover.png'), img_temp.format)
        return './downloads/' + keywords + '/' + onlyfiles[0], './downloads/' + keywords + '/' + 'test-image-cover.png'