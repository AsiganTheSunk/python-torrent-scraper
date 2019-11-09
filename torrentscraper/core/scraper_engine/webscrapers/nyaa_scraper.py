#!/usr/bin/env python3

# Import External Libraries
from NyaaPy.utils import Utils
from bs4 import BeautifulSoup

# Import System Libraries
import traceback

# Import Custom Data Structure
from torrentscraper.datastruct.rawdata_instance import RAWDataInstance

# Import Custom Exceptions
from torrentscraper.core.scraper_engine.webscrapers.exceptions.webscraper_error import WebScraperProxyListError
from torrentscraper.core.scraper_engine.webscrapers.exceptions.webscraper_error import WebScraperParseError
from torrentscraper.core.scraper_engine.webscrapers.exceptions.webscraper_error import WebScraperContentError

# Constants
from lib.fileflags import FileFlags as fflags

class NyaaScraper():
    def __init__(self, logger):
        self.name = self.__class__.__name__
        self.logger = logger
        self.proxy_list = ['http://nyaa.si']
        self._proxy_list_length = len(self.proxy_list)
        self._proxy_list_pos = 0
        self.cloudflare_cookie = False
        self.query_type = True
        self.disable_quality = False
        self.thread_defense_bypass_cookie = False
        self.torrent_file = False
        self.magnet_link = True

        self.main_page = self.proxy_list[self._proxy_list_pos]
        self.default_search = '/'
        self.default_tail = ''
        self.default_params = {'f': '0', 'c:': '0_0', 'p': '0'}
        self.supported_searchs = [fflags.ANIME_DIRECTORY_FLAG]

    def update_main_page(self):
        try:
            value = self._proxy_list_pos
            if self._proxy_list_length > self._proxy_list_pos:
                value += 1

            self._proxy_list_pos = value
            self.main_page = self.proxy_list[self._proxy_list_pos]
        except IndexError as err:
            raise WebScraperProxyListError(self.name, err, traceback.format_exc())

    def get_raw_data(self, content=None):
        raw_data = RAWDataInstance()
        soup = BeautifulSoup(content, 'html.parser')

        try:
            ttable = soup.select('table tr')
            if ttable != []:
                dict_result = Utils.parse_nyaa(ttable, limit=None)

                for item in dict_result:
                    seed = str(item['seeders'])
                    if seed == '0':
                        seed = '1'
                    leech = str(item['leechers'])
                    if leech == '0':
                        leech = '1'

                    size = item['size']
                    if 'MiB' in size:
                        size = size.replace('MiB', 'MB')
                        size = float(size[:-2])
                    elif 'GiB' in size:
                        size = size.replace('GiB', 'GB')
                        size = float(size[:-2]) * 1000

                    magnet_link = item['magnet']

                    raw_data.add_magnet(str(magnet_link))
                    raw_data.add_size(int(size))
                    raw_data.add_seed(int(seed))
                    raw_data.add_leech(int(leech))
                    self.logger.debug('{0} New Entry Raw Values: {1:7} {2:>4}/{3:4} {4}'.format(
                        self.name, str(size), str(seed), str(leech), magnet_link))
            else:
                raise WebScraperContentError(self.name, 'ContentError: unable to retrieve values', traceback.format_exc())
        except WebScraperContentError as err:
            raise WebScraperContentError(err.name, err.err, err.trace)
        except Exception as e:
            raise WebScraperParseError(self.name, 'ParseError: unable to retrieve values', traceback.format_exc())
        return raw_data

    def magnet_link_scrapper(self, content):
        return
