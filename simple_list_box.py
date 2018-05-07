#!/usr/bin/python3
# -*- coding: utf-8 -*-
from tkinter import Tk, BOTH, Scale, LEFT, Listbox, StringVar, END, font

class SimpleListBox(Listbox):
    def __init__(self, master, item_list):
        Listbox.__init__(self, master, height=19, width=80)
        self.item_list = item_list
        self.selection = StringVar()
        self.on_create()

    def on_create(self):

        for item in self.item_list:
            self.insert(END, item)
        self.bind("<<ListboxSelect>>", self.on_select)

    def on_select(self, val):
        sender = val.widget
        index = sender.curselection()
        value = sender.get(index)
        self.selection.set(value)

    def get_selection(self):
        return self.selection

    def autowidth(self, maxwidth):
        f = font.Font(font=self.cget("font"))
        pixels = 0
        for item in self.get(0, "end"):
            pixels = max(pixels, f.measure(item))
        # bump listbox size until all entries fit
        pixels = pixels + 10
        width = int(self.cget("width"))
        for w in range(0, maxwidth + 1, 5):
            if self.winfo_reqwidth() > pixels:
                break
            self.config(font=('calibri', (11)), width=width + w)