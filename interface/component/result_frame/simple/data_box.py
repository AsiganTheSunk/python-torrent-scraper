# Import Interface Libraries
from tkinter import *
from config_parser import CustomConfigParser
import gettext

try:
    se_config = CustomConfigParser('./torrentscraper.ini')
    language_config = se_config.get_section_map('Language')
    if language_config['language'] == '0':
        _ = lambda s: s
    else:
        es = gettext.translation('data_box', localedir='./interface/locale', languages=['es'])
        es.install()
        _ = es.gettext

    HASH_TEXT = _('Hash')
    SIZE_TEXT = _('Size')
    SEED_TEXT = _('Seeds')
    LEECH_TEXT = _('Leechs')
    LANGUAGE_TEXT = _('Language')
    ANNOUNCE_LIST_TEXT = _('AnnounceList')
except Exception as err:
    print(err)

class SimpleDataBox(Frame):
    def __init__(self, master, row, column, background='#F0F8FF'):
        Frame.__init__(self, master, background=background)
        self.grid(row=row, column=column)
        self.data = None
        self.main_theme = '#ADD8E6'
        self.highlight_theme = '#91B6CE'
        self.on_create()

    def on_create(self):
        upperborder = Frame(self, width=396, height=2, background=self.highlight_theme)
        upperborder.grid(row=0, column=0)

        data_box = Frame(self, background=self.highlight_theme)
        data_box.grid(row=1, column=0)

        T2 = Text(data_box, bg='#DCDCDC', width=49, height=12)
        self.data = T2
        T2.grid(row=0, column=0)
        T2.configure(relief='flat')
        quote = '[{0}]: ---' \
                '\n-------------------------------------------------' \
                '\n[{1}]: ---' \
                '\n[{2}]: ---' \
                '\n[{3}]: ---' \
                '\n-------------------------------------------------' \
                '\n[{4}]:( - )' \
                '\n-------------------------------------------------' \
                '\n[{5}]:' \
                '\n\t[HTTPS]: --\n\t[HTTP]: --\n\t[UDP]: --'.format(HASH_TEXT, SIZE_TEXT, SEED_TEXT, LEECH_TEXT, LANGUAGE_TEXT, ANNOUNCE_LIST_TEXT)

        T2.insert(END, quote)
        T2.config(state=DISABLED)

        lowerborder = Frame(self, width=396, height=2, background=self.highlight_theme)
        lowerborder.grid(row=2, column=0)

    def set_data(self, info_data):
        self.data.configure(state=NORMAL)
        self.data.delete('1.0', END)
        self.data.insert(END, info_data)
        self.data.configure(state=DISABLED)
