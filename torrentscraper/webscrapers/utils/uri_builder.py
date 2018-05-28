#!/usr/bin/env python3

# Import System Libraries
import urllib.parse

# Import Custom Constant
from lib.fileflags import FileFlags as fflags

# Constants
SEASON_WRAP = -1
EPISODE_WRAP = 0
TEMPORADA_WRAP = 1
SPECIAL_WEBSCRAPER = 'MejorTorrentScraper'


class UriBuilder(object):
    def __init__(self, logger):
        self.name = self.__class__.__name__

        # Custom Logger
        self.logger = logger

    def build_request_url(self, websearch, webscraper):
        '''
        This function performs the construction of a custom uri, for the WebScraper that is being used in the call.
        :param websearch: this value, represents the items used in the construction of the custom uri
        :type websearch: websearch
        :param webscraper: this value, represents the WebScraper you're using
        :type webscraper: WebScraper
        :return: this function, returns the custom uri created for the request
        :rtype: str
        '''
        search_query = {}
        search_params = {}
        search_uri_list = []

        if webscraper.name == SPECIAL_WEBSCRAPER:
            search_query = self._get_mjrt_url(websearch)
        else:
            search_query = self._get_general_url(websearch)

        if webscraper.default_params != {}:
            search_params = {**search_query, **webscraper.default_params}
        else:
            search_params = search_query

        self.logger.debug('{0} Query Params:'.format(self.name))
        for item in search_params:
            self.logger.debug('[ {0} : {1} ]'.format(item, search_params[item]))

        if webscraper.query_type:
            search_uri = '{0}{1}?{2}'.format(webscraper.main_page, webscraper.default_search, (
                urllib.parse.urlencode(search_params)))
        else:
            search_uri = '{0}{1}{2}{3}'.format(webscraper.main_page, webscraper.default_search, (
                search_params['q']).replace(' ','%20').replace('&','and'), webscraper.default_tail)

        self.logger.debug0('{0} Generated Uri from Query Params: [ {1} ]'.format(self.name, search_uri))
        return search_uri

    def _get_mjrt_url(self, websearch):
        '''

        :param websearch:
        :return:
        '''
        if websearch.search_type == fflags.FILM_DIRECTORY_FLAG:
            return {'valor': '{0}'.format(websearch.title)}
        else:
            if websearch.season != '':
                return {'valor': '{0} - {1}'.format(websearch.title, websearch.season[-1:])}
            else:
                return {'valor': '{0}'.format(websearch.title)}

    def _get_general_url(self, websearch):
        '''

        :param websearch:
        :return:
        '''
        if websearch.search_type == fflags.FILM_DIRECTORY_FLAG:
            return {'q': '{0} {1} {2}'.format(
                websearch.title, websearch.year, websearch.quality.strip())}

        elif websearch.search_type == fflags.ANIME_DIRECTORY_FLAG:
            return ({'q': '{0} {1} {2} {3}'.format(
                websearch.source, websearch.title, websearch.episode, websearch.quality).strip()})

        elif websearch.search_type == fflags.SHOW_DIRECTORY_FLAG:
            if websearch.season != '' and websearch.episode != '':
                return {'q': '{0} S{1}E{2} {3}'.format(
                    websearch.title, websearch.season, websearch.episode, websearch.quality).strip()}
            else:
                return {'q': '{0} Season {1} {2}'.format(
                    websearch.title, websearch.season[1:], websearch.quality).strip()}
