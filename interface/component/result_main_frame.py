#!/usr/bin/env python

# Import System Libraries
from logging import INFO
import logging

# Import Interface Libraries
from tkinter import *

# Import Interface Custom Components
from .composed.info_panel import InfoPanel
from .composed.result_panel import ResultPanel

# Import External Libraries
from PIL import ImageTk, Image

# Import Custom Utils
from torrentscraper.utils.custom_logger import CustomLogger
from torrentscraper.webscrapers.utils.magnet_builder import MagnetBuilder

# Define Aux Logger to use on MagnetBuilder
# TODO Add Logger to the whole interface
logger = CustomLogger(name=__name__, level=INFO)
formatter = logging.Formatter(fmt='%(asctime)s -  [%(levelname)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(INFO)
logger.addHandler(console_handler)

class ResultMainFrame(Frame):
    def __init__(self, master, row, column, dataframe, info, image_poster, background='#ADD8E6'):
        Frame.__init__(self, master, background=background)
        self.grid(row=row, column=column)
        self.name = self.__class__.__name__
        self.master = master
        self.info_panel = None
        self.result_panel = None
        self.on_create(dataframe, info, image_poster)


    def on_create(self, dataframe, info, image_poster):
        '''

        :param dataframe:
        :param info:
        :param image_poster:
        :return:
        '''
        upper_border_frame = Frame(self, width=864, height=11, background='#ADD8E6')
        upper_border_frame.grid(row=0, column=0)

        info_panel = InfoPanel(self, 1, 0)
        self.info_panel = info_panel

        middle_border_frame = Frame(self, width=864, height=5, background='#ADD8E6')
        middle_border_frame.grid(row=2, column=0)

        result_panel = ResultPanel(self, 3, 0)
        self.result_panel = result_panel

        lower_border_frame = Frame(self, width=864, height=14, background='#ADD8E6')
        lower_border_frame.grid(row=4, column=0)

        # Update, the contents of the two Main Panels
        self.update_poster(image_poster)
        self.update_description(info)
        self.update_result_search(dataframe)
        self.update_data_box(dataframe)

    def update_poster(self, image_poster):
        '''

        :param image_poster:
        :return:
        '''
        aux = Image.open(image_poster)
        poster_image = ImageTk.PhotoImage(aux)
        self.info_panel.poster_box.poster_image = poster_image
        self.info_panel.poster_box.poster_container.configure(borderwidth=0, highlightbackground='#848482',
                                                         image=poster_image)

    def update_description(self, info):
        '''

        :param info:
        :return:
        '''
        self.info_panel.info_box.set_info_text(info)

    def update_data_box(self, dataframe):
        '''

        :param dataframe:
        :return:
        '''
        index_selection = self.result_panel.list_panel.list_box.result_box.get_selection()
        if index_selection != 'empty':
            index_selection = self.result_panel.list_panel.list_box.result_box.get_selection()
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
            self.result_panel.data_panel.data_box.data_box.set_data(quote)

    def update_result_search(self, dataframe):
        '''

        :param dataframe:
        :return:
        '''
        self.result_panel.list_panel.list_box.result_box.dataframe = dataframe
        lista = []
        for index in dataframe.index.tolist():
            dn = dataframe.iloc[int(index)]['name']
            formato = '[ {0} ]'.format(dn)
            lista.append(formato)

        self.result_panel.list_panel.list_box.result_box.set_item_list(lista)