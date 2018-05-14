#!/usr/bin/python3
# -*- coding: utf-8 -*-

from logging import DEBUG, INFO, WARNING
import logging
import traceback
from tkinter import Tk, BOTH, Scale, LEFT, Listbox, StringVar, END, font
from torrentscraper.fileflags import FileFlags as fflag
from torrentscraper.webscrapers.utils.magnet_builder import MagnetBuilder
from torrentscraper import scraper_engine as se
from torrentscraper.datastruct.websearch_instance import WebSearchInstance
# Import Custom Logger
from torrentscraper.utils.custom_logger import CustomLogger
from lib.metadata.regex.regexengine import RegexEngine

logger = CustomLogger(name=__name__, level=INFO)
formatter = logging.Formatter(fmt='%(asctime)s -  [%(levelname)s]: %(message)s',
                              datefmt='%m/%d/%Y %I:%M:%S %p')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(INFO)

logger.addHandler(console_handler)


class SimpleListBox(Listbox):
    def __init__(self, master, item_list, databox, displaybox ,dataframe=None):
        Listbox.__init__(self, master, height=19, width=80)
        self.item_list = item_list
        self.master = master
        self.databox = databox
        self.dislaybox = displaybox
        self.dataframe = dataframe
        self.index_selection = StringVar()
        self.on_create()

    def on_create(self):
        self.index_selection.set('empty')
        for item in self.item_list:
            self.insert(END, item)
        self.bind("<<ListboxSelect>>", self.on_select)

    def on_select(self, val):
        sender = val.widget
        index = sender.curselection()
        value = sender.get(index)

        self.index_selection.set(value)
        print(self.index_selection.get())
        # self.selection.set(value)

        if self.index_selection.get() != 'empty':
            print('INDEX:', str( self.index_selection.get()[2:-2]))
            name = self.index_selection.get()[2:-2]
            magnet = self.dataframe.loc[self.dataframe['name'] == name]['magnet'].values[0]
            size = self.dataframe.loc[self.dataframe['name'] == name]['size'].values[0]
            seed = self.dataframe.loc[self.dataframe['name'] == name]['seed'].values[0]
            leech = self.dataframe.loc[self.dataframe['name'] == name]['leech'].values[0]
            language = ''

            print('size: ',size, 'seed: ', seed, 'leech: ',leech)
            print('magnet: ', magnet)
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
                                                                           len(magnet_instance['announce_list']['https']),
                                                                           len(magnet_instance['announce_list']['http']),
                                                                           len(magnet_instance['announce_list']['udp']))
            print(quote)
            self.databox.set_data(quote)
            regex_engine = RegexEngine()
            metadata = regex_engine.map(name, fflag.SHOW_DIRECTORY_FLAG)

            self.dislaybox.set_image(metadata.quality, metadata.vcodec, metadata.bit, metadata.acodec, metadata.channels)

    def set_item_list(self, aux_list):
        self.item_list = aux_list
        for item in self.item_list:
            self.insert(END, item)

    def get_selection(self):
        return self.index_selection.get()

    def autowidth(self, maxwidth):
        f = font.Font(font=self.cget("font"))
        pixels = 0
        for item in self.get(0, "end"):
            pixels = max(pixels, f.measure(item))
        # bump listbox size until all entries fit
        pixels = pixels + 10
        width = int(self.cget("width"))
        for w in range(0, maxwidth + 1, 5):
            if self.winfo_reqwidth() > pixels:
                break
            self.config(font=('calibri', (11)), width=width + w)