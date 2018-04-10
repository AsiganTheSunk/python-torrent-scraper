#!/usr/bin/env python

from bs4 import BeautifulSoup
from torrentscraper.datastruct import torrent_instance as ti

FILM_FLAG = 'FILM'
SHOW_FLAG = 'SHOW'
ANIME_FLAG = 'ANIME'

class KatScrapperTypeB():
    def __init__(self):
        self.name = self.__class__.__name__
        self.proxy_list = ['https://katcr.co']
        self._proxy_list_length = len(self.proxy_list)
        self._proxy_list_pos = 0
        self.cloudflare_cookie = False
        self.query_type = False
        self.disable_quality = True

        self.main_page = self.proxy_list[self._proxy_list_pos]
        self.default_search = '/katsearch/page/1/'
        self.default_tail = ''
        self.default_params = {}
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

    def webscrapper (self, content=None, search_type=None, size_type=None, debug=False):
        torrent_instance = ti.TorrentInstance(name=self.name, search_type=search_type, size_type=size_type)
        soup = BeautifulSoup (content, 'html.parser')
        #print(soup.prettify())
        ttable = soup.findAll('table', {'class': 'table table--bordered table--striped table--hover torrents_table'})
        # Retrieving individual values from the search result
        tbody = ttable[0].findAll('tbody')[0]
        if tbody != []:
            print ('%s retrieving individual values from the table \n' % self.name)
            for items in tbody:
                title = (items.findAll('a', {'class': 'torrents_table__torrent_title'}))[0].text
                size = (items.findAll('td', {'data-title': 'Size'}))[0].text

                # Converting GB to MB, to easily manage the pandas structure
                if 'MB' in size:
                    size = float(size[:-3])
                elif 'GB' in size:
                    size = float(size[:-3]) * 1000

                magnet_link = (items.findAll('a', {'title': 'Torrent magnet link'}))[0]['href']

                # Changing 0 to 1 to avoid ratio problem
                seed = (items.findAll('td', {'data-title': 'Seed'}))[0].text
                if seed == '0':
                    seed = '1'

                # Changing 0 to 1 to avoid ratio problem
                leech = (items.findAll('td', {'data-title': 'Leech'}))[0].text
                if leech == '0':
                    leech = '1'

                if debug:
                    print('%s adding torrent entry ...\n title: [ %s ]\n size: [ %s ]\n seeds: [ %s ]\n leech: [ %s ]\n magnet: [ %s ]'
                          % (self.name, str(title).strip(), str(size), str(seed), str(leech), magnet_link))
                torrent_instance.add_namelist(str(title).strip())
                torrent_instance.add_seedlist(int(seed))
                torrent_instance.add_leechlist(int(leech))
                torrent_instance.add_magnetlist(str(magnet_link))
                torrent_instance.add_sizelist(int(size))

        else:
            print ('%s unable to retrieve individual values from the table ...\n' % self.name)

        return torrent_instance

    def magnet_link_scrapper(self, content):
        return
