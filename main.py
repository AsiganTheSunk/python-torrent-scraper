#!/usr/bin/env python

from torrentscraper import scraper_engine as se
from torrentscraper.datastruct.websearch_instance import WebSearchInstance
from torrentscraper.webscrapers.utils.magnet_builder import MagnetBuilder
from torrentscraper.utils.custom_logger import CustomLogger
import logging

DEBUG = 20
DEBUG0 = 15

logger = CustomLogger(name=__name__, level=DEBUG)
formatter = logging.Formatter(fmt='%(asctime)s -  [%(levelname)s]: %(message)s',
                              datefmt='%m/%d/%Y %I:%M:%S %p')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(DEBUG)
logger.addHandler(console_handler)
# content = websearch(url= 'https://www.pogdesign.co.uk/cat/')
# dataframe = tvcs.TvCalendarScrapper().webscrapper(content=content.text)
# dataframe.to_csv('./montly_tvcalendar.csv', sep='\t', encoding='utf-8')

# rarbg_file = open('/home/asigan/python-torrent-scrapper/examples/rarbgexample.html')
# piratebay_file = open('/home/asigan/python-torrent-scrapper/examples/thepiratebayexample.html')
# rarbg_magnet = open('/home/asigan/python-torrent-scrapper/examples/ttlkrarbg.html')
# piratebay_magnet = open('/home/asigan/python-torrent-scrapper/examples/gotTPB.html')


MAGNET_SAMPLE = 'magnet:?xt=urn:btih:224472e05e3b1087348ea1be58febb73b5456cfc' \
                '&dn=Future.Man.S01E01.Pilot.1080p.AMZN.WEBRip.DDP5.1.x264-NTb%5Brartv%5D' \
                '&tr=http%3A%2F%2Ftracker.trackerfix.com%3A80%2Fannounce' \
                '&tr=udp%3A%2F%2F9.rarbg.me%3A2710&tr=udp%3A%2F%2F9.rarbg.to%3A2710'


def main():
    websearch = WebSearchInstance(title='Rick & Morty', year='', season='03', episode='08', quality='HDTV', header='', search_type='SHOW')
    scraper_engine = se.ScraperEngine()
    p2p_instance_list = scraper_engine.search(websearch)
    dataframe = scraper_engine.create_magnet_dataframe(p2p_instance_list)
    dataframe = scraper_engine.unique_magnet_dataframe(dataframe)
    dataframe = scraper_engine.get_dataframe(dataframe, 5)

    # mbuilder = MagnetBuilder(logger)
    #
    # magnet = mbuilder.parse_from_magnet(MAGNET_SAMPLE)
    # print(magnet['status'])
    # result = mbuilder.optimize_magnet(magnet)
    # print(result['display_name'])
    # print(result['status'])

if __name__ == '__main__':
    main()
