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

# Introducir Threshholds de comportamiento, para el sleep, en base a los tiempos de respuesta y que se ajuste.
def main():
    run_interface()
    #
    # websearch = WebSearchInstance(title='Silicon Valley', season='1', quality='HDTV', search_type=fflags.SHOW_DIRECTORY_FLAG)
    # websearch = websearch.validate()
    # ts = TorrentScraper()
    # result = ts.scrap(websearch)

    # print(result.values)
    # for a in result.values:
    #     print(a[0], a[1], a[2], a[3], a[4], a[5], a[6])

if __name__ == '__main__':
    main()




# TODO Propagar Theme por los objetos, añadirlo al menu de configuración general
# pyinstaller --onefile --name TorretScraper-v0.4.8.2 --paths=C:\Users\Asigan\Documents\python-torrent-scrapper\Lib\site-packages\win32com --windowed
# --icon=C:\Users\Asigan\Documents\GitHub\python-torrent-scrapper\interface\resources\grumpy-cat.ico --log-level=DEBUG main.py
