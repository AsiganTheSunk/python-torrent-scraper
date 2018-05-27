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

def main():
    #run_interface()
    ws = WebSearchInstance(title='Rick and Morty', season='3', quality='1080p', search_type=fflags.SHOW_DIRECTORY_FLAG)
    webscraper = PirateBayScraper(logger)
    uri_builder = UriBuilder(logger)
    tvdb = TVDbShowExtension()
    episode = ''
    number_episodes = tvdb.get_number_of_season_episodes(ws.title, ws.season)
    for index in range(0, number_episodes, 1):
        if len(str(index+1)) == 1:
            episode = '0'+str(index+1)
        ws.set_episode(episode)
        ws.validate()
        search = uri_builder.build_request_url(ws, webscraper)
        print(search)

    #ws = WebSearchInstance(title='Resident Evil 3', search_type=fflags.FILM_DIRECTORY_FLAG)
    # ws = WebSearchInstance(title='Rick and Morty', season='3', search_type=fflags.SHOW_DIRECTORY_FLAG)
    # ws = ws.validate()
    # se = ScraperEngine()
    # p2p_instance_list = se.search(ws)
    # dataframe = se.create_magnet_dataframe(p2p_instance_list)
    # print(dataframe)
    # dataframe = se.unique_magnet_dataframe(dataframe)
    # dataframe = se.get_dataframe(dataframe, top=10)

if __name__ == '__main__':
    main()

# TODO Propagar Theme por los objetos, añadirlo al menu de configuración general
# pyinstaller --onefile --name TorretScraper-v0.4.8.2 --paths=C:\Users\Asigan\Documents\python-torrent-scrapper\Lib\site-packages\win32com --windowed
# --icon=C:\Users\Asigan\Documents\GitHub\python-torrent-scrapper\interface\resources\grumpy-cat.ico --log-level=DEBUG main.py
