#!/usr/bin/env python
#-*- coding. utf-8 -*-

from torrentscrapper.utils import color
from colorama import Fore, Style
class TorrentInstance():

    def __init__(self):
        self.namelist = []
        self.sizelist = []
        self.seedlist = []
        self.leechlist = []
        self.magnetlist = []

    def list(self):
        struct = zip(self.namelist, self.sizelist, self.seedlist, self.leechlist, self.magnetlist)
        for name, size, seed, leech, magnet in struct:
            print Fore.LIGHTMAGENTA_EX + name + Style.RESET_ALL, Fore.GREEN + size + Style.RESET_ALL, Fore.BLUE + seed + Style.RESET_ALL, Fore.LIGHTRED_EX + leech + Style.RESET_ALL, magnet
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