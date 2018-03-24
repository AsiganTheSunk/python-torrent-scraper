#!/usr/bin/env python

from bs4 import BeautifulSoup
from torrentscrapper.struct import TorrentInstance as ti

FILM_FLAG = 'FILM'
SHOW_FLAG = 'SHOW'
ANIME_FLAG = 'ANIME'

class KatScrapperTypeA():
    def __init__(self):
        self.name = self.__class__.__name__
        self.proxy_list = ['https://kickass.cd']
        self._proxy_list_length = len(self.proxy_list)
        self._proxy_list_pos = 0
        self.cloudflare_cookie = False
        self.query_type = True
        self.disable_quality = False

        self.main_page = self.proxy_list[self._proxy_list_pos]
        self.default_search = '/search.php'
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
        ttable = soup.findAll('tr', {'class':'odd'})

        # Retrieving individual values from the search result
        if ttable != []:
            print ('%s retrieving individual values from the table:\n' % self.name)
            for items in ttable:
                _torrent_pos = len(torrent_instance.magnetlist)
                title = (items.findAll('a', {'class': 'cellMainLink'}))[0].text
                size = (items.findAll('td', {'class': 'nobr center'}))[0].text

                # Converting GB to MB, to easily manage the pandas structure
                if 'MiB' in size:
                    size = size.replace('MiB', 'MB')
                    size = float(size[:-3])
                elif 'GiB' in size:
                    size = size.replace('GiB', 'GB')
                    size = float(size[:-3]) * 1000

                magnet_link = (items.findAll('a', {'title': 'Torrent magnet link'}))[0]['href']

                # Bandage to the problem of getting the seeds and the leechs using _torrent_pos
                # Changing 0 to 1 to avoid ratio problem
                seed = (soup.findAll('td', {'class': 'green center'}))[ _torrent_pos].text
                if seed == '0':
                    seed = '1'

                # Changing 0 to 1 to avoid ratio problem
                leech = (soup.findAll('td', {'class': 'red lasttd center'}))[ _torrent_pos].text
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
