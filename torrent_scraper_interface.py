#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from interface.main_threaded_interface import ThreadedClient

def run_interface():
    root = tkinter.Tk()
    client = ThreadedClient(root)
    root.resizable(width=False, height=False)
    # root.attributes("-toolwindow", 1)
    root.iconbitmap('./interface/resources/grumpy-cat.ico')
    root.title("python-torrent-scraper-interface-v0.4.8")
    root.mainloop()
