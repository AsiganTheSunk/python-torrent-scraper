#!/usr/bin/env python

from colorama import Fore, Style
import os
from collections.abc import Mapping

class TorrentInstance(Mapping):
    def __init__(self, name, search_type, size_type):
        self.name = name
        self.search_type = search_type
        self.size_type = size_type

        self.namelist = []
        self.sizelist = []
        self.seedlist = []
        self.leechlist = []
        self.magnetlist = []

        self._storage = {'search_type':self.search_type,
                         'size_type':self.size_type}

    def __getitem__(self, key):
        if key == 'name':
            return self._get_name_list()
        elif key == 'size':
            return self._get_size_list()
        elif key == 'seed':
            return self._get_seed_list()
        elif key == 'leech':
            return self._get_leech_list()
        elif key == 'magnet':
            return self._get_magnet_list()
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

    def _get_size_list(self):
        return self.sizelist

    def _get_seed_list(self):
        return self.seedlist

    def _get_leech_list(self):
        return self.leechlist

    def _get_name_list(self):
        return self.namelist

    def _get_magnet_list(self):
        return self.magnetlist

    def list(self):
        struct = zip(self.namelist, self.sizelist, self.seedlist, self.leechlist, self.magnetlist)
        print (self.name + '\n')
        for name, size, seed, leech, magnet in struct:

            if os.name == 'nt':
                print (name, str(size), str(seed), str(leech), magnet)
            else:
                print(Fore.LIGHTMAGENTA_EX + name + Style.RESET_ALL, Fore.GREEN + str(size) + Style.RESET_ALL,
                      Fore.BLUE + str(seed) + Style.RESET_ALL, Fore.LIGHTRED_EX + str(leech) + Style.RESET_ALL, magnet)
        return

    def add_namelist(self, value):
        self.namelist.append(value)

    def add_sizelist(self, value):
        self.sizelist.append(value)

    def add_seedlist(self, value):
        self.seedlist.append(value)

    def add_leechlist(self, value):
        self.leechlist.append(value)

    def add_magnetlist(self, value):
        self.magnetlist.append(value)