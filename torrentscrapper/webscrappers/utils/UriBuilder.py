#!/usr/bin/env python

import urllib.parse

SEASON_WRAP = -1
EPISODE_WRAP = 0

class UriBuilder():
    def __init__(self):
        self.name = self.__class__.__name__

    def build_request_url(self, websearch, webscraper, verbose=False, debug=False):
        search_params = {}
        search_query = None
        if webscraper.disable_quality:
            websearch.quality = ''

        search_query = ({'q':'{header} {title} {year} {season}{episode} {quality}'.format(
                header=websearch.header,
                title=websearch.title,
                year=websearch.year,
                season=self.eval_wrapped_key(value=websearch.season, wrap_type=SEASON_WRAP, category=None),
                episode=self.eval_wrapped_key(value=websearch.episode, wrap_type=EPISODE_WRAP, category=None),
                quality=websearch.quality).strip()})

        if webscraper.default_params != {}:
            search_params = {**search_query, **webscraper.default_params}
        else:
            search_params = search_query

        if debug:
            print('%s:' % (self.name))
            for item in search_params:
                print((' [ %s : %s ]') % (item, search_params[item] ))

        if webscraper.query_type:
            search_uri = '%s%s?%s' % (webscraper.main_page, webscraper.default_search, (urllib.parse.urlencode(search_params)))
        else:
            search_uri = '%s%s%s%s' % (webscraper.main_page, webscraper.default_search, (search_params['q']).replace(' ','%20').replace('&','and'), webscraper.default_tail)

        if (verbose or debug):
            print('%s:\n [ %s ]' % (self.name, search_uri))
        return search_uri

    def eval_wrapped_key(self, value, wrap_type, category=None):
        '''
        This function peform auxiliary help to the build name functions validating the content of the string
        :param value: It represents the key you're testing
        :param wrap_type: It represents the type of wrapping the string it's going to get, numbers 0 to 2, being
                        0 for [value], 1 for (value), 2 for -(value) 3 value
        :return: modified value
        '''
        if value is None:
            return ''
        else:
            if wrap_type is -1:
                if value is '':
                    return value
                return ('S' + value)
            elif wrap_type is 0:
                if value is '':
                    return value
                return ('E' + value)
            else:
                return value
