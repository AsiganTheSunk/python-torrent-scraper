#!/usr/bin/env python3

# Import System Libraries
from collections.abc import Mapping
import os

# Import External Libraries
from colorama import Fore, Style
from lib.fileflags import FileFlags as fflags

class WebSearchInstance(Mapping):
    def __init__(self, title='', year='', season='', episode='', quality='', source='', search_type='', lower_size_limit=-1, upper_size_limit=-1, ratio_limit=-1):
        self.search_type = search_type
        self.lower_size_limit = lower_size_limit
        self.upper_size_limit = upper_size_limit
        self.ratio_limit = ratio_limit
        self.quality = quality
        self.title = title
        self.year = year
        self.season = season
        self.episode = episode
        self.source = source
        self._storage = {'search_type': self.search_type,
                         'lower_size_limit': self.lower_size_limit,
                         'upper_size_limit': self.upper_size_limit,
                         'ratio_limit': self.ratio_limit,
                         'quality': self.quality,
                         'title': self.title,
                         'year': self.year,
                         'season': self.season,
                         'episode': self.episode,
                         'source': self.source}

    def __getitem__(self, key):
        if key == 'alpha_tango_shit':
            return
        return self._storage[key]

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)

    def validate(self):
        if self.search_type == fflags.ANIME_DIRECTORY_FLAG:
            self.season = ''
            self.year = ''
            if len(self.episode) == 1:
                self.episode = '0' + str(self.episode)

        elif self.search_type == fflags.FILM_DIRECTORY_FLAG:
            self.season = ''
            self.episode = ''
            self.source = ''

        elif self.search_type == fflags.SHOW_DIRECTORY_FLAG:
            self.source = ''
            self.year = ''
            if len(self.episode) == 1:
                self.episode = '0' + str(self.episode)
            if len(self.season) == 1:
                self.season = '0' + str(self.season)

        return self
    # def __repr__(self):
    #     '''
    #     This function, overrides the default function method.
    #     :return: this function, returns every component in the magnet instance
    #     :rtype: str
    #     '''
    #     return

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
        self.source = value