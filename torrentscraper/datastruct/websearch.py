#!/usr/bin/env python

class RAWData(object):
    def __init__(self):
        self.size_list = []
        self.seed_list = []
        self.leech_list = []
        self.magnet_list = []

    def add_size(self, value):
        self.size_list.append(value)

    def add_seed(self, value):
        self.seed_list.append(value)

    def add_leech(self, value):
        self.leech_list.append(value)

    def add_magnet(self, value):
        self.magnet_list.append(value)

    def list(self):
        struct = zip(self.size_list, self.seed_list, self.leech_list, self.magnet_list)
        print('{0:^7} {1:>4}/{2:4} {3} '.format('SIZE', 'SEED', 'LEECH', 'MAGNET'))
        for size, seed, leech, magnet in struct:
            print('{0:7} {1:>4}/{2:4} {3} '.format(str(size), str(seed), str(leech), magnet))
        return


class WebSearch:
    def __init__(self, title='', year='', season='', episode='', quality='', header='', search_type='', lower_size_limit=-1, upper_size_limit=-1 ,ratio_limit=-1):
        self.search_type = search_type
        self.quality = quality
        self.title = title
        self.year = year
        self.season = season
        self.episode = episode
        self.header = header
        self.lower_size_limit = lower_size_limit
        self.upper_size_limit = upper_size_limit
        self.ratio_limit = ratio_limit

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

    def set_size_limit(self, value):
        self.size_limit = value