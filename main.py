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
from lib.tvdbshowextension import TVDbShowExtension
from torrentscraper.webscrapers.utils.uri_builder import UriBuilder
from torrentscraper.webscrapers.pirate_bay_scraper import PirateBayScraper
import logging
from logging import DEBUG
from torrentscraper.utils.custom_logger import CustomLogger

logger = CustomLogger(name=__name__, level=DEBUG)
formatter = logging.Formatter(fmt='%(asctime)s -  [%(levelname)s]: %(message)s',
                              datefmt='%m/%d/%Y %I:%M:%S %p')
file_handler = logging.FileHandler('log/scraper_engine.log', 'w')
file_handler.setFormatter(formatter)
file_handler.setLevel(level=DEBUG)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(DEBUG)

from torrentscraper.torrent_scraper import TorrentScraper

def main():
    #run_interface()
    # # websearch0 == WebSearchInstance(title='Rick and Morty', season='3', search_type=fflags.SHOW_DIRECTORY_FLAG)
    websearch = WebSearchInstance(title='Rick and Morty', season='03', search_type=fflags.SHOW_DIRECTORY_FLAG)
    ts = TorrentScraper()
    ts.scrap_batch(websearch)
    # se = ScraperEngine()
    # p2p_instance_list = se.search(websearch)
    # dataframe = se.create_magnet_dataframe(p2p_instance_list)
    # print(dataframe)
    # # dataframe = se.unique_magnet_dataframe(dataframe)
    # dataframe = se.get_dataframe(dataframe, top=10)

if __name__ == '__main__':
    main()




# TODO Propagar Theme por los objetos, añadirlo al menu de configuración general
# pyinstaller --onefile --name TorretScraper-v0.4.8.2 --paths=C:\Users\Asigan\Documents\python-torrent-scrapper\Lib\site-packages\win32com --windowed
# --icon=C:\Users\Asigan\Documents\GitHub\python-torrent-scrapper\interface\resources\grumpy-cat.ico --log-level=DEBUG main.py
