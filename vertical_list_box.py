#!/usr/bin/python3
# -*- coding: utf-8 -*-

from logging import INFO
import logging
from tkinter import *
from lib.fileflags import FileFlags as fflag
from torrentscraper.webscrapers.utils.magnet_builder import MagnetBuilder

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
from qbit_config_data_panel import QbitConfigDataPanel
from about_config_data_panel import AboutConfigDataPanel
from scraperengine_config_data_panel import ScraperEngineConfigDataPanel

class SimpleVerticalListBox(Listbox):
    def __init__(self, master, item_list, buttonbox=None):
        Listbox.__init__(self, master, height=20, width=15)
        self.item_list = item_list
        self.master = master
        self.buttonbox = buttonbox
        self.index_selection = StringVar()
        self.qbit = None
        self.about = None
        self.se = None

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

        if self.index_selection.get() != 'empty':
            index = self.index_selection.get()[3:-2]
            # print('INDEX:', str( self.index_selection.get()[3:-2]))
            if 'Qbittorrent' in index:
                if self.about is not None:
                    self.about.grid_remove()
                elif self.se is not None:
                    self.se.grid_remove()
                elif self.qbit is not None:
                    self.qbit.grid_forget()
                self.qbit = QbitConfigDataPanel(self.master, 0, 1)
            elif 'About' in index:
                if self.qbit is not None:
                    self.qbit.grid_remove()
                elif self.se is not None:
                    self.se.grid_remove()
                elif self.about is not None:
                    self.about.grid_remove()
                self.about = AboutConfigDataPanel(self.master, 0, 1)
            elif 'ScraperEngine' in index:
                if self.qbit is not None:
                    self.qbit.grid_remove()
                elif self.se is not None:
                    self.se.grid_remove()
                elif self.about is not None:
                    self.about.grid_remove()
                self.se = ScraperEngineConfigDataPanel(self.master, 0, 1)


    def set_item_list(self, aux_list):
        self.item_list = aux_list
        for item in self.item_list:
            self.insert(END, item)

    def get_selection(self):
        return self.index_selection.get()

