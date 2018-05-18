#!/usr/bin/env python3

# Import System Libraries
from logging import INFO
import logging

# Import Interface Libraries
from tkinter import *

# Import Interface Custom Components
from interface.component.result_frame.composed.info_panel import InfoPanel
from interface.component.result_frame.composed.result_panel import ResultPanel

# Import External Libraries
from PIL import ImageTk, Image

# Import Custom Utils
from torrentscraper.utils.custom_logger import CustomLogger

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

        result_panel = ResultPanel(self, 3, 0, self.close_window)
        self.result_panel = result_panel

        lower_border_frame = Frame(self, width=864, height=14, background='#ADD8E6')
        lower_border_frame.grid(row=4, column=0)

        # Update, the contents of the two Main Panels
        self.update_poster(image_poster)
        self.update_description(info)
        self.update_result_search(dataframe)


    def close_window(self):
        self.master.destroy()

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