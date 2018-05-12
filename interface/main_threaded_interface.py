# Import Custom Widgets

# Import Custom Logger

from torrentscraper.datastruct.websearch_instance import WebSearchInstance
from lib.imdbfilmextension import IMDbExtension
from interface.widget.simple_option_menu import SimpleOptionMenu
from tkinter import *
import tkinter
import threading
import queue


from torrent_scraper import TorrentScraper
from lib.cover_downloader import CoverDownloader
from interface.widget.result_main_frame import ResultMainFrame


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

        # # Setting up the Custom Logger of the InputMainFrame()
        # self.logger = CustomLogger(name=__name__, level=INFO)
        # formatter = logging.Formatter(fmt='%(asctime)s -  [%(levelname)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        #
        # console_handler = logging.StreamHandler()
        # console_handler.setFormatter(formatter)
        # console_handler.setLevel(INFO)
        # self.logger.addHandler(console_handler)

        # Input Block
        input_block_space0 = Frame(self, width=865, height=30, background='#ADD8E6')
        input_block_space0.grid(row=0, column=0)

        input_block_space1 = Frame(self, width=803, height=2, background='#F0F8FF')
        input_block_space1.grid(row=1, column=0)

        input_block = Frame(self, width=865, height=25, background='#F0F8FF')
        input_block.grid(row=2, column=0)

        input_block_space1 = Frame(self, width=803, height=2, background='#F0F8FF')
        input_block_space1.grid(row=3, column=0)

        input_block_space1 = Frame(self, width=865, height=45, background='#ADD8E6')
        input_block_space1.grid(row=4, column=0)

        # Entries, PopUp Block
        space_block = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block.grid(row=0, column=0)

        header = {'[HorribleSubs]': 'HorribleSubs'}
        header_popup = SimpleOptionMenu(input_block, '[ Header ]', *header)
        header_popup.grid(row=0, column=1, columnspan=1, sticky='W')
        self.header_popup = header_popup

        space_block0 = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block0.grid(row=0, column=3)

        title_entry = Entry(input_block, width=34)
        title_entry.insert(END, '')
        title_entry.grid(row=0, column=4)
        self.title_entry = title_entry

        space_block1 = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block1.grid(row=0, column=5)

        year_entry = Entry(input_block, width=5)
        year_entry.insert(END, '')
        year_entry.grid(row=0, column=6)
        self.year_entry = year_entry

        space_block2 = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block2.grid(row=0, column=7)

        season_entry = Entry(input_block, width=3)
        season_entry.insert(END, '')
        season_entry.grid(row=0, column=8)
        self.season_entry = season_entry

        space_block4 = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block4.grid(row=0, column=9)

        episode_entry = Entry(input_block, width=3)
        episode_entry.insert(END, '')
        episode_entry.grid(row=0, column=10)
        self.episode_entry = episode_entry

        space_block5 = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block5.grid(row=0, column=11)

        quality = {'1080p': '1080p', '720p': '720p', 'HDTV': 'HDTV', 'WEBRip': 'WEBRip'}
        quality_popup = SimpleOptionMenu(input_block, '[ Quality ]', *quality)
        quality_popup.grid(row=0, column=12, columnspan=1, sticky='W')
        self.quality_popup = quality_popup

        space_block5 = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block5.grid(row=0, column=13)

        search_type = {'SHOW': 'SHOW', 'MOVIE': 'MOVIE', 'ANIME': 'ANIME'}
        search_type_popup = SimpleOptionMenu(input_block, '[ Search Type ]', *search_type)
        search_type_popup.grid(row=0, column=14, columnspan=1, sticky='W')
        self.search_type_popup = search_type_popup

        space_block6 = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block6.grid(row=0, column=15)

        search_button = Button(input_block, text='Search', command= lambda: retrieveData(self.get_input()), width=15, relief='groove', borderwidth=2, bg='#DCDCDC', highlightbackground='#848482')
        search_button.grid(row=0, column=16, sticky="w", pady=4, padx=3)

    def get_input(self):
        return WebSearchInstance(title=self.title_entry.get(),
                                                    season=self.season_entry.get()[:2],
                                                    episode=self.episode_entry.get(),
                                                    header=self.header_popup.selection,
                                                    quality=self.quality_popup.selection,
                                                    search_type=self.search_type_popup.selection,
                                                    year=self.year_entry.get()[:4])

    def processIncoming(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                print('result: ', msg)


            except queue.Empty:
                pass

class ThreadedClient:
    def __init__(self, master):
        self.master = master

        # Create the queue
        self.queue = queue.Queue()

        # Set up the GUI part
        self.gui =  InputMainFrame(master, 0, 0, self.retrieveData, self.queue)#, self.reset)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        self.gui.processIncoming()
        if not self.running:
            # sys.exit(1)
            print('BackgroundThread: ENDED')
            top = Toplevel()
            top.geometry("865x625")
            # top.iconbitmap('./interface/placerholder/grumpy-cat.ico')
            # top.title("python-torrent-scraper-v0.3.2")
            top.resizable(width=False, height=False)
            ResultMainFrame(top, 0, 0)
        else:
            self.master.after(500, self.periodicCall)

    def BackgroundThread(self, websearch):
        if self.running:
            # Asynchronous I/O of Scraper Engine
            torrent_scraper = TorrentScraper()
            dataframe = torrent_scraper.scrap(websearch)
            self.queue.put(dataframe)

            cover_downloader = CoverDownloader()
            cover = cover_downloader.download(websearch)
            self.queue.put(cover)

            imdb_extension = IMDbExtension()
            info = imdb_extension.get_movie_info(websearch.title)
            self.queue.put(info)

            self.running = 0

    def retrieveData(self, websearch):
        print('Scrap!, Status: ', self.running)
        self.thread1 = threading.Thread(target=self.BackgroundThread, args=(websearch,))
        self.thread1.start()

    def reset(self):
        self.running = 1
        print('Click', self.running)

root = tkinter.Tk()
client = ThreadedClient(root)
root.mainloop()