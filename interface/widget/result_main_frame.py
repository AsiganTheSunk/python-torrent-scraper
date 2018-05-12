#!/usr/bin/env python

from tkinter import *
from interface.widget.simple_info_panel import InfoPanel
from interface.widget.ResultPanel import ResultPanel
from PIL import ImageTk, Image
from logging import INFO
import logging

# Import Custom Logger
from torrentscraper.utils.custom_logger import CustomLogger
from torrentscraper.webscrapers.utils.magnet_builder import MagnetBuilder
from torrentscraper.datastruct.websearch_instance import WebSearchInstance

logger = CustomLogger(name=__name__, level=INFO)
formatter = logging.Formatter(fmt='%(asctime)s -  [%(levelname)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(INFO)
logger.addHandler(console_handler)

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


class ResultMainFrame(Frame):
    def __init__(self, master, row, column,background='#ADD8E6'):
        Frame.__init__(self, master, background=background)
        self.grid(row=row, column=column)
        self.name = self.__class__.__name__
        self.on_create()

    def on_create(self):
        # poster_thread = PosterThreadImage(1, 'Poster Thread', 'Westworld Season 2')
        # poster_thread.start()
        #
        # description_thread = DescriptionThreadInfo(2, 'Description Thread', 'Westworld')
        # description_thread.start()
        #
        # websearch = WebSearchInstance('Westworld', '', '02', '01', '1080p', '', 'SHOW')
        # search_result_thread = SearchResultThreadInfo(3, 'Search Result Thread', websearch)
        # search_result_thread.start()

        upper_border_frame = Frame(self, width=864, height=11, background='#ADD8E6')
        upper_border_frame.grid(row=0, column=0)

        info_panel = InfoPanel(self, 1, 0)

        middle_border_frame = Frame(self, width=864, height=5, background='#ADD8E6')
        middle_border_frame.grid(row=2, column=0)

        result_panel = ResultPanel(self, 3, 0)

        lower_border_frame = Frame(self, width=864, height=14, background='#ADD8E6')
        lower_border_frame.grid(row=4, column=0)

        # info_panel.update_idletasks()  # Actualizate FRAME!
        # info_panel.after(500, update_poster(poster_thread, info_panel)) # Se pone la actualizacion 200ms despues de pintar el frame por defecto?
        # info_panel.after(500, update_description(description_thread, info_panel)) # Se pone la actualizacion 200ms despues de pintar el frame por defecto?
        # result_panel.update_idletasks()  # Actualizate FRAME!
        # result_panel.after(500, update_result_search(search_result_thread, result_panel)) # Se pone la actualizacion 200ms despues de pintar el frame por defecto?
        # result_panel.after(500, update_data_box(search_result_thread, result_panel)) # Se pone la actualizacion 200ms despues de pintar el frame por defecto?
        #
