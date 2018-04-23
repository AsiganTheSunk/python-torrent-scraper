#!/usr/bin/env python

from bs4 import BeautifulSoup
from torrentscraper.datastruct import p2p_instance as ti

FILM_FLAG = 'FILM'
SHOW_FLAG = 'SHOW'
ANIME_FLAG = 'ANIME'

class RarbgScrapper():
    def __init__(self):
        self.name = self.__class__.__name__
        self.proxy_list = ['https://www.rarbg.is', 'https://rarbg.unblockall.org']
        self._proxy_list_length = len(self.proxy_list)
        self._proxy_list_pos = 0
        self.cloudflare_cookie = False
        self.query_type = False
        self.disable_quality = True
        self.thread_defense_bypass_cookie = True

        self.default_params = {}
        self.main_page = self.proxy_list[self._proxy_list_pos]
        self.default_search = '/torrents.php?search='
        self.default_tail = ''
        self.supported_searchs = [FILM_FLAG, SHOW_FLAG]

    def update_main_page(self):
        try:
            value = self._proxy_list_pos
            if self._proxy_list_length > self._proxy_list_pos:
                value += 1

            self._proxy_list_pos = value
            self.main_page = self.proxy_list[self._proxy_list_pos]
        except IndexError:
            raise IndexError


    def webscrapper(self, content=None, search_type=None, size_type=None, debug=False):
        torrent_instance = ti.TorrentInstance(name=self.name, search_type=search_type, size_type=size_type)
        soup = BeautifulSoup (content, 'html.parser')
        ttable = soup.findAll('tr', {'class': 'lista2'})
        print(soup)
        # Retrieving individual values from the search result
        if ttable != []:
            print ('%s retrieving individual values from the table' % self.name)

            for items in ttable:
                title = (items.findAll('a')[1])['title']
                magnet_link = (items.findAll('a')[1])['href']

                # Changing 0 to 1 to avoid ratio problem
                seed = items.findAll('td', {'class': 'lista'})[4].text
                if seed == '0':
                    seed = '1'

                # Changing 0 to 1 to avoid ratio problem
                leech = items.findAll('td', {'class': 'lista'})[5].text
                if leech == '0':
                    leech = '1'

                # Converting GB to MB, to easily manage the pandas structure
                size = items.findAll('td', {'class': 'lista'})[3].text
                if 'GB' in size:
                    size = float(size[:-2]) * 1000
                else:
                    size = float(size[:-2])

                torrent_instance.add_namelist(str(title).strip())
                torrent_instance.add_size(int(size))
                torrent_instance.add_seed(int(seed))
                torrent_instance.add_leech(int(leech))
                torrent_instance.add_magnet(str(self.main_page + magnet_link))


        else:
            print ('%s unable to retrieve individual values from the table ...' % self.name)
        return torrent_instance

    def magnet_link_scrapper(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        table = (soup.findAll('table',{'class':'lista'}))
        td = table[0].findAll('td',{'class':'lista'})[0]
        magnet = td.findAll('a')[1]['href']
        return (magnet)
