#!/usr/bin/python3
# -*- coding: utf-8 -*-

from logging import INFO
import logging
from tkinter import *

# Import Custom Logger
from torrentscraper.utils.custom_logger import CustomLogger

logger = CustomLogger(name=__name__, level=INFO)
formatter = logging.Formatter(fmt='%(asctime)s -  [%(levelname)s]: %(message)s',
                              datefmt='%m/%d/%Y %I:%M:%S %p')


console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(INFO)

logger.addHandler(console_handler)
from interface.component.config_frame.composed.qbit_config_data_panel import QbitConfigDataPanel
from interface.component.config_frame.composed.about_config_data_panel import AboutConfigDataPanel
from interface.component.config_frame.composed.scraperengine_config_data_panel import ScraperEngineConfigDataPanel
from interface.component.config_frame.composed.general_config_data_panel import GeneralConfigDataPanel

class SimpleVerticalListBox(Listbox):
    def __init__(self, master, item_list, right_block, cmmndCloseConfig,buttonbox=None):
        Listbox.__init__(self, master, height=19, width=15)
        self.item_list = item_list
        self.master = master
        self.buttonbox = buttonbox
        self.cmmndCloseConfig = cmmndCloseConfig
        self.right_block = right_block
        self.index_selection = StringVar()
        self.qbit = None
        self.about = None
        self.se = None
        self.general = None

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
            if 'Qbittorrent' in index:
                self.eval_frame()
                self.qbit = QbitConfigDataPanel(self.right_block, 0, 0, self.cmmndCloseConfig)
            elif 'About' in index:
                self.eval_frame()
                self.about = AboutConfigDataPanel(self.right_block, 0, 0, self.cmmndCloseConfig)
            elif 'General' in index:
                self.eval_frame()
                self.general = GeneralConfigDataPanel(self.right_block, 0, 0, self.cmmndCloseConfig)
            elif 'ScraperEngine' in index:
                self.eval_frame()
                self.se = ScraperEngineConfigDataPanel(self.right_block, 0, 0, self.cmmndCloseConfig)

    def eval_frame(self):
        if self.qbit is not None:
            self.qbit.grid_remove()
            self.qbit.destroy()
            self.qbit = None
        elif self.se is not None:
            self.se.grid_remove()
            self.se.destroy()
            self.se = None
        elif self.about is not None:
            self.about.grid_remove()
            self.about.destroy()
            self.about = None
        elif self.general is not None:
            self.general.grid_remove()
            self.general.destroy()
            self.general = None


    def set_item_list(self, aux_list):
        self.item_list = aux_list
        for item in self.item_list:
            self.insert(END, item)

    def get_selection(self):
        return self.index_selection.get()

