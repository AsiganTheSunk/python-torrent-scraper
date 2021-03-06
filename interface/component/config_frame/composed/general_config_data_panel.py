#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from interface.component.config_frame.simple.button_box import ButtonBox
from config_parser import CustomConfigParser
from interface.component.input_frame.simple.option_menu import SimpleOptionMenu
from interface.component.config_frame.simple.single_button_box import SingleButtonBox
import gettext
from lib.description_downloader import DescriptionDownloader
from lib.cover_downloader import CoverDownloader
try:
    se_config = CustomConfigParser('./torrentscraper.ini')
    language_config = se_config.get_section_map('Language')
    if language_config['language'] == '0':
        _ = lambda s: s
    else:
        es = gettext.translation('general_config_data_panel', localedir='./interface/locale', languages=['es'])
        es.install()
        _ = es.gettext
except Exception as err:
    print(err)

LABEL0_TEXT = _('Search Configuration')
LABEL1_TEXT = _('Language Configuration')
LANGUAGE_POPUP_TEXT = [_('English'), _('Spanish')]
SEARCH_POPUP_TEXT = [_('Standar'), _('Deep'), _('Custom')]
BUTTON0_TEXT = _('SAVE')
BUTTON1_TEXT = _('EXIT')
BUTTON2_TEXT = _('CLEAR CACHE')

class GeneralConfigDataPanel(Frame):
    def __init__(self, master, row, column, cmmndCloseConfig, background='#ADD8E6'):
        Frame.__init__(self, master, background=background)
        self.grid(row=row, column=column)
        self.cmmndCloseConfig = cmmndCloseConfig
        self.button_box = None
        self.master = master
        self.se_config = CustomConfigParser('./torrentscraper.ini')
        self.scraper_config = self.se_config.get_section_map('ScraperEngine')
        self.search_config = self.se_config.get_section_map('Search')
        self.language_config = self.se_config.get_section_map('Language')
        self.standar_profile =  self.se_config.get_section_map('StandarProfile')
        self.deep_profile = self.se_config.get_section_map('DeepProfile')

        self.language_popup = None
        self.search_popup = None

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
        label = Label(label_frame1, text=LABEL0_TEXT, background=self.main_theme, font=('calibri', (10)))
        label.grid(row=0, column=0)

        inner_border_frame1 = Frame(label_frame1, width=250, height=2, background=self.highlight_theme)
        inner_border_frame1.grid(row=1, column=0)

        # Search PopUp: Content
        inner_border_frame2 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame2.grid(row=2, column=0)

        if  self.search_config['search_config'] == '0':
            search_config_value = SEARCH_POPUP_TEXT[0]
        elif self.search_config['search_config'] == '1':
            search_config_value = SEARCH_POPUP_TEXT[1]
        else:
            search_config_value = SEARCH_POPUP_TEXT[2]


        self.search_popup = SimpleOptionMenu(self, search_config_value, *SEARCH_POPUP_TEXT)
        self.search_popup.grid(row=3, column=0, columnspan=1)

        inner_border_frame2 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame2.grid(row=4, column=0)

        # Label Frame 2
        label_frame2 = Frame(self, width=275, height=18, background=self.main_theme)
        label_frame2.grid(row=5, column=0)

        # Label Frame 2: Content
        label = Label(label_frame2, text=LABEL1_TEXT, background=self.main_theme, font=('calibri', (10)))
        label.grid(row=0, column=0)

        inner_border_frame4 = Frame(label_frame2, width=250, height=2, background=self.highlight_theme)
        inner_border_frame4.grid(row=1, column=0)

        # Search PopUp: Content
        inner_border_frame2 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame2.grid(row=6, column=0)

        if self.language_config['language'] == '0':
            language_value = LANGUAGE_POPUP_TEXT[0]
        elif self.language_config['language'] == '1':
            language_value = LANGUAGE_POPUP_TEXT[1]
        else:
            language_value = LANGUAGE_POPUP_TEXT[0]
        self.language_popup = SimpleOptionMenu(self, language_value, *LANGUAGE_POPUP_TEXT)
        self.language_popup.grid(row=7, column=0, columnspan=1)

        inner_border_frame2 = Frame(self, width=275, height=40, background=self.main_theme)
        inner_border_frame2.grid(row=8, column=0)

        single = SingleButtonBox(self, 10, 0, fst_text=BUTTON2_TEXT, cmmndClearCache=self.clear_cache)

        # ButtonBox: Content
        inner_border_frame6 = Frame(self, width=275, height=33, background=self.main_theme)
        inner_border_frame6.grid(row=11, column=0)

        self.button_box = ButtonBox(self, 12, 0, self.cmmndCloseConfig, self.save_picks, fst_text=BUTTON0_TEXT, snd_text=BUTTON1_TEXT)

        inner_border_frame7 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame7.grid(row=13, column=0)

    def save_picks(self):
        language = self.language_popup.selection
        search = self.search_popup.selection
        search_value = -1
        language_value = -1

        if language == LANGUAGE_POPUP_TEXT[0]:
            language_value = 0
        elif language == LANGUAGE_POPUP_TEXT[1]:
            language_value = 1
        else:
            language_value = 0

        if search == SEARCH_POPUP_TEXT[0]:
            search_value = 0
            for item in self.scraper_config:
                self.se_config.set_section_key('ScraperEngine', item, self.standar_profile[item])
        elif search == SEARCH_POPUP_TEXT[1]:
            search_value = 1
            for item in self.scraper_config:
                self.se_config.set_section_key('ScraperEngine', item, self.deep_profile[item])
        else:
            search_value = 2

        print('DEBUG: (Save_Picks()) - ', language, language_value)
        print('DEBUG: (Save_Picks()) - ', search, search_value)
        self.se_config.set_section_key('Search', 'search_config', str(search_value))
        self.se_config.set_section_key('Language', 'language', str(language_value))


    def clear_cache(self):
        try:
            description_downloader = DescriptionDownloader()
            description_downloader.clear_cache()
            cover_downloader = CoverDownloader()
            cover_downloader.clear_cache()
            print('Cleaning Was Successfull!!')
        except Exception as err:
            print('button clear cache',err)