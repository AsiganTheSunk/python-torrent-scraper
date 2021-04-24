#!/usr/bin/env python3

import urllib.parse

from core.constants.fileflags import FileFlags

SEASON_WRAP = -1
EPISODE_WRAP = 0


class UriBuilder:
    def __init__(self):
        self.name = self.__class__.__name__

    def build_request_url(self, web_scraper, web_search):
        """
        This function performs the construction of a custom uri, for the WebScraper that is being used in the call.
        :param web_search: this value, represents the items used in the construction of the custom uri
        :type web_search: websearch
        :param web_scraper: this value, represents the WebScraper you're using
        :type web_scraper: WebScraper
        :return: this function, returns the custom uri created for the request
        :rtype: str
        """
        search_params = {}
        search_query = None
        if web_scraper.disable_quality:
            web_search.quality = ''

        search_query = ({'q': '{header} {title} {year} {season}{episode} {quality}'.format(
                header=web_search.source,
                title=web_search.title,
                year=web_search.year,
                season=self.eval_wrapped_key(value=web_search.season, wrap_type=SEASON_WRAP, search_type=None),
                episode=self.eval_wrapped_key(value=web_search.episode, wrap_type=EPISODE_WRAP, search_type=web_search.search_type),
                quality=web_search.quality).strip()})

        if web_scraper.default_params != {}:
            search_params = {**search_query, **web_scraper.default_params}
        else:
            search_params = search_query

        # self.logger.debug('{0} Query Params:'.format(self.name))
        # for item in search_params:
        #     self.logger.debug('[ {0} : {1} ]'.format(item, search_params[item]))

        if web_scraper.query_type:
            search_uri = '{0}{1}?{2}'.format(web_scraper.main_page, web_scraper.default_search,
                                             (urllib.parse.urlencode(search_params)))
        else:
            search_uri = '{0}{1}{2}{3}'.format(web_scraper.main_page, web_scraper.default_search,
                                               (search_params['q']).replace(' ', '%20').replace('&', 'and'),
                                               web_scraper.default_tail)
        # self.logger.debug0('{0} Generated Uri from Query Params: [ {1} ]'.format(self.name, search_uri))
        return search_uri

    @staticmethod
    def eval_wrapped_key(value, wrap_type, search_type=None):
        """
        This function peform auxiliary help to the build name functions validating the content of the string
        :param search_type:
        :param value: It represents the key you're testing
        :type value: str
        :param wrap_type: It represents the type of wrapping the string it's going to get, numbers 0 to 2, being 0
        for [value], 1 for (value), 2 for -(value) 3 value
        :type wrap_type: int
        :return: modified value
        :rtype: str
        """
        if value is None:
            return ''
        else:
            if wrap_type == -1:
                if value == '':
                    return value
                return 'S' + value
            elif wrap_type == 0:
                if value == '' or search_type is FileFlags.ANIME_DIRECTORY_FLAG:
                    return value
                return 'E' + value
            else:
                return value
