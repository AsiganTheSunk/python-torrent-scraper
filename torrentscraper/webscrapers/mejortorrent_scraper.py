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

# Import Custom
from lib.fileflags import FileFlags as fflags

class MejorTorrentScraper():
    def __init__(self, logger):
        self.name = self.__class__.__name__

        # CustomLogger
        self.logger = logger

        # Scraper Configuration Parameters
        self.batch_style = True
        self.query_type = True
        self.cloudflare_cookie = False
        self.thread_defense_bypass_cookie = False


        # Supported FileFlags
        self.supported_searchs = [fflags.FILM_DIRECTORY_FLAG, fflags.SHOW_DIRECTORY_FLAG]

        # Sleep Limit, for connections to the web source
        self.safe_sleep_time = [0.500, 1.250]

        # ProxyList Parameters
        self.proxy_list = ['http://www.mejortorrent.com']
        self._proxy_list_pos = 0
        self._proxy_list_length = len(self.proxy_list)
        self.main_page = self.proxy_list[self._proxy_list_pos]

        # Uri Composition Parameters
        self.default_search = '/secciones.php'
        self.default_tail = ''
        self.default_params = {'sec':'buscador'}

        # Hop Definitions
        self.batch_hops = [self.get_torrent_link_batch, self.get_torrent_info]
        self.hops = [self.get_torrent_link, self.get_torrent_info]

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
            ttable = soup.findAll('tr')
            for index, item in enumerate(ttable[34:-14]):
                try:
                    magnet_link = item.findAll('a')[0]['href']
                    raw_data.add_new_row(magnet=magnet_link)
                    self.logger.debug0('{0} New Entry Raw Values: {1:7} {2:>4}/{3:4} {4}'.format(
                        self.name, str(int(0)), str(1), str(1), magnet_link))

                except Exception as err:
                    raise WebScraperParseError(self.name, 'ParseError: unable to retrieve values {0}'.format(err),
                                               traceback.format_exc())
        except Exception as err:
            raise WebScraperContentError(self.name, 'ContentError: unable to retrieve values {0}'.format(err),
                                         traceback.format_exc())


        return raw_data

    def get_torrent_link_batch(self, content, websearch, hop, *args):
        '''

        :param content:
        :param websearch:
        :param hop:
        :param args:
        :return:
        '''
        soup = BeautifulSoup(content, 'html.parser')
        try:
            surrogated_id = ''
            surrogated_list = []
            ttable = soup.findAll('table')
            for index, item in enumerate(ttable[19:-3]):
                try:
                    surrogated_id = hop.split('-')[3:-(len(hop.split('-')[3:]) -2)]
                    surrogated_id = surrogated_id[0]+surrogated_id[1]
                    id = item.findAll('a')[0]['href']
                    single_link_pattern = '/secciones.php?sec=descargas&ap=contar&tabla=series&id={0}'.format(id.split('-')[4])
                    self.logger.debug('{0} - {1}::{2} : {3}'.format(self.name, 'Batch_Mode Single-iD', id, single_link_pattern))
                    surrogated_list.append(single_link_pattern)

                except Exception as err:
                    raise WebScraperParseError(self.name, 'ParseError: unable to retrieve values: {0}'.format(err), traceback.format_exc())
            return surrogated_list, surrogated_id

        except Exception as err:
            raise WebScraperContentError(self.name, 'ContentError: unable to retrieve values {0}'.format(err),
                                         traceback.format_exc())


    def get_torrent_link(self, content, websearch, *args):
        soup = BeautifulSoup(content, 'html.parser')
        if websearch.search_type == fflags.FILM_DIRECTORY_FLAG:
            try:
                link = ''
                tr = soup.findAll('tr')
                for index, item in enumerate(tr[32:-1]):
                    try:
                        link = item.findAll('a')[0]['href']
                    except Exception as err:
                        raise WebScraperParseError(self.name, 'ParseError: unable to retrieve values: {0}'.format(err),
                                                   traceback.format_exc())
            except Exception as err:
                raise WebScraperContentError(self.name, 'ContentError: unable to retrieve values {0}'.format(err),
                                                 traceback.format_exc())
            return '/' + link
        else:
            try:
                ttable = soup.findAll('table')
                for index, item in enumerate(ttable[19:-3]):
                    try:
                        if websearch.episode != '':
                            id = item.findAll('a')[0]['href']
                            single_link_pattern = '/secciones.php?sec=descargas&ap=contar&tabla=series&id={0}'.format(
                                id.split('-')[4])

                            if '{0}x{1}'.format(websearch.season[1:], websearch.episode) in \
                                    id.split('-')[(len(id.split('-')) - 1):][0]:
                                self.logger.debug('{0} - {1}::{2} : {3}'.format(self.name, 'Normal_Mode Single-iD', id, single_link_pattern))
                                return single_link_pattern

                    except Exception as err:
                        raise WebScraperParseError(self.name, 'ParseError: unable to retrieve values: {0}'.format(err),
                                                   traceback.format_exc())
            except Exception as err:
                raise WebScraperContentError(self.name, 'ContentError: unable to retrieve values {0}'.format(err),
                                                 traceback.format_exc())

    def get_torrent_info(self, content, *args):
        soup = BeautifulSoup(content, 'html.parser')
        torrent_file = ''
        try:
            ttable = soup.findAll('table')
            try:
                # Retrieving the Link to the Torrent File
                torrent_file = ttable[15].select('a')[0]['href']

                # Normalize output, because this web is inconsistent with it, removing the default_proxy_url
                if self.proxy_list[self._proxy_list_pos] in torrent_file:
                    torrent_file =  torrent_file[len(self.proxy_list[self._proxy_list_pos]):]
            except Exception as err:
                raise WebScraperParseError(self.name, 'ParseError: unable to retrieve values: {0}'.format(err),
                                           traceback.format_exc())
        except Exception as err:
            raise WebScraperContentError(self.name, 'ContentError: unable to retrieve values {0}'.format(err),
                                         traceback.format_exc())
        return torrent_file
