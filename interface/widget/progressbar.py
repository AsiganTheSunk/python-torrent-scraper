#!/usr/bin/env python

try:
  import Tkinter              # Python 2
  import ttk
except ImportError:
    from tkinter import *       # Python 3
    import tkinter.ttk as ttk
    from PIL import ImageTk, Image

class SimplePB:
    def __init__(self, parent):
        self.parent = parent

        self.ProgressBar()

    def ProgressBar(self):
        ft = ttk.Frame()
        ft.pack(expand=True, fill=X, side=BOTTOM)
        pb_hd = ttk.Progressbar(ft, orient='horizontal', mode='indeterminate')
        pb_hd.pack(expand=True, fill=X, side=BOTTOM)
        pb_hd.start(50)
