#!/usr/bin/env python

# Import External Libraries
from tkinter import *

# Import Custom Frames
from .component.result_main_frame import ResultMainFrame
from .component.input_main_frame import InputMainFrame

# Import System Libraries
import threading
import queue

# Import Custom Utils
from lib.imdbfilmextension import IMDbExtension
from torrent_scraper import TorrentScraper
from lib.cover_downloader import CoverDownloader


class ThreadedClient:
    def __init__(self, master):
        self.master = master

        # Create the queue
        self.queue = queue.Queue()

        # Set up the GUI part
        self.gui =  InputMainFrame(master, 0, 0, self.retrieveData, self.queue)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.active_search = 0

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        '''

        :return:
        '''
        self.gui.processIncoming()
        if self.active_search:
            print('BackgroundThread: ENDED')
            top = Toplevel()
            top.geometry("865x625")
            # top.iconbitmap('./interface/placerholder/grumpy-cat.ico')
            # top.title("python-torrent-scraper-v0.3.2")
            top.resizable(width=False, height=False)
            ResultMainFrame(top, 0, 0, self.gui.dataframe, self.gui.info, self.gui.image_poster)

            # Reset the Search, variables
            # self.reset_active_search()
        else:
            self.master.after(400, self.periodicCall)

    def BackgroundThread(self, websearch):
        '''

        :param websearch:
        :return:
        '''
        if not self.active_search:
            # Block the Button Function

            # Asynchronous I/O of Scraper Engine
            self.gui.progressbar_status['text'] = 'Scraping Magnets from Trackers ...'
            torrent_scraper = TorrentScraper()
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
            imdb_extension = IMDbExtension()
            info = imdb_extension.get_movie_info(websearch.title)
            self.queue.put(info)
            self.gui.progressbar['value'] = 100
            self.gui.progressbar_status['text'] = 'Done !'
            self.gui.update_idletasks()
            self.active_search = 1

    def retrieveData(self, websearch):
        '''

        :param websearch:
        :return:
        '''
        print('Scrap!, Status: ', self.active_search)
        self.thread1 = threading.Thread(target=self.BackgroundThread, args=(websearch,))
        self.thread1.start()

    def reset_active_search(self):
        '''

        :return:
        '''
        # self.active_search = 0
        # self.gui.image_poster = None
        # self.gui.dataframe = None
        # self.gui.info = None
        pass
