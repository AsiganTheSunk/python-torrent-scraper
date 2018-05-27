#!/usr/bin/env python3

class RAWDataInstance(object):
    def __init__(self):
        self.size_list = []
        self.seed_list = []
        self.leech_list = []
        self.magnet_list = []
        self.surrogated_list = []

    def add_new_row(self, size='0', seed='1', leech='1', magnet='', surrogated_id='NaN'):
        self.size_list.append(str(int(size)))
        self.seed_list.append(str(int(seed)))
        self.leech_list.append(str(int(leech)))
        self.magnet_list.append(str(magnet))
        self.surrogated_list.append(surrogated_id)

    def list(self):
        struct = zip(self.size_list, self.seed_list, self.leech_list, self.magnet_list, self.surrogated_list)
        print('{0:^7} {1:>4}/{2:4} {3} {4}'.format('SIZE', 'SEED', 'LEECH', 'MAGNET', 'SURROGATED_ID'))
        for size, seed, leech, magnet, surrogated_id in struct:
            print('{0:7} {1:>4}/{2:4} {3} {4}'.format(str(size), str(seed), str(leech), magnet, surrogated_id))
        return
