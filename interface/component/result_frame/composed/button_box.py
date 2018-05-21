# Import Interface Libraries
from tkinter import *
from tkinter import messagebox

# Import Custom Utils Libraries
from torrentscraper.qclient_manager import QClientManager

CANCEL = "cancel"
YES = "yes"



class ButtonBox(Frame):
    def __init__(self, master, row, column, cmmndClose, fst_text='DOWNLOAD', snd_text='EXIT', background='#ADD8E6'):
        Frame.__init__(self, master, background=background)
        self.grid(row=row, column=column)
        self.fst_text = fst_text
        self.snd_text = snd_text
        self.tmp_magnet = ''
        self.tmp_hash = ''
        self.master = master
        self.cmmndClose = cmmndClose

        self.main_theme = '#ADD8E6'
        self.highlight_theme = '#91B6CE'

        self.on_create()

    def on_create(self):
        left_border_frame = Frame(self, width=2, height=40, background=self.highlight_theme)
        left_border_frame.grid(row=0, column=0)

        button_frame = Frame(self, background=self.main_theme)
        button_frame.grid(row=0, column=1)

        B = Button(button_frame, text=self.fst_text, width=15, height=2, relief='flat', borderwidth=2, command=lambda: self.download())
        B.grid(row=0, column=0)

        inner_border_frameb = Frame(button_frame, width=2, height=40, background=self.highlight_theme)
        inner_border_frameb.grid(row=0, column=1)

        inner_border_frame = Frame(button_frame, width=40, height=40, background=self.main_theme)
        inner_border_frame.grid(row=0, column=2)

        inner_border_framea = Frame(button_frame, width=2, height=40, background=self.highlight_theme)
        inner_border_framea.grid(row=0, column=3)

        B1 = Button(button_frame, text=self.snd_text, width=15, height=2, relief='flat', borderwidth=2, command=lambda: self.cmmndClose())
        B1.grid(row=0, column=4)

        right_border_frame = Frame(self, width=2, height=40, background=self.highlight_theme)
        right_border_frame.grid(row=0, column=2)

    def download(self):
        print('Added Magnet To QBittorrent: ', self.tmp_magnet)
        if self.yes_no():
            try:
                qclient = QClientManager()
                qclient.load_magnet(self.tmp_magnet)
            except:
                print('Unable to stablish connection with the Qbittorent Remote Server!')

    def yes_no(self):
        result = messagebox.askyesno('Download', 'Are you sure you want to download the file with {0}'.format(self.tmp_hash))
        return result
