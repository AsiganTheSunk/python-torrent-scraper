from tkinter import *
from interface.component.config_frame.simple.button_box import ButtonBox
import gettext
idiomas = []
t = gettext.translation('programa', 'locale', languages=idiomas, fallback=True,)
_ = t.gettext

LABEL0_TEXT = _('Remote Qbittorrent Configuration')
LABEL1_TEXT = _(': User')
LABEL2_TEXT = _(': Password')
BUTTON0_TEXT = _('SAVE')
BUTTON1_TEXT = _('EXIT')

class QbitConfigDataPanel(Frame):
    def __init__(self, master, row, column, cmmndCloseConfig, width=275, height=274, background='#ADD8E6'):
        Frame.__init__(self, master, width=width, height=height, background=background)
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
        label = Label(label_frame1, text='Remote Qbittorrent Configuration', background=self.main_theme)
        label.grid(row=0, column=0)

        inner_border_frame1 = Frame(label_frame1, width=250, height=2, background=self.highlight_theme)
        inner_border_frame1.grid(row=1, column=0)

        inner_border_framex = Frame(label_frame1, width=250, height=2, background=self.main_theme)
        inner_border_framex.grid(row=2, column=0)

        entry_frame = Frame(label_frame1, width=250, height=17, background=self.highlight_theme)
        entry_frame.grid(row=3, column=0)

        self.user_entry = Entry(entry_frame, width=15)
        self.user_entry.insert(END, '')
        self.user_entry.grid(row=0, column=0)
        self.user_entry['state'] = 'disable'

        label = Label(entry_frame, text=': User', background=self.main_theme)
        label.grid(row=0, column=1)

        push_frame = Frame(entry_frame, width=70, height=19, background=self.main_theme)
        push_frame.grid(row=0, column=3)

        inner_border_framex = Frame(label_frame1, width=250, height=2, background=self.main_theme)
        inner_border_framex.grid(row=4, column=0)

        entry_frame0 = Frame(label_frame1, width=250, height=17, background=self.main_theme)
        entry_frame0.grid(row=5, column=0)

        self.pass_entry = Entry(entry_frame0, width=15)
        self.pass_entry.insert(END, '')
        self.pass_entry.grid(row=0, column=0)
        self.pass_entry['state'] = 'disable'

        label1 = Label(entry_frame0, text=': Password', background=self.main_theme)
        label1.grid(row=0, column=1)

        push_frame0 = Frame(entry_frame0, width=47, height=18, background=self.main_theme)
        push_frame0.grid(row=0, column=3)

        inner_border_frame2 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame2.grid(row=4, column=0)

        # ButtonBox: Content
        inner_border_frame3 = Frame(self, width=275, height=160, background=self.main_theme)
        inner_border_frame3.grid(row=7, column=0)

        self.button_box = ButtonBox(self, 8, 0, self.cmmndCloseConfig, self.save_picks)

        inner_border_frame4 = Frame(self, width=275, height=3, background=self.main_theme)
        inner_border_frame4.grid(row=9, column=0)


    def save_picks(self):
        pass
