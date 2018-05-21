#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import System Libraries
import queue
import gettext

# Import Custom Interface Components
from interface.component.input_frame.simple.option_menu import SimpleOptionMenu

# Import Custom DataStructure
from torrentscraper.datastruct.websearch_instance import WebSearchInstance
from interface.component.config_frame.config_main_frame import ConfigMainFrame

from input_box import InputBox
# Import Interface Libraries
from tkinter import *
from tkinter.ttk import Progressbar
from lib.fileflags import FileFlags as fflags
from config_parser import CustomConfigParser

try:
    se_config = CustomConfigParser('./torrentscraper.ini')
    language_config = se_config.get_section_map('Language')
    if language_config['language'] == '0':
        _ = lambda s: s
    else:
        es = gettext.translation('input_main_frame', localedir='./interface/locale', languages=['es'])
        es.install()
        _ = es.gettext
except Exception as err:
    print(err)

HEADER_TEXT = _('[ Header ]')
QUALITY_TEXT = _('[ Quality ]')
YEAR_TEXT = _('Year')
TITLE_TEXT = _('Title')
SEASON_TEXT = _('S')
EPISODE_TEXT = _('Ep')
SEARCH_TYPE = _('[ Category ]')
SEARCH_TYPE_LIST = [_('SHOW'), _('FILM'), _('ANIME')]
SEARCH_TEXT = _('Search')

class InputMainFrame(Frame):
    def __init__(self, master, row, column, retrieveData, queue):
        self.name = self.__class__.__name__
        # Setting Up the InputMainFrame
        Frame.__init__(self, master)
        self.configure(background='#ADD8E6')
        self.grid(row=row, column=column)

        # Parent Frame & Queue for Threading
        self.master = master
        self.queue = queue

        # Input Variable
        self.header_popup = None
        self.title_entry = None
        self.year_entry = None
        self.season_entry = None
        self.episode_entry = None
        self.quality_popup = None
        self.search_type_popup = None

        # Setting Up the Variables to be Updated in Top Frame
        self.image_poster = None
        self.dataframe = None
        self.info = None

        self.progressbar = None
        self.progressbar_status = None
        self.search_button = None

        self.main_theme = '#ADD8E6'
        self.highlight_theme = '#91B6CE'

        self.on_create(retrieveData)

    def on_create(self, retrieveData):
        # Input Block
        input_block_space0 = Frame(self, width=865, height=30, background=self.main_theme)
        input_block_space0.grid(row=0, column=0)

        input_block_space1 = Frame(self, width=852, height=2, background=self.highlight_theme)
        input_block_space1.grid(row=1, column=0)

        input_block = Frame(self, width=865, height=25, background='#F0F8FF')
        input_block.grid(row=2, column=0)

        input_block_space1 = Frame(self, width=852, height=2, background=self.highlight_theme)
        input_block_space1.grid(row=3, column=0)

        input_block_space2 = Frame(self, width=865, height=20, background=self.main_theme)
        input_block_space2.grid(row=4, column=0)

        label_status = Label(input_block_space2, background=self.main_theme)
        label_status.grid(row=0,column=0)
        self.progressbar_status = label_status

        progressbar_block = Progressbar(self, orient=HORIZONTAL, length=855, mode='determinate')
        progressbar_block.grid(row=5, column=0)
        self.progressbar = progressbar_block

        input_block_space3 = Frame(self, width=865, height=5, background='#ADD8E6')
        input_block_space3.grid(row=6, column=0)

        ##########################################################################################
        # Entries, PopUp Block
        space_block = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block.grid(row=0, column=0)

        header = {'[HorribleSubs]': 'HorribleSubs'}
        self.header_popup = SimpleOptionMenu(input_block, HEADER_TEXT, *header)
        self.header_popup.grid(row=0, column=1, columnspan=1, sticky='W')

        space_block0 = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block0.grid(row=0, column=3)

        self.title_entry =InputBox(input_block, 0, 4, default_message=TITLE_TEXT)

        space_block1 = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block1.grid(row=0, column=5)

        self.year_entry = InputBox(input_block, 0, 6, width=5, default_message=YEAR_TEXT)

        space_block2 = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block2.grid(row=0, column=7)

        self.season_entry = InputBox(input_block, 0, 8, width=3, default_message=SEASON_TEXT)

        space_block4 = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block4.grid(row=0, column=9)

        self.episode_entry = InputBox(input_block, 0, 10, width=3, default_message=EPISODE_TEXT)

        space_block5 = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block5.grid(row=0, column=11)

        quality = ['1080p', '720p','HDTV', 'WEBRip', '']
        self.quality_popup = SimpleOptionMenu(input_block, QUALITY_TEXT, *quality)
        self.quality_popup.grid(row=0, column=12, columnspan=1, sticky='W')

        space_block5 = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block5.grid(row=0, column=13)

        self.search_type_popup = SimpleOptionMenu(input_block, SEARCH_TYPE, *SEARCH_TYPE_LIST)
        self.search_type_popup.grid(row=0, column=14, columnspan=1, sticky='W')

        space_block6 = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block6.grid(row=0, column=15)

        self.search_button = Button(input_block, text=SEARCH_TEXT, command=lambda: retrieveData(self.get_input()), width=15, relief='groove', borderwidth=2, bg='#DCDCDC', highlightbackground='#848482')
        self.search_button.grid(row=0, column=16, sticky="w", pady=4, padx=3)

        config_img = PhotoImage(file='./interface/resources/config.png')
        self.config_img = config_img
        config_button = Button(input_block, relief='groove', borderwidth=2, bg='#DCDCDC', highlightbackground='#848482', image=config_img, command= lambda: self.configuration())
        config_button.grid(row=0, column=18, sticky="w", pady=4, padx=2)

    def configuration(self):
        top = Toplevel()
        top.iconbitmap('./interface/resources/grumpy-cat.ico')
        top.resizable(width=False, height=False)
        config = ConfigMainFrame(top, 1, 0)

    def get_input(self):
        search_type = ''
        if self.search_type_popup.selection == 'FILM' or self.search_type_popup.selection == 'CINE':
            search_type = fflags.FILM_DIRECTORY_FLAG
        elif self.search_type_popup.selection == 'SHOW' or self.search_type_popup.selection =='SERIE':
            search_type = fflags.SHOW_DIRECTORY_FLAG
        elif self.search_type_popup.selection == 'ANIME':
            search_type = fflags.ANIME_DIRECTORY_FLAG
        return WebSearchInstance(title=self.title_entry.get(),
                                                    season=self.season_entry.get()[:2],
                                                    episode=self.episode_entry.get(),
                                                    header=self.header_popup.selection,
                                                    quality=self.quality_popup.selection,
                                                    search_type=search_type,
                                                    year=self.year_entry.get()[:4])

    def validate_entries(self):
        if self.search_type_popup.selection == 'SHOW' or self.search_type_popup.selection == 'SERIE':
            if len(self.title_entry.get()) and len(self.season_entry.get()) and len(self.episode_entry.get()) > 0:
                return True
        elif self.search_type_popup.selection == 'FILM' or self.search_type_popup.selection == 'CINE':
            if len(self.title_entry.get()) > 0:
                return True
        elif self.search_type_popup.selection == 'ANIME':
            if len(self.title_entry.get()) and len(self.episode_entry.get()) > 0:
                return True
        return False

    def processIncoming(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                if self.dataframe is None:
                    self.dataframe = msg

                elif self.image_poster is None:
                    self.image_poster = msg

                elif self.info is None:
                    self.info = msg

                print('*********************' * 4)
                print('Dataframe: \n', self.dataframe)
                print('Info: \n', self.info)
                print('ImagePoster: ', self.image_poster)
                print('*********************' * 4)
            except queue.Empty:
                pass