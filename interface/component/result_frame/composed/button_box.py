# Import Interface Libraries
from tkinter import *
from tkinter import messagebox

# Import Custom Utils Libraries
from torrentscraper.qclient_manager import QClientManager

CANCEL = "cancel"
YES = "yes"

class ButtonBox(Frame):
    def __init__(self, master, row, column, root, width=275, height=300, background='#ADD8E6'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.on_create()
        self.tmp_magnet = ''
        self.tmp_hash = ''
        self.root = root
        self.master = master

    def on_create(self):
        left_border_frame = Frame(self, width=2, height=40, background='#F0F8FF')
        left_border_frame.grid(row=0, column=0)

        button_frame = Frame(self, width=200, height=40, background='#F0F8FF')
        button_frame.grid(row=0, column=1)

        B = Button(button_frame, text='DOWNLOAD', width=15, height=2, relief='flat', borderwidth=2, command=lambda: self.download())
        B.grid(row=0, column=0)

        inner_border_frameb = Frame(button_frame, width=2, height=40, background='#F0F8FF')
        inner_border_frameb.grid(row=0, column=1)

        inner_border_frame = Frame(button_frame, width=40, height=40, background='#ADD8E6')
        inner_border_frame.grid(row=0, column=2)

        inner_border_framea = Frame(button_frame, width=2, height=40, background='#F0F8FF')
        inner_border_framea.grid(row=0, column=3)

        B1 = Button(button_frame, text='EXIT', width=15, height=2, relief='flat', borderwidth=2, command=lambda: self.exit())
        B1.grid(row=0, column=4)

        right_border_frame = Frame(self, width=2, height=40, background='#F0F8FF')
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
        print(result)
        return result

    def exit(self):
        self.root.destroy()