# Import System Libraries
import queue

# Import Custom Interface Components
from interface.component.input_frame.simple.option_menu import SimpleOptionMenu
# Import Custom DataStructure
from torrentscraper.datastruct.websearch_instance import WebSearchInstance
from interface.component.config_frame.config_main_frame import ConfigMainFrame
# Import Interface Libraries
from tkinter import *
from tkinter.ttk import Progressbar

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

        self.on_create(retrieveData)

    def on_create(self, retrieveData):
        # Input Block
        input_block_space0 = Frame(self, width=865, height=30, background='#ADD8E6')
        input_block_space0.grid(row=0, column=0)

        input_block_space1 = Frame(self, width=837, height=2, background='#F0F8FF')
        input_block_space1.grid(row=1, column=0)

        input_block = Frame(self, width=865, height=25, background='#F0F8FF')
        input_block.grid(row=2, column=0)

        input_block_space1 = Frame(self, width=837, height=2, background='#F0F8FF')
        input_block_space1.grid(row=3, column=0)

        input_block_space2 = Frame(self, width=865, height=20, background='#ADD8E6')
        input_block_space2.grid(row=4, column=0)

        label_status = Label(input_block_space2, background='#ADD8E6')
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

        search_type = {'SHOW': 'SHOW', 'FILM': 'FILM', 'ANIME': 'ANIME'}
        search_type_popup = SimpleOptionMenu(input_block, '[ Search Type ]', *search_type)
        search_type_popup.grid(row=0, column=14, columnspan=1, sticky='W')
        self.search_type_popup = search_type_popup

        space_block6 = Frame(input_block, width=3, height=25, background='#F0F8FF')
        space_block6.grid(row=0, column=15)

        search_button = Button(input_block, text='Search', command=lambda: retrieveData(self.get_input()), width=15, relief='groove', borderwidth=2, bg='#DCDCDC', highlightbackground='#848482')
        search_button.grid(row=0, column=16, sticky="w", pady=4, padx=3)
        self.search_button = search_button

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
        return WebSearchInstance(title=self.title_entry.get(),
                                                    season=self.season_entry.get()[:2],
                                                    episode=self.episode_entry.get(),
                                                    header=self.header_popup.selection,
                                                    quality=self.quality_popup.selection,
                                                    search_type=self.search_type_popup.selection,
                                                    year=self.year_entry.get()[:4])

    def validate_entries(self):
        if self.search_type_popup.selection == 'SHOW':
            if len(self.title_entry.get()) and len(self.season_entry.get()) and len(self.episode_entry.get()) > 0:
                print(self.title_entry.get())
                print(self.episode_entry.get())
                print(self.season_entry.get())
                return True
        elif self.search_type_popup.selection == 'FILM':
            if len(self.title_entry.get()) > 0:
                print(self.title_entry.get())
                return True
        elif self.search_type_popup.selection == 'ANIME':
            if len(self.title_entry.get()) and len(self.episode_entry.get()) > 0:
                print(self.title_entry.get())
                print(self.episode_entry.get())
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