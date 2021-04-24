#!/usr/bin/env python3

from typing import List


class RAWDataInstance:
    def __init__(self, web_scraper):
        self.web_scraper = web_scraper
        self.seed_list = []
        self.leech_list = []
        self.size_list = []
        self.resource_link_list = []

    def get_row_data(self, resource_index):
        return self.resource_link_list[resource_index], self.size_list[resource_index], \
               self.seed_list[resource_index], self.leech_list[resource_index]

    def add_new_row(self, seed: int, leech: int, size: int, magnet: str) -> None:
        """
        This Function will create another row of information for the RAWDataInstance object
        :param seed: int
        :param leech: int
        :param size: int
        :param magnet: str
        :return: None
        """
        self.seed_list.append(seed)
        self.leech_list.append(leech)
        self.size_list.append(size)
        self.resource_link_list.append(magnet)

    def list(self):
        struct = zip(self.size_list, self.seed_list, self.leech_list, self.resource_link_list)
        print('{0:^7} {1:>4}/{2:4} {3} '.format('SIZE', 'SEED', 'LEECH', 'MAGNET'))
        for size, seed, leech, magnet in struct:
            print('{0:7} {1:>4}/{2:4} {3} '.format(str(size), str(seed), str(leech), magnet))
        return
