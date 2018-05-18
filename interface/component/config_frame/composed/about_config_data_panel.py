from tkinter import *
from interface.component.config_frame.simple.button_box import ButtonBox

import gettext
idiomas = []
# t = gettext.translation('programa', 'locale', languages=idiomas, fallback=True,)
# _ = t.gettext
es = gettext.translation('about_config_data_panel', localedir='./interface/locale', languages=['es'])
es.install()
_ = es.gettext
# _ = lambda s:s

LABEL0_TEXT = _('About')
LABEL1_TEXT = _('Did it for the Lulz')
BUTTON0_TEXT = _('ISSUE')
BUTTON1_TEXT = _('EXIT')

class AboutConfigDataPanel(Frame):
    def __init__(self, master, row, column, cmmndCloseConfig, width=275, height=274, background='#ADD8E6'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.master = master
        self.cmmndCloseConfig = cmmndCloseConfig
        self.main_theme = '#ADD8E6'
        self.highlight_theme = '#F0F8FF'
        self.on_create()

    def on_create(self):
        inner_border_frame0 = Frame(self, width=275, height=5, background=self.main_theme)
        inner_border_frame0.grid(row=0, column=0)

        # Label Frame 1
        label_frame1 = Frame(self, width=275, height=18, background=self.main_theme)
        label_frame1.grid(row=1, column=0)

        # Label Frame 1: Content
        label = Label(label_frame1, text=LABEL0_TEXT, background=self.main_theme)
        label.grid(row=0, column=0)

        inner_border_frame1 = Frame(label_frame1, width=250, height=2, background=self.highlight_theme)
        inner_border_frame1.grid(row=1, column=0)

        label = Label(self, text=LABEL1_TEXT, background=self.main_theme)
        label.grid(row=2, column=0)

        inner_border_frame2 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame2.grid(row=3, column=0)

        # ButtonBox: Content
        inner_border_frame3 = Frame(self, width=275, height=183, background=self.main_theme)
        inner_border_frame3.grid(row=4, column=0)

        self.button_box = ButtonBox(self, 5, 0, self.cmmndCloseConfig, self.open_issue, fst_text=BUTTON0_TEXT, snd_text=BUTTON1_TEXT)

        inner_border_frame4 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame4.grid(row=6, column=0)

    def open_issue(self):
        pass