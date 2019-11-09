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
    root.title('python-torrent-scraper-interface-v0.4.9.1')
    root.mainloop()


def main():
    run_interface()


if __name__ == '__main__':
    main()

# TODO Propagar Theme por los objetos, añadirlo al menu de configuración general
# pyinstaller --onefile --name TorretScraper-v0.4.8.2 --paths=C:\Users\Asigan\Documents\python-torrent-scrapper\Lib\site-packages\win32com --windowed
# --icon=C:\Users\Asigan\Documents\GitHub\python-torrent-scrapper\interface\resources\grumpy-cat.ico --log-level=DEBUG main.py
