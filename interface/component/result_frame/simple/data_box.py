# Import Interface Libraries
from tkinter import *

class SimpleDataBox(Frame):
    def __init__(self, master, row, column, width=275, height=300, background='#F0F8FF'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.data = None
        self.on_create()


    def on_create(self):
        upperborder = Frame(self, width=353, height=3, background='#F0F8FF')
        upperborder.grid(row=0, column=0)

        data_box = Frame(self, width=200, height=185, background='#F0F8FF')
        data_box.grid(row=1, column=0)

        T2 = Text(data_box, bg='#DCDCDC', width=49, height=12)
        self.data = T2
        T2.grid(row=0, column=0)
        T2.configure(relief='flat')
        quote = '[Hash]: ---' \
                '\n-------------------------------------------------' \
                '\n[Size]: ---' \
                '\n[Seed]: ---' \
                '\n[Leech]: ---' \
                '\n-------------------------------------------------' \
                '\n[Language]:(-)' \
                '\n-------------------------------------------------' \
                '\n[AnnounceList]:' \
                '\n\t[HTTPS]: --\n\t[HTTP]: --\n\t[UDP]: --'

        T2.insert(END, quote)
        T2.config(state=DISABLED)

        lowerborder = Frame(self, width=353, height=3, background='#F0F8FF')
        lowerborder.grid(row=2, column=0)

    def set_data(self, info_data):
        self.data.configure(state=NORMAL)
        self.data.delete('1.0', END)
        self.data.insert(END, info_data)
        self.data.configure(state=DISABLED)
