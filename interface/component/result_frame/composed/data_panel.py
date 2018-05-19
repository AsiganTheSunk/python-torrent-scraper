from tkinter import *
from interface.component.result_frame.simple.data_box import SimpleDataBox
from interface.component.result_frame.composed.display_box import DisplayBox
from interface.component.result_frame.composed.button_box import ButtonBox

import gettext
idiomas = []
t = gettext.translation('programa', 'locale', languages=idiomas, fallback=True,)
_ = t.gettext
# es = gettext.translation('about_config_data_panel', localedir='./interface/locale', languages=['es'])
# es.install()
# _ = es.gettext
# _ = lambda s:s
BUTTON0_TEXT = _('DOWNLOAD')
BUTTON1_TEXT = _('EXIT')

class DataPanel(Frame):
    def __init__(self, master, row, column, cmmndClose, width=275, height=300, background='#ADD8E6'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.display_box = None
        self.data_box = None
        self.button_box = None
        self.master = master
        self.cmmndClose = cmmndClose
        self.on_create()

    def on_create(self):
        inner_border_frame3 = Frame(self, width=275, height=3, background='#ADD8E6')
        inner_border_frame3.grid(row=0, column=0)

        display_box = DisplayBox(self, 1, 0)
        self.display_box = display_box

        inner_border_frame2 = Frame(self, width=275, height=18, background='#ADD8E6')
        inner_border_frame2.grid(row=2, column=0)

        data_box = SimpleDataBox(self, 3, 0)
        self.data_box = data_box

        inner_border_frame1 = Frame(self, width=275, height=17, background='#ADD8E6')
        inner_border_frame1.grid(row=4, column=0)

        button_box = ButtonBox(self, 5, 0, self.cmmndClose, fst_text=BUTTON0_TEXT, snd_text=BUTTON1_TEXT)
        self.button_box = button_box

        inner_border_frame0 = Frame(self, width=275, height=3, background='#ADD8E6')
        inner_border_frame0.grid(row=6, column=0)


