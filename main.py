#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from torrent_scraper_interface import run_interface
from NyaaPy import Pantsu
from torrentscraper.scraper_engine import ScraperEngine
from torrentscraper.datastruct.websearch_instance import WebSearchInstance
from lib.fileflags import FileFlags as fflags
from lib.malanimeextension import MalAnimeExtension
from torrentscraper.webscrapers.mejortorrent_scraper import MejorTorrentScraper
from torrentscraper.webscrapers.utils.uri_builder import UriBuilder

def main():
    # run_interface()

    from torrentscraper.webscrapers import mejortorrent_scraper as mjrt

    ws = WebSearchInstance(title='Resident Evil 3', search_type=fflags.FILM_DIRECTORY_FLAG)
    #ws = WebSearchInstance(title='Rick y Morty', search_type=fflags.SHOW_DIRECTORY_FLAG)
    ws = ws.validate()
    se = ScraperEngine()
    p2p_instance_list = se.search(ws)
    dataframe = se.create_magnet_dataframe(p2p_instance_list)
    dataframe = se.unique_magnet_dataframe(dataframe)
    dataframe = se.get_dataframe(dataframe, top=10)

if __name__ == '__main__':
    main()

# TODO Propagar Theme por los objetos, añadirlo al menu de configuración general
# pyinstaller --onefile --name TorretScraper-v0.4.8.2 --paths=C:\Users\Asigan\Documents\python-torrent-scrapper\Lib\site-packages\win32com --windowed
# --icon=C:\Users\Asigan\Documents\GitHub\python-torrent-scrapper\interface\resources\grumpy-cat.ico --log-level=DEBUG main.py
