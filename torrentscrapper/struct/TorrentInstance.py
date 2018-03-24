#!/usr/bin/env python
#-*- coding. utf-8 -*-

from colorama import Fore, Style
import os

class TorrentInstance():
    def __init__(self, name, search_type, size_type):
        self.scrapper_name = name
        self.search_type = search_type
        self.size_type = size_type

        self.namelist = []
        self.sizelist = []
        self.seedlist = []
        self.leechlist = []
        self.magnetlist = []

    def list(self):
        struct = zip(self.namelist, self.sizelist, self.seedlist, self.leechlist, self.magnetlist)
        print (self.scrapper_name + '\n')
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