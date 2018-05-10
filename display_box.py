from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import os
from torrentscraper import scraper_engine as se
from torrentscraper.datastruct.websearch_instance import WebSearchInstance
from simple_option_menu import SimpleOptionMenu
from simple_list_box import SimpleListBox
from imdbfilmextension import IMDbExtension
from simple_poster_box import SimplePosterBox
from simple_info_box import SimpleInfoBox

class DisplayBox(Frame):
    def __init__(self, master, row, column, width=275, height=300, background='red'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.flag_box = None
        self.label1 = None
        self.label2 = None
        self.label3 = None
        self.label4 = None
        self.label5 = None
        self.on_create()

    def on_create(self):
        # Future : frame.resize((48, 48), Image.ANTIALIAS)
        flag_box = Frame(self, width=200, height=50)
        flag_box.grid(row=0, column=0)
        self.flag_box = flag_box

        # Generating the Spots for the Images
        tmp_img = Image.open('./60x48px/placeholder.png')

        # Setting up image loading
        placeholder = ImageTk.PhotoImage(tmp_img)
        flag_box.placeholder = placeholder

        # Color de para el esqueleto: #F0F8FF
        # Blocks to the left side of the item box
        initial_block = Frame(flag_box, width=35, height=48, background='#ADD8E6')
        initial_block.grid(row=0, column=0)

        space_block0 = Frame(flag_box, width=3, height=48, background='#ADD8E6')
        space_block0.grid(row=0, column=1)

        # Fifth to the right side
        lable5 = Label(flag_box, width=60, height=48, background='#ADD8E6')
        lable5.configure(borderwidth=0, image=placeholder)
        lable5.grid(row=0, column=2)
        self.label5 = lable5

        space_block1 = Frame(flag_box, width=3, height=48, background='#ADD8E6')
        space_block1.grid(row=0, column=3)

        # Fourth to the rigth side
        label4 = Label(flag_box, width=60, height=48, background='#ADD8E6')
        label4.configure(borderwidth=0, image=placeholder)
        label4.grid(row=0, column=4)
        self.label4 = label4

        space_block2 = Frame(flag_box, width=3, height=48, background='#ADD8E6')
        space_block2.grid(row=0, column=5)

        # Third to the right side
        label3 = Label(flag_box, width=60, height=48, background='#ADD8E6')
        label3.configure(borderwidth=0, image=placeholder)
        label3.grid(row=0, column=6)
        self.label3 = label3

        space_block3 = Frame(flag_box, width=3, height=48, background='#ADD8E6')
        space_block3.grid(row=0, column=7)

        # Second to the right side
        label2 = Label(flag_box, width=60, height=48, background='#ADD8E6')
        label2.configure(borderwidth=0, image=placeholder)
        label2.grid(row=0, column=8)
        self.label2 = label2

        space_block4 = Frame(flag_box, width=3, height=48, background='#ADD8E6')
        space_block4.grid(row=0, column=9)

        # First to the right side
        label1 = Label(flag_box, width=60, height=48, background='#ADD8E6')
        label1.configure(borderwidth=0, image=placeholder)
        label1.grid(row=0, column=10)
        self.label1 = label1

        space_block5 = Frame(flag_box, width=3, height=48, background='#ADD8E6')
        space_block5.grid(row=0, column=11)

    def set_image(self, quality, vcodec, bit, acodec, channels):
        aux_list = []
        aux_list.append(self.get_quality_img(quality))
        aux_list.append(self.get_vcodec_img(vcodec))
        aux_list.append(self.get_bit_img(bit))
        aux_list.append(self.get_acodec_img(acodec))
        aux_list.append(self.get_channels_img(channels))

        aux = []
        # print('LIST: ', aux_list)
        for i in range(0, 5, 1):
            if aux_list[i] != './60x48px/placeholder.png':
                aux.append(aux_list[i])

        for i in range(len(aux),5,1):
            # print('Adding Key: ', './60x48px/placeholder.png')
            aux.append('./60x48px/placeholder.png')
        # print('RESULT LIST: ', aux_list)

        img0 = Image.open(aux[0])
        img1 = Image.open(aux[1])
        img2 = Image.open(aux[2])
        img3 = Image.open(aux[3])
        img4 = Image.open(aux[4])

        # Setting up image loading
        _img0 = ImageTk.PhotoImage(img0)
        self.flag_box_img0 = _img0

        _img1 = ImageTk.PhotoImage(img1)
        self.flag_box._img1 = _img1

        _img2 = ImageTk.PhotoImage(img2)
        self.flag_box._img2 = _img2

        _img3 = ImageTk.PhotoImage(img3)
        self.flag_box._img3 = _img3

        _img4 = ImageTk.PhotoImage(img4)
        self.flag_box._img4 = _img4

        self.label5.configure(image=_img4)
        self.label4.configure(image=_img3)
        self.label3.configure(image=_img2)
        self.label2.configure(image=_img1)
        self.label1.configure(image=_img0)


    def get_bit_img(self, stream):
        if '10bit' == stream:
            return './60x48px/10_bit.png'
        return './60x48px/placeholder.png'

    def get_quality_img(self, stream):
        if '4K' == stream:
            return './60x48px/4K.png'
        if '1080p' == stream:
            return './60x48px/1080.png'
        if '720p' == stream:
            return './60x48px/720.png'
        if '480p' in stream:
            return './60x48px/480.png'
        return './60x48px/placeholder.png'

    def get_vcodec_img(self, stream):
        if 'x265' == stream:
            print(stream)
            return './60x48px/h265.png'
        elif 'H265' == stream:
            return './60x48px/h265.png'
        elif 'x264' == stream:
            print(stream)
            return './60x48px/x264.png'
        elif 'H264' == stream:
            print(stream)
            return './60x48px/x264.png'
        elif 'divx' is stream:
            return './60x48px/divx.png'
        return './60x48px/placeholder.png'

    def get_channels_img(self, stream):
        if '5.1'  == stream:
            return './60x48px/6.png'
        elif '6.0'  == stream:
            return './60x48px/6.png'
        elif '6.1' == stream:
            return './60x48px/6.png'
        elif'6CH' == stream:
            return './60x48px/6.png'
        elif '7.1' == stream:
            return './60x48px/8.png'
        return './60x48px/2.png'

    def get_acodec_img(self, stream):
        if 'mp3' in stream:
            return './60x48px/mp3.png'
        if 'aac' == stream:
            return './60x48px/aac.png'
        elif 'ac3' == stream:
            return './60x48px/dolby.png'
        elif 'dts' in stream:
            return './60x48px/dts.png'
        return './60x48px/placeholder.png'