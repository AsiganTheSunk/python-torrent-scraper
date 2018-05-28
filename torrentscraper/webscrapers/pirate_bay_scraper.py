#!/usr/bin/env python3

# Import System Libraries
import traceback

# Import External Libraries
from bs4 import BeautifulSoup

# Import Custom Data Structure
from torrentscraper.datastruct.rawdata_instance import RAWDataInstance

# Import Custom Exceptions
from torrentscraper.webscrapers.exceptions.webscraper_error import WebScraperParseError
from torrentscraper.webscrapers.exceptions.webscraper_error import WebScraperContentError
from torrentscraper.webscrapers.exceptions.webscraper_error import WebScraperProxyListError

# Import Custom Constants
from lib.fileflags import FileFlags as fflags


class PirateBayScraper(object):
    def __init__(self, logger):
        self.name = self.__class__.__name__

        # CustomLogger
        self.logger = logger

        # Scraper Configuration Parameters
        self.query_type = True
        self.cloudflare_cookie = False
        self.thread_defense_bypass_cookie = False

        # Supported FileFlags
        self.supported_searchs = [fflags.FILM_DIRECTORY_FLAG, fflags.SHOW_DIRECTORY_FLAG]

        # Sleep Limit, for connections to the web source
        self.safe_sleep_time = [0.500, 1.250]

        # ProxyList Parameters
        self.proxy_list = ['https://unblockedbay.info', 'https://ukpirate.org', 'https://thehiddenbay.info']
        self._proxy_list_pos = 0
        self._proxy_list_length = len(self.proxy_list)
        self.main_page = self.proxy_list[self._proxy_list_pos]

        # Uri Composition Parameters
        self.default_search = '/s/'
        self.default_tail = ''
        self.default_params = {'category':'0', 'page':'0', 'orderby':'99'}

        # Hop Definitions
        self.hops = [self.get_magnet_info]
        self.batch_hops = []

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
            # Retrieving individual raw values from the search result
            ttable = soup.findAll('table', {'id': 'searchResult'})
            if ttable != []:
                try:
                    self.logger.info('{0} Retrieving Raw Values from Search Result Response:'.format(self.name))
                    for items in ttable:
                        tbody = items.findAll('tr')
                        for tr in tbody[1:]:

                            seed = (tr.findAll('td'))[2].text
                            if seed == '0':
                                seed = '1'
                            leech = (tr.findAll('td'))[3].text
                            if leech == '0':
                                leech = '1'

                            size_string = (tr.findAll('font',{'class':'detDesc'}))
                            size = (size_string[0].text).split(',')[1][6:]

                            # Converting GB to MB, to easily manage the pandas structure
                            if 'MiB' in size:
                                size = size.replace('MiB','MB')
                                size = float(size[:-2])
                            elif 'GiB' in size:
                                size = size.replace('GiB', 'GB')
                                size = float(size[:-2]) * 1000
                            elif 'B' in size:
                                size = float(size[:-2]) * 0.000001

                            magnet_link = (tr.findAll('a'))[2]['href']
                            if size > 1:
                                raw_data.add_new_row(size, seed, leech, magnet_link)
                            self.logger.debug0('{0} New Entry Raw Values: {1:7} {2:>4}/{3:4} {4}'.format(
                                self.name, str(int(size)), str(seed), str(leech), magnet_link))
                except Exception as err:
                    raise WebScraperParseError(self.name, 'ParseError: unable to retrieve values: {0}'.format(err),
                                               traceback.format_exc())
        except Exception as err:
            raise WebScraperContentError(self.name, 'ContentError: unable to retrieve values {0}'.format(err),
                                         traceback.format_exc())
        return raw_data

    def get_magnet_info(self, content, *args):
        soup = BeautifulSoup(content, 'html.parser')
        magnet = ''
        try:
            content = (soup.findAll('div',{'class':'download'}))
            if content!=[]:
                try:
                    magnet = content[0].findAll('a')[0]['href']
                    print('entra aqui por yisus: ', magnet)
                    return magnet
                except Exception as err:
                    raise WebScraperParseError(self.name, 'ParseError: unable to retrieve values: {0}'.format(err),
                                               traceback.format_exc())
        except Exception as err:
            raise WebScraperContentError(self.name, 'ContentError: unable to retrieve values {0}'.format(err),
                                         traceback.format_exc())

