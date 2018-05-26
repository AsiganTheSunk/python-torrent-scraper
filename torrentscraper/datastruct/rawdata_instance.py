#!/usr/bin/env python3

class RAWDataInstance(object):
    def __init__(self):
        self.size_list = []
        self.seed_list = []
        self.leech_list = []
        self.magnet_list = []

    def add_new_row(self, size='0', seed='1', leech='1', magnet=''):
        self.size_list.append(str(int(size)))
        self.seed_list.append(str(int(seed)))
        self.leech_list.append(str(int(leech)))
        self.magnet_list.append(str(magnet))

    def list(self):
        struct = zip(self.size_list, self.seed_list, self.leech_list, self.magnet_list)
        print('{0:^7} {1:>4}/{2:4} {3} '.format('SIZE', 'SEED', 'LEECH', 'MAGNET'))
        for size, seed, leech, magnet in struct:
            print('{0:7} {1:>4}/{2:4} {3} '.format(str(size), str(seed), str(leech), magnet))
        return
