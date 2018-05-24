#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from interface.main_threaded_interface import ThreadedClient
import os

def run_interface():
    root = tkinter.Tk()
    client = ThreadedClient(root)
    root.resizable(width=False, height=False)
    if os.name == 'nt':
        root.iconbitmap('./interface/resources/grumpy-cat.ico')
    root.title('python-torrent-scraper-interface-v0.4.9')
    root.mainloop()
