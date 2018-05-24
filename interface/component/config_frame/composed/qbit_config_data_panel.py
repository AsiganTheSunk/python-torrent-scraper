from tkinter import *
from interface.component.config_frame.simple.button_box import ButtonBox
from interface.component.config_frame.simple.input_box import InputBox
import gettext

try:
    from config_parser import CustomConfigParser
    se_config = CustomConfigParser('./torrentscraper.ini')
    language_config = se_config.get_section_map('Language')
    if language_config['language'] == '0':
        _ = lambda s: s
    else:
        es = gettext.translation('qbit_config_data_panel', localedir='./interface/locale', languages=['es'])
        es.install()
        _ = es.gettext
except Exception as err:
    print(err)

LABEL0_TEXT = _('Remote Qbittorrent Configuration')
LABEL1_TEXT = _(': User')
LABEL2_TEXT = _(': Password')
BUTTON0_TEXT = _('SAVE')
BUTTON1_TEXT = _('EXIT')

class QbitConfigDataPanel(Frame):
    def __init__(self, master, row, column, cmmndCloseConfig, background='#ADD8E6'):
        Frame.__init__(self, master, background=background)
        self.grid(row=row, column=column)
        self.cmmndCloseConfig = cmmndCloseConfig
        self.button_box = None
        self.master = master
        self.user_entry = None
        self.pass_entry = None
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

        inner_border_framex = Frame(label_frame1, width=250, height=2, background=self.main_theme)
        inner_border_framex.grid(row=2, column=0)

        entry_frame = Frame(label_frame1, width=250, height=17, background=self.main_theme)
        entry_frame.grid(row=3, column=0)

        self.user_entry = InputBox(entry_frame, 0, 0, default_message=LABEL1_TEXT, width=15)
        self.user_entry.disable()

        inner_border_framex = Frame(label_frame1, width=250, height=2, background=self.main_theme)
        inner_border_framex.grid(row=4, column=0)

        entry_frame0 = Frame(label_frame1, width=250, height=17, background=self.main_theme)
        entry_frame0.grid(row=5, column=0)

        self.pass_entry = InputBox(entry_frame0, 0, 0, default_message=LABEL2_TEXT, width=15)
        self.pass_entry.disable()

        inner_border_frame2 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame2.grid(row=4, column=0)

        # ButtonBox: Content
        inner_border_frame3 = Frame(self, width=275, height=163, background=self.main_theme)
        inner_border_frame3.grid(row=7, column=0)

        self.button_box = ButtonBox(self, 8, 0, self.cmmndCloseConfig, self.save_picks, fst_text=BUTTON0_TEXT, snd_text=BUTTON1_TEXT)

        inner_border_frame4 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame4.grid(row=9, column=0)


    def save_picks(self):
        pass
