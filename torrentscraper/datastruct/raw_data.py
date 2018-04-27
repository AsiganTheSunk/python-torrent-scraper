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
