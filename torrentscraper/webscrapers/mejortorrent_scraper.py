#!/usr/bin/env python3

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
from lib.fileflags import FileFlags as fflags

class MejorTorrentScraper():
    def __init__(self, logger):
        self.name = self.__class__.__name__
        self.logger = logger
        self.proxy_list = ['http://www.mejortorrent.com']
        self.supported_searchs = [fflags.FILM_DIRECTORY_FLAG, fflags.SHOW_DIRECTORY_FLAG]
        self._proxy_list_length = len(self.proxy_list)
        self._proxy_list_pos = 0
        self.cloudflare_cookie = False
        self.query_type = True
        self.disable_quality = True
        self.thread_defense_bypass_cookie = False
        self.torrent_file = True
        self.magnet_link = False

        self.main_page = self.proxy_list[self._proxy_list_pos]
        self.default_search = '/secciones.php'
        self.default_tail = ''
        self.default_params = {'sec':'buscador'}
        self.hops = [self.get_magnet_link, self.get_magnet_clickhere]

    def update_main_page(self):
        pass
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
            ttable = soup.findAll('tr')
            for index, item in enumerate(ttable[34:-14]):
                try:
                    magnet_link = item.findAll('a')[0]['href']
                    raw_data.add_new_row(magnet=magnet_link)
                    self.logger.debug0('{0} New Entry Raw Values: {1:7} {2:>4}/{3:4} {4}'.format(
                        self.name, str(int(0)), str(1), str(1), magnet_link))
                except WebScraperContentError as err:
                    raise WebScraperContentError(err.name, err.err, err.trace)
        except Exception as e:
            raise WebScraperParseError(self.name, 'ParseError: unable to retrieve values', traceback.format_exc())
        return raw_data

    def get_magnet_link(self, content, websearch):
        soup = BeautifulSoup(content, 'html.parser')
            # Retrieving individual raw values from the search result
        if websearch.search_type == fflags.FILM_DIRECTORY_FLAG:
            tr = soup.findAll('tr')
            for index, item in enumerate(tr[32:-1]):
                try:
                    link = item.findAll('a')[0]['href']
                except Exception as err:
                    raise WebScraperParseError(self.name, 'ParseError: unable to retrieve values: {0}'.format(err),
                                               traceback.format_exc())
                return '/' + link
        else:
            ttable = soup.findAll('table')
            try:
                for index, item in enumerate(ttable[19:-3]):
                    # try:
                    id = item.findAll('a')[0]['href']
                    print('index id: ', id)
                    magnet_link = '/secciones.php?sec=descargas&ap=contar&tabla=series&id={0}'.format(id.split('-')[4])
                    self.logger.warning('{0} - - {1}'.format(self.name, magnet_link))
                    print('status: ',id, magnet_link)
                    if 'x{0}'.format(websearch.episode) in id:
                        return magnet_link
                    # else: # Batch Mode
                    #    tmp_magnet_list.append(magnet_link)
            except Exception as err:
                print(self.name, 'get_magnet_link()', err)


        # except Exception as err:
        #     raise WebScraperContentError(self.name, 'ContentError: unable to retrieve values {0}'.format(err),
        #                                  traceback.format_exc())

    def get_magnet_clickhere(self, content, websearh):
        soup = BeautifulSoup(content, 'html.parser')
        magnet = ''
        try:
            ttable = soup.findAll('table')
            # for index, item in enumerate(ttable):
            #     print('index: ', index, 'item: \n', item)
            try:
                try:
                    magnet = ttable[15].select('a')[0]['href']
                    if self.proxy_list[self._proxy_list_pos] in magnet:
                        magnet =  magnet[len(self.proxy_list[self._proxy_list_pos]):]

                    self.logger.warning('{0} - - {1}'.format(self.name, magnet))
                    return magnet
                except Exception as err:
                    pass
            except Exception as err:
                raise WebScraperParseError(self.name, 'ParseError: unable to retrieve values: {0}'.format(err),
                                           traceback.format_exc())
        except Exception as err:
            raise WebScraperContentError(self.name, 'ContentError: unable to retrieve values {0}'.format(err),
                                         traceback.format_exc())
