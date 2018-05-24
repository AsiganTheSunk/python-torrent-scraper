#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from torrent_scraper_interface import run_interface
from NyaaPy import Pantsu
from torrentscraper.scraper_engine import ScraperEngine
from torrentscraper.datastruct.websearch_instance import WebSearchInstance
from lib.fileflags import FileFlags as fflags
from lib.malanimeextension import MalAnimeExtension




def main():
    run_interface()

if __name__ == '__main__':
    main()

#pyinstaller --onefile --name TorretScraper-v0.4.8.2 --paths=C:\Users\Asigan\Documents\python-torrent-scrapper\Lib\site-packages\win32com --windowed
# --icon=C:\Users\Asigan\Documents\GitHub\python-torrent-scrapper\interface\resources\grumpy-cat.ico --log-level=DEBUG main.py

# TODO Propagar Theme por los objetos, añadirlo al menu de configuración general
