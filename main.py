#!/usr/bin/env python

from tkinter import *
from tkinter import ttk
from simple_info_panel import InfoPanel
from ResultPanel import ResultPanel
from display_box import DisplayBox
from data_panel import DataPanel
from data_box import DataBox
from list_box import ListBox
from simple_poster_box import SimplePosterBox
from imdbfilmextension import IMDbExtension
from PIL import Image
from google_images_download import google_images_download
from PIL import ImageTk, Image
from os import listdir
from os.path import isfile, join
import threading
from logging import DEBUG, INFO, WARNING
import logging
import traceback
from torrentscraper.webscrapers.utils.magnet_builder import MagnetBuilder
from torrentscraper import scraper_engine as se
from torrentscraper.datastruct.websearch_instance import WebSearchInstance
# Import Custom Logger
from torrentscraper.utils.custom_logger import CustomLogger

logger = CustomLogger(name=__name__, level=INFO)
formatter = logging.Formatter(fmt='%(asctime)s -  [%(levelname)s]: %(message)s',
                              datefmt='%m/%d/%Y %I:%M:%S %p')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(INFO)

logger.addHandler(console_handler)


class SearchResultThreadInfo(threading.Thread):
    def __init__(self, threadID, name, websearch):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.websearch = websearch
        self.dataframe = ''

    def run(self):
        print ("SearchResultThreadInfo" + self.name)
        self.dataframe = self.search()
        print ("SearchResultThreadInfo" + self.name)

    def search(self):
        scraper_engine = se.ScraperEngine()
        p2p_instance_list = scraper_engine.search(self.websearch)
        dataframe = scraper_engine.create_magnet_dataframe(p2p_instance_list)
        dataframe = scraper_engine.unique_magnet_dataframe(dataframe)
        return scraper_engine.get_dataframe(dataframe, 15)

class PosterThreadImage(threading.Thread):
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


class DescriptionThreadInfo(threading.Thread):
    def __init__(self, threadID, name, name_search):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.name_search = name_search
        self.info = ''

    def run(self):
        print ("Starting DescriptionThreadInfo" + self.name)
        self.info = self.get_data()
        print ("Exiting DescriptionThreadInfo" + self.name)

    def get_data(self):
        imdb_extension = IMDbExtension()
        movie_index = imdb_extension.get_movie_index(self.name_search)
        year = imdb_extension.get_year(movie_index)
        runtime = imdb_extension.get_runtime(movie_index)
        actors = imdb_extension.get_actors(movie_index)
        director = imdb_extension.get_director(movie_index)
        plot_summary = imdb_extension.get_plot_summary(movie_index)
        info = '[Title]: {0}\n' \
               '[Year]: {1}\n' \
               '----------------------------------------------------------------------------------------' \
               '[Runtime]: {2} Min\n' \
               '[Director]: {3}\n' \
               '----------------------------------------------------------------------------------------' \
               '[Actors]:\n{4}\n' \
               '----------------------------------------------------------------------------------------' \
               '[Plot Summary]:\n{5}\n'.format(
            self.name_search, year, runtime, director, actors, plot_summary)
        return info

def update_poster(poster_thread, info_panel):
    poster_thread.join()

    image_path = poster_thread.image_path[1]
    aux = Image.open(image_path)
    poster_image = ImageTk.PhotoImage(aux)
    info_panel.poster_box.poster_image = poster_image
    info_panel.poster_box.poster_container.configure(borderwidth=0, highlightbackground='#848482', image=poster_image)

def update_description(description_thread, info_panel):
    description_thread.join()
    info = description_thread.info
    info_panel.info_box.set_info_text(info)

def update_data_box(search_result_thread, result_panel):
    index_selection = result_panel.list_panel.list_box.result_box.get_selection()
    if index_selection != 'empty':
        dataframe = search_result_thread.dataframe
        index_selection = result_panel.list_panel.list_box.result_box.get_selection()
        print('INDEX:', str(index_selection))
        magnet = dataframe[['name'] == index_selection]['magnet']
        size = dataframe[['name'] == index_selection]['size']
        seed = dataframe[['name'] == index_selection]['seed']
        leech = dataframe[['name'] == index_selection]['leech']
        language = ''

        mbuilder = MagnetBuilder(logger)
        magnet_instance = mbuilder.parse_from_magnet(magnet, size, seed, leech)

        quote = '[Hash]: {0}' \
                '\n-------------------------------------------------' \
                '\n[Size]: {1} MB' \
                '\n[Seed]: {2}' \
                '\n[Leech]: {3}' \
                '\n-------------------------------------------------' \
                '\n[Language]:( - )' \
                '\n-------------------------------------------------' \
                '\n[AnnounceList]:' \
                '\n\t[HTTPS]: {4}\n\t[HTTP]: {5}\n\t[UDP]: {6}'.format(magnet_instance['hash'],
                                                                       magnet_instance['size'],
                                                                       magnet_instance['seed'],
                                                                       magnet_instance['leech'],
                                                                       magnet_instance['announce_list']['https'],
                                                                       magnet_instance['announce_list']['http'],
                                                                       magnet_instance['announce_list']['udp'])
        print(quote)
        result_panel.data_panel.data_box.data_box.set_data(quote)



def update_result_search(search_result_thread, result_panel):
    search_result_thread.join()
    dataframe =  search_result_thread.dataframe
    result_panel.list_panel.list_box.result_box.dataframe = dataframe
    lista = []
    for index in dataframe.index.tolist():
        dn = dataframe.iloc[int(index)]['name']
        _hash = dataframe.iloc[int(index)]['hash']
        magnet = dataframe.iloc[int(index)]['magnet']
        size = dataframe.iloc[int(index)]['size']
        seed = dataframe.iloc[int(index)]['seed']
        leech = dataframe.iloc[int(index)]['leech']
        ratio = dataframe.iloc[int(index)]['ratio']
        formato = '[ {0} ]'.format(dn)
        lista.append(formato)

    result_panel.list_panel.list_box.result_box.set_item_list(lista)


def main():
    poster_thread = PosterThreadImage(1, 'Poster Thread', 'Westworld')
    poster_thread.start()

    description_thread = DescriptionThreadInfo(2, 'Description Thread', 'Westworld')
    description_thread.start()

    websearch = WebSearchInstance('Westworld', '', '02', '01', '1080p', '', 'SHOW')
    search_result_thread = SearchResultThreadInfo(3, 'Search Result Thread', websearch)
    search_result_thread.start()

    root = Tk()
    root.geometry("865x625")
    root.style = ttk.Style()
    root.style.theme_use("clam")
    root.iconbitmap('./cat-grumpy.ico')
    root.title("python-torrent-scraper-v0.3.2")
    root.resizable(width=False, height=False)

    upper_border_frame = Frame(root, width=864, height=11, background='#ADD8E6')
    upper_border_frame.grid(row=0, column=0)

    info_panel = InfoPanel(root, 1, 0)

    middle_border_frame = Frame(root, width=864, height=5, background='#ADD8E6')
    middle_border_frame.grid(row=2, column=0)

    result_panel = ResultPanel(root, 3, 0)

    lower_border_frame = Frame(root, width=864, height=14, background='#ADD8E6')
    lower_border_frame.grid(row=4, column=0)

    # poster_thread = myThread(1, "Thread-1", 'Rick & Morty')
    # poster_thread.start()

    info_panel.update_idletasks()  # Actualizate FRAME!
    info_panel.after(500, update_poster(poster_thread, info_panel)) # Se pone la actualizacion 200ms despues de pintar el frame por defecto?
    info_panel.after(500, update_description(description_thread, info_panel)) # Se pone la actualizacion 200ms despues de pintar el frame por defecto?
    result_panel.update_idletasks()  # Actualizate FRAME!
    result_panel.after(500, update_result_search(search_result_thread, result_panel)) # Se pone la actualizacion 200ms despues de pintar el frame por defecto?
    result_panel.after(500, update_data_box(search_result_thread, result_panel)) # Se pone la actualizacion 200ms despues de pintar el frame por defecto?
    root.mainloop()

if __name__ == '__main__':
    main()

# content = websearch(url= 'https://www.pogdesign.co.uk/cat/')
# dataframe = tvcs.TvCalendarScrapper().webscrapper(content=content.text)
# dataframe.to_csv('./montly_tvcalendar.csv', sep='\t', encoding='utf-8')
from button_box import ButtonBox
