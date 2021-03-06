#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import External Libraries
from tkinter import *
# Import Custom Frames
from interface.component.result_frame.result_main_frame import ResultMainFrame
from interface.component.input_frame.input_main_frame import InputMainFrame
# Import System Libraries
import threading
import queue
import os
# Import Custom Utils
from torrentscraper.torrent_scraper import TorrentScraper
from lib.cover_downloader import CoverDownloader
from lib.description_downloader import DescriptionDownloader

from config_parser import CustomConfigParser
import gettext
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

SOURCE_TEXT = _('[ Source ]')

class ThreadedClient:
    def __init__(self, master):
        self.master = master

        # Create the queue
        self.queue = queue.Queue()

        # Set up the GUI part
        self.gui = InputMainFrame(master, 0, 0, self.retrieveData, self.queue)
        self.result_gui = None
        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.active_search = 0
        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()
        self.periodicCallCategory()

    def periodicCallCategory(self):
        if self.gui.search_type_popup.selection == 'SHOW' or self.gui.search_type_popup.selection == 'SERIE':
            self.gui.year_entry.reset_to_default()
            self.gui.title_entry.enable()
            self.gui.year_entry.disable()
            self.gui.season_entry.enable()
            self.gui.episode_entry.enable()
            self.gui.source_popup['state'] = 'disable'
            self.gui.quality_popup['state'] = 'normal'


        elif self.gui.search_type_popup.selection == 'FILM' or self.gui.search_type_popup.selection == 'CINE':
            self.gui.episode_entry.reset_to_default()
            self.gui.season_entry.reset_to_default()
            self.gui.title_entry.enable()
            self.gui.year_entry.enable()
            self.gui.season_entry.disable()
            self.gui.episode_entry.disable()

            self.gui.update_idletasks()
            self.gui.source_popup['state'] = 'disable'
            self.gui.quality_popup['state'] = 'normal'


        elif self.gui.search_type_popup.selection == 'ANIME':
            self.gui.year_entry.reset_to_default()
            self.gui.season_entry.reset_to_default()
            self.gui.title_entry.enable()
            self.gui.year_entry.disable()
            self.gui.season_entry.disable()
            self.gui.episode_entry.enable()
            self.gui.source_popup['state'] = 'normal'
            self.gui.quality_popup['state'] = 'normal'


        else:
            self.gui.title_entry.reset_to_default()
            self.gui.title_entry.disable()
            self.gui.year_entry.disable()
            self.gui.season_entry.disable()
            self.gui.episode_entry.disable()
            self.gui.source_popup['state'] = 'disable'
            self.gui.quality_popup['state'] = 'disable'

        self.master.after(100, self.periodicCallCategory)

    def periodicCall(self):
        '''

        :return:
        '''
        self.gui.processIncoming()
        while self.active_search:
            print('BackgroundThread: ENDED')
            top = Toplevel()
            if os.name == 'nt':
                top.iconbitmap('./interface/resources/grumpy-cat.ico')
            top.resizable(width=False, height=False)

            self.result_gui = ResultMainFrame(top, 0, 0, self.gui.dataframe, self.gui.info, self.gui.image_poster)
            self.gui.search_button['state'] = 'normal'
            self.reset_active_search()
        else:
            self.master.after(100, self.periodicCall)

    def BackgroundThread(self, websearch):
        '''

        :param websearch:
        :return:
        '''
        if not self.active_search:
            self.se_config = CustomConfigParser('./torrentscraper.ini')
            self.scraper_config = self.se_config.get_section_map('ScraperEngine')

            # Asynchronous I/O of Scraper Engine
            self.gui.progressbar_status['text'] = 'Scraping Magnets from Trackers ...'
            torrent_scraper = TorrentScraper(self.scraper_config)
            dataframe = torrent_scraper.scrap(websearch)
            self.queue.put(dataframe)
            self.gui.progressbar['value'] = 60
            self.gui.update_idletasks()

            self.gui.progressbar_status['text'] = 'Retrieving Poster Image ...'
            cover_downloader = CoverDownloader()
            cover = cover_downloader.download(websearch)
            self.queue.put(cover)
            self.gui.progressbar['value'] = 80
            self.gui.update_idletasks()

            self.gui.progressbar_status['text'] = 'Retrieving General Information ...'

            description_downloader = DescriptionDownloader()
            info = description_downloader.get_info(websearch.search_type, websearch.title)
            self.queue.put(info)
            self.gui.progressbar['value'] = 100
            self.gui.progressbar_status['text'] = 'Done !'
            self.gui.update_idletasks()
            self.active_search = 1
            print('Status: ', self.active_search)

    def retrieveData(self, websearch):
        '''

        :param websearch:
        :return:
        '''
        if self.gui.validate_entries():
            print('Scrap!, Status: ', self.active_search)
            self.gui.search_button['state'] = 'disable'
            self.gui.update_idletasks()
            tmp_websearh = websearch.validate()

            thread = threading.Thread(target=self.BackgroundThread, args=(tmp_websearh,))
            thread.start()




    def reset_active_search(self):
        '''

        :return:
        '''
        self.active_search = 0
        self.gui.progressbar['value'] = 0
        self.gui.progressbar_status['text'] = ''
        self.gui.update_idletasks()
        self.gui.image_poster = None
        self.gui.dataframe = None
        self.gui.info = None
