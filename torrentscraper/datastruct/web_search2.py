#!/usr/bin/env python

from colorama import Fore, Style
import os
from collections.abc import Mapping

class WebSearch(Mapping):
    def __init__(self, title='', year='', season='', episode='', quality='', header='', search_type='', size_limit=''):
        self.search_type = search_type
        self.size_limit = size_limit
        self.quality = quality
        self.title = title
        self.year = year
        self.season = season
        self.episode = episode
        self.header = header
        self._storage = {'search_type': self.search_type,
                         'size_limit': self.size_limit,
                         'quality': self.quality,
                         'title': self.title,
                         'year': self.year,
                         'season': self.season,
                         'episode': self.episode,
                         'header': self.header}

        # Add list of Torrent, related to this, so we can access the contents of this
        # object, based only on the specific search that has been done

    def __getitem__(self, key):
        if key == 'alpha_tango_shit':
            return
        return self._storage[key]

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)

    def __repr__(self):
        '''
        This function, overrides the default function method.
        :return: this function, returns every component in the magnet instance
        :rtype: str
        '''
        return



    def set_search_type(self, value):
        self.search_type = value

    def set_quality(self, value):
        self.quality = value

    def set_title(self, value):
        self.title = value

    def set_year(self, value):
        self.year = value

    def set_season(self, value):
        self.season = value

    def set_episode(self, value):
        self.episode = value

    def set_header(self, value):
        self.header = value