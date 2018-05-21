from tkinter import *
from tkinter import END

class SimpleInfoBox(Frame):
    def __init__(self, master, row, column, width=275, height=590, background='#ADD8E6'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.info = 'Loading Information'
        self.info_text = None
        self.on_create()

    def on_create(self):
        left_border_frame = Frame(self, width=2, height=262, background='#ADD8E6')
        left_border_frame.grid(row=0, column=0)

        info_box = Frame(self, width=590, height=275, background='#F0F8FF')
        info_box.grid(row=0, column=1)

        inner_info_box = Frame(info_box, width=590, height=275, background='#F0F8FF')
        inner_info_box.grid(row=0, column=0)

        upper_border_info_box = Frame(inner_info_box, width=620, height=2, background='#F0F8FF')
        upper_border_info_box.grid(row=0, column=0)

        info_text = Text(inner_info_box, bg='#DCDCDC', width=88, height=17)
        info_text.grid(row=1, column=0)

        lower_border_info_box = Frame(inner_info_box, width=619, height=2, background='#F0F8FF')
        lower_border_info_box.grid(row=2, column=0)

        scroll_bar = Scrollbar(inner_info_box)
        scroll_bar.grid(row=1, column=1, sticky='nw')

        scroll_bar.configure(relief='groove')
        info_text.configure(relief='flat')

        scroll_bar.config(command=info_text.yview)
        info_text.config(yscrollcommand=scroll_bar.set)

        info_text.insert(END, self.info)
        info_text.config(state=DISABLED)
        self.info_text = info_text

        lower_border_info_box = Frame(info_box, width=640, height=5, background='#ADD8E6')
        lower_border_info_box.grid(row=3, column=0)

    def set_info_text(self, info):
        self.info_text.config(state=NORMAL)
        self.info_text.delete('1.0', END)
        self.info_text.insert(END, info)
        self.info_text.config(state=DISABLED)

