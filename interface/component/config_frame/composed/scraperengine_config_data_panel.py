#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from interface.component.config_frame.simple.button_box import ButtonBox
from config_parser import CustomConfigParser
import gettext
from config_parser import CustomConfigParser

try:
    se_config = CustomConfigParser('./torrentscraper.ini')
    language_config = se_config.get_section_map('Language')
    if language_config['language'] == '0':
        _ = lambda s: s
    else:
        es = gettext.translation('scraperengine_config_data_panel', localedir='./interface/locale', languages=['es'])
        es.install()
        _ = es.gettext
except Exception as err:
    print(err)

LABEL0_TEXT = _('Information Sources')
BUTTON0_TEXT = _('SAVE')
BUTTON1_TEXT = _('EXIT')

class ScraperEngineConfigDataPanel(Frame):
    def __init__(self, master, row, column, cmmndCloseConfig, background='#ADD8E6'):
        Frame.__init__(self, master, background=background)
        self.grid(row=row, column=column)
        self.cmmndCloseConfig = cmmndCloseConfig
        self.button_box = None
        self.master = master
        self.se_config = CustomConfigParser('./torrentscraper.ini')
        self.scraper_config = self.se_config.get_section_map('ScraperEngine')
        self.search_config = self.se_config.get_section_map('Search')
        self.standar_profile = self.se_config.get_section_map('StandarProfile')
        self.deep_profile = self.se_config.get_section_map('DeepProfile')
        self.check_bar0 = None
        self.check_bar1 = None

        self.main_theme = '#ADD8E6'
        self.highlight_theme = '#F0F8FF'

        self.on_create()

    def on_create(self):
        inner_border_frame0 = Frame(self, width=275, height=5, background=self.main_theme)
        inner_border_frame0.grid(row=0, column=0)

        label_frame0 = Frame(self, width=275, height=18, background=self.main_theme)
        label_frame0.grid(row=1, column=0)

        label = Label(label_frame0, text=LABEL0_TEXT, background=self.main_theme)
        label.grid(row=0, column=0)

        inner_border_frame0 = Frame(label_frame0, width=250, height=2, background=self.highlight_theme)
        inner_border_frame0.grid(row=1, column=0)

        inner_border_frame2 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame2.grid(row=2, column=0)

        check_bar0 = Checkbar(self, self.scraper_config)
        check_bar0.grid(row=3, column=0)
        self.check_bar0 = check_bar0

        inner_border_frame3 = Frame(self, width=275, height=2, background=self.main_theme)
        inner_border_frame3.grid(row=4, column=0)

        check_bar1 = Checkbar0(self, self.scraper_config)
        check_bar1.grid(row=5, column=0)
        self.check_bar1 = check_bar1

        inner_border_frame4 = Frame(self, width=275, height=153, background=self.main_theme)
        inner_border_frame4.grid(row=6, column=0)

        button_box = ButtonBox(self, 7, 0, self.cmmndCloseConfig, self.save_picks, fst_text=BUTTON0_TEXT, snd_text=BUTTON1_TEXT)
        self.button_box = button_box

        inner_border_frame5 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame5.grid(row=8, column=0)

    def save_picks(self):
        aux0 = self.check_bar0.get_picks()
        aux1 = self.check_bar1.get_picks()

        result = dict(list(aux0.items()) + list(aux1.items()))
        for index, item in enumerate(result):
            print(index, item, result[item])
            self.se_config.set_section_key('ScraperEngine', item, str(result[item]))

        if len(set(result.items()) & set(self.standar_profile .items())) != 0:
            self.se_config.set_section_key('Search', 'search_config', '0')
        elif len(set(result.items()) & set(self.deep_profile .items())) != 0:
            self.se_config.set_section_key('Search', 'search_config', '1')
        else:
            self.se_config.set_section_key('Search', 'search_config', '2')

class Checkbar(Frame):
    def __init__(self, parent, picks):
        Frame.__init__(self, parent)
        self.main_theme = '#ADD8E6'
        self.highlight_theme = '#F0F8FF'
        self.picks = picks
        self.var1 = IntVar()
        self.var2 = IntVar()
        self.var3 = IntVar()

        self.var1.set(self.picks['thepiratebay'])
        check_button0 = Checkbutton(self, text='thepiratebay', variable=self.var1, background=self.main_theme)
        check_button0.grid(row=1, column=0)

        self.var2.set(self.picks['kickass'])
        check_button1 = Checkbutton(self, text='kickass', variable=self.var2, background=self.main_theme)
        check_button1.grid(row=1, column=1)

        self.var3.set(self.picks['torrentfunk'])
        check_button2 = Checkbutton(self, text='torrentfunk', variable=self.var3, background=self.main_theme)
        check_button2.grid(row=1, column=2)

    def get_picks(self):
        result = {'thepiratebay': self.var1.get(), 'kickass': self.var2.get(), 'torrentfunk':self.var3.get()}
        return result


class Checkbar0(Frame):
    def __init__(self, parent, picks):
        Frame.__init__(self, parent)
        self.main_theme = '#ADD8E6'
        self.highlight_theme = '#F0F8FF'
        self.picks = picks
        self.var4 = IntVar()
        self.var5 = IntVar()
        self.var6 = IntVar()

        self.var4.set(self.picks['extratorrent'])
        check_button0 = Checkbutton(self, text='extratorrent', variable=self.var4, background=self.main_theme)
        check_button0.grid(row=1, column=0)
        # TODO **** DISABLED
        check_button0['state'] = 'disable'

        self.var5.set(self.picks['rarbg'])
        check_button1 = Checkbutton(self, text='rarbg', variable=self.var5, background=self.main_theme)
        check_button1.grid(row=1, column=1)
        # TODO **** DISABLED
        check_button1['state'] = 'disable'

        self.var6.set(self.picks['mejortorrent'])
        check_button2 = Checkbutton(self, text='mejortorrent', variable=self.var6, background=self.main_theme)
        check_button2.grid(row=1, column=2)
        # TODO **** DISABLED
        check_button2['state'] = 'disable'

    def get_picks(self):
        result = {'extratorrent': self.var4.get(), 'rarbg': self.var5.get(), 'mejortorrent':self.var6.get()}
        return result