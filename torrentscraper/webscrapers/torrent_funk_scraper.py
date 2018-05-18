#!/usr/bin/env python3

# Import System Libraries
import traceback
import logging

# Import External Libraries
from bs4 import BeautifulSoup

# Import Custom Data Structure
from torrentscraper.datastruct.rawdata_instance import RAWDataInstance

# Import Custom Exceptions
from torrentscraper.webscrapers.exceptions.webscraper_error import WebScraperProxyListError
from torrentscraper.webscrapers.exceptions.webscraper_error import WebScraperParseError
from torrentscraper.webscrapers.exceptions.webscraper_error import WebScraperContentError

# Constants
from lib.fileflags import FileFlags as fflags

FILM_FLAG = fflags.FILM_DIRECTORY_FLAG
SHOW_FLAG = fflags.SHOW_DIRECTORY_FLAG
ANIME_FLAG = fflags.ANIME_DIRECTORY_FLAG

class TorrentFunkScraper(object):
    def __init__(self, logger):
        self.name = self.__class__.__name__
        self.logger = logger
        self.proxy_list = ['https://torrentfunk.unblocked.mx','https://www.torrentfunk.com']
        self._proxy_list_length = len(self.proxy_list)
        self._proxy_list_pos = 0
        self.cloudflare_cookie = False
        self.query_type = False
        self.disable_quality = False
        self.thread_defense_bypass_cookie = False
        self.torrent_file = True
        self.magnet_link = False

        self.default_params = {}
        self.main_page = self.proxy_list[self._proxy_list_pos]
        self.default_search = '/all/torrents/'
        self.default_tail = '.html'
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

    def get_raw_data(self, content=None,):
        raw_data = RAWDataInstance()
        soup = BeautifulSoup(content, 'html.parser')

        try:
            # Retrieving individual values from the search result
            ttable = soup.findAll('table', {'class':'tmain'})
            if ttable != []:
                self.logger.info('{0} Retrieving Raw Values from Search Result Response:'.format(self.name))
                for items in ttable:
                    tbody = items.findAll('tr')
                    for tr in tbody[1:]:
                        seed = (tr.findAll('td'))[3].text
                        if seed == '0':
                            seed = '1'

                        leech = (tr.findAll('td'))[4].text
                        if leech == '0':
                            leech = '1'

                        # Converting GB to MB, to Easily Manage The Pandas Structure
                        size = (tr.findAll('td'))[2].text
                        if 'MB' in size:
                            size = float(size[:-2])
                        elif 'GB' in size:
                            size = float(size[:-2]) * 1000

                        magnet_link = (tr.findAll('a'))[0]['href']

                        # Patch to Avoid Getting False Torrents
                        if int(seed) < 1500:
                            raw_data.add_magnet(str(magnet_link))
                            raw_data.add_seed(int(seed))
                            raw_data.add_leech(int(leech))
                            raw_data.add_size(int(size))
                            self.logger.debug('{0} New Entry Raw Values: {1:7} {2:>4}/{3:4} {4}'.format(self.name,
                                                                                                          str(int(size)),
                                                                                                          str(seed),
                                                                                                          str(leech),
                                                                                                          magnet_link))
            else:
                raise WebScraperContentError(self.name, 'ContentError: unable to retrieve values',
                                             traceback.format_exc())
        except WebScraperContentError as err:
            raise WebScraperContentError(err.name, err.err, err.trace)
        except Exception as err:
            raise WebScraperParseError(self.name, err, traceback.format_exc())
        return raw_data

    def get_magnet_link(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        try:
            content = (soup.findAll('div',{'class':'content'}))
            if content != []:
                magnet = content[2].findAll('a')[1]['href']

            else:
                raise WebScraperContentError(self.name, 'ContentError: unable to retrieve values', traceback.format_exc())
        except WebScraperContentError as err:
            raise WebScraperContentError(err.name, err.err, err.trace)
        except Exception as err:
            raise WebScraperParseError(self.name, 'ParseError: unable to retrieve values', traceback.format_exc())
        return magnet


