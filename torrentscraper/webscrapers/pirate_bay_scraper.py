#!/usr/bin/env python

# Import System Libraries
import traceback

# Import External Libraries
from bs4 import BeautifulSoup

# Import Custom Data Structure
from torrentscraper.datastruct.rawdata_instance import RAWDataInstance

# Import Custom Exceptions
from torrentscraper.webscrapers.exceptions.webscraper_error import WebScraperProxyListError
from torrentscraper.webscrapers.exceptions.webscraper_error import WebScraperParseError
from torrentscraper.webscrapers.exceptions.webscraper_error import WebScraperContentError

# Constants
FILM_FLAG = 'FILM'
SHOW_FLAG = 'SHOW'
ANIME_FLAG = 'ANIME'

class PirateBayScraper():
    def __init__(self, logger):
        self.name = self.__class__.__name__
        self.logger = logger
        self.proxy_list = ['https://unblockedbay.info', 'https://ukpirate.org', 'https://thehiddenbay.info']
        self._proxy_list_length = len(self.proxy_list)
        self._proxy_list_pos = 0
        self.cloudflare_cookie = False
        self.query_type = True
        self.disable_quality = False
        self.thread_defense_bypass_cookie = False
        self.torrent_file = False
        self.magnet_link = True

        self.main_page = self.proxy_list[self._proxy_list_pos]
        self.default_search = '/s/'
        self.default_tail = ''
        self.default_params = {'category':'0', 'page':'0', 'orderby':'99'}
        self.supported_searchs = [FILM_FLAG, SHOW_FLAG, ANIME_FLAG]

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

                        magnet_link = (tr.findAll('a'))[2]['href']

                        raw_data.add_magnet(str(magnet_link))
                        raw_data.add_size(size)
                        raw_data.add_seed(seed)
                        raw_data.add_leech(leech)
                        self.logger.debug('{0} New Entry Raw Values: {1:7} {2:>4}/{3:4} {4}'.format(self.name,
                                                                                                      str(size),
                                                                                                      str(seed),
                                                                                                      str(leech),
                                                                                                      magnet_link))
            else:
                raise WebScraperContentError(self.name, 'ContentError: unable to retrieve values', traceback.format_exc())
        except WebScraperContentError as err:
            raise WebScraperContentError(err.name, err.err, err.trace)
        except Exception as e:
            raise WebScraperParseError(self.name, 'ParseError: unable to retrieve values', traceback.format_exc())
        return raw_data

    # TODO MECANICA DE RECONEXION POR FALLO EN RECUPERACION DE MAGNET
    def get_magnet_link(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        try:
            content = (soup.findAll('div',{'class':'download'}))
            if content != []:
                magnet = content[0].findAll('a')[0]['href']
            else:
                raise WebScraperContentError(self.name, 'ParseError: unable to retrieve values', traceback.format_exc())
        except WebScraperContentError as err:
            raise WebScraperContentError(err.name, err.err, err.trace)
        except Exception as e:
            raise WebScraperParseError(self.name, 'ParseError: unable to retrieve values', traceback.format_exc())
        return magnet
