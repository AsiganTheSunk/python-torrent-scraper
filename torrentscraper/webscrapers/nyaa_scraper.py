#!/usr/bin/env python3

# Import External Libraries
from NyaaPy.utils import Utils
from bs4 import BeautifulSoup

# Import System Libraries
import traceback

# Import Custom Data Structure
from torrentscraper.datastruct.rawdata_instance import RAWDataInstance

# Import Custom Exceptions
from torrentscraper.webscrapers.exceptions.webscraper_error import WebScraperParseError
from torrentscraper.webscrapers.exceptions.webscraper_error import WebScraperContentError
from torrentscraper.webscrapers.exceptions.webscraper_error import WebScraperProxyListError

# Import Custom Constants
from lib.fileflags import FileFlags as fflags


class NyaaScraper(object):
    def __init__(self, logger):
        self.name = self.__class__.__name__

        # CustomLogger
        self.logger = logger

        # Scraper Configuration Parameters
        self.query_type = True
        self.batch_style = False
        self.cloudflare_cookie = False
        self.thread_defense_bypass_cookie = False

        # Supported FileFlags
        self.supported_searchs = [fflags.ANIME_DIRECTORY_FLAG]

        # Sleep Limit, for connections to the web source
        self.safe_sleep_time = [0.500, 1.250]

        # ProxyList Parameters
        self.proxy_list = ['http://nyaa.si']
        self._proxy_list_pos = 0
        self._proxy_list_length = len(self.proxy_list)
        self.main_page = self.proxy_list[self._proxy_list_pos]

        # Uri Composition Parameters
        self.default_search = '/'
        self.default_tail = ''
        self.default_params = {'f': '0', 'c:': '0_0', 'p': '0'}

        # Hop Definitions
        self.hops = []
        self.batch_hops = []

    def update_main_page(self):
        '''

        :return:
        '''
        try:
            value = self._proxy_list_pos
            if self._proxy_list_length > self._proxy_list_pos:
                value += 1

            self._proxy_list_pos = value
            self.main_page = self.proxy_list[self._proxy_list_pos]
        except IndexError as err:
            raise WebScraperProxyListError(self.name, err, traceback.format_exc())

    def get_raw_data(self, content=None):
        '''

        :param content:
        :return:
        '''
        raw_data = RAWDataInstance()
        soup = BeautifulSoup(content, 'html.parser')

        try:
            ttable = soup.select('table tr')
            if ttable != []:
                try:
                    dict_result = Utils.parse_nyaa(ttable, limit=None)

                    for item in dict_result:
                        size = item['size']
                        if 'MiB' in size:
                            size = size.replace('MiB', 'MB')
                            size = float(size[:-2])
                        elif 'GiB' in size:
                            size = size.replace('GiB', 'GB')
                            size = float(size[:-2]) * 1000

                        seed = str(item['seeders'])
                        if seed == '0':
                            seed = '1'
                        leech = str(item['leechers'])
                        if leech == '0':
                            leech = '1'

                        magnet_link = item['magnet']

                        raw_data.add_new_row(size, seed, leech, magnet_link)
                        self.logger.debug('{0} New Entry Raw Values: {1:7} {2:>4}/{3:4} {4}'.format(
                            self.name, str(size), str(seed), str(leech), magnet_link))
                except Exception as err:
                    raise WebScraperParseError(self.name, 'ParseError: unable to retrieve values: {0}'.format(err),
                                               traceback.format_exc())
        except Exception as err:
            raise WebScraperContentError(self.name, 'ContentError: unable to retrieve values {0}'.format(err),
                                         traceback.format_exc())
        return raw_data

    def magnet_link_scrapper(self, content):
        return
