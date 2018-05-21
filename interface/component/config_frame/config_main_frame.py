from tkinter import *

from interface.component.config_frame.composed.custom_list_box import CustomListBox

class ConfigMainFrame(Frame):
    def __init__(self, master, row, column):
        Frame.__init__(self, master)
        self.grid(row=row, column=column)
        self.configure(background='#ADD8E6')
        self.var = IntVar()
        self.checkbutton = None

        self.main_theme = '#ADD8E6'
        self.highlight_theme = '#F0F8FF'
        self.on_create()

    def on_create(self):
        upper_border = Frame(self, width=376, height=3, background=self.main_theme)
        upper_border.grid(row=0, column=0)
        vlb = CustomListBox(self, 1, 0, self.close)
        lower_border = Frame(self, width=376, height=3, background=self.main_theme)
        lower_border.grid(row=2, column=0)

    def close(self):
        self.master.destroy()