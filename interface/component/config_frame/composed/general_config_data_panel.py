from tkinter import *
from interface.component.config_frame.simple.button_box import ButtonBox
from config_parser import CustomConfigParser
from interface.component.input_frame.simple.option_menu import SimpleOptionMenu

class GeneralConfigDataPanel(Frame):
    def __init__(self, master, row, column, cmmndCloseConfig, width=275, height=274, background='#ADD8E6'):
        Frame.__init__(self, master, width=width, height=height, background=background)
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
        label = Label(label_frame1, text='Search Configuration', background=self.main_theme)
        label.grid(row=0, column=0)

        inner_border_frame1 = Frame(label_frame1, width=250, height=2, background=self.highlight_theme)
        inner_border_frame1.grid(row=1, column=0)

        # Search PopUp: Content
        inner_border_frame2 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame2.grid(row=2, column=0)

        if  self.search_config['search_config'] == '0':
            search_config_value = 'Standar'
        elif self.search_config['search_config'] == '1':
            search_config_value = 'Deep'
        else:
            search_config_value = 'Custom'

        search_configuration = {'Standar': '0', 'Deep': '1'}
        self.search_popup = SimpleOptionMenu(self, search_config_value, *search_configuration)
        self.search_popup.grid(row=3, column=0, columnspan=1)

        inner_border_frame2 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame2.grid(row=4, column=0)

        # Label Frame 2
        label_frame2 = Frame(self, width=275, height=18, background=self.main_theme)
        label_frame2.grid(row=5, column=0)

        # Label Frame 2: Content
        label = Label(label_frame2, text='Language Configuration', background=self.main_theme)
        label.grid(row=0, column=0)

        inner_border_frame4 = Frame(label_frame2, width=250, height=2, background=self.highlight_theme)
        inner_border_frame4.grid(row=1, column=0)

        # Search PopUp: Content
        inner_border_frame2 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame2.grid(row=6, column=0)

        if self.language_config['language'] == '0':
            language_value = 'English'
        elif self.language_config['language'] == '1':
            language_value = 'Spanish'
        else:
            language_value = 'English'
        language_configuration = {'English': '0', 'Spanish': '1'}
        self.language_popup = SimpleOptionMenu(self, language_value, *language_configuration)
        self.language_popup.grid(row=7, column=0, columnspan=1)

        inner_border_frame2 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame2.grid(row=8, column=0)

        # ButtonBox: Content
        inner_border_frame6 = Frame(self, width=275, height=110, background=self.main_theme)
        inner_border_frame6.grid(row=9, column=0)

        self.button_box = ButtonBox(self, 10, 0, self.cmmndCloseConfig, self.save_picks)

        inner_border_frame7 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame7.grid(row=11, column=0)

    def save_picks(self):
        language = self.language_popup.selection
        search = self.search_popup.selection

        if language == 'English':
            language_value = 0
        elif language == 'Spanish':
            language_value = 1
        else:
            language_value = 0

        if search == 'Standar':
            search_value = 0
            for item in self.scraper_config:
                # print(item, self.standar_profile[item])
                self.se_config.set_section_key('ScraperEngine', item, self.standar_profile[item])
        elif search == 'Deep':
            search_value = 1
            for item in self.scraper_config:
                # print(item, self.deep_profile[item])
                self.se_config.set_section_key('ScraperEngine', item, self.deep_profile[item])
        else:
            search_value = 2

        print(language, language_value)
        print(search, search_value)
        self.se_config.set_section_key('Search', 'search_config', str(search_value))
        self.se_config.set_section_key('Language', 'language', str(language_value))


