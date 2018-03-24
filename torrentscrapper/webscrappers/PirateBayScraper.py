#!/usr/bin/env python

from bs4 import BeautifulSoup
from torrentscrapper.struct import TorrentInstance as ti

FILM_FLAG = 'FILM'
SHOW_FLAG = 'SHOW'
ANIME_FLAG = 'ANIME'

class PirateBayScraper():
    def __init__(self):
        self.name = self.__class__.__name__
        self.proxy_list = ['https://unblockedbay.info/', 'https://ukpirate.org/', 'https://thehiddenbay.info/']
        self._proxy_list_length = len(self.proxy_list)
        self._proxy_list_pos = 0
        self.cloudflare_cookie = False
        self.query_type = True
        self.disable_quality = False

        self.main_page = self.proxy_list[self._proxy_list_pos]
        self.default_search = 's/'
        self.default_tail = ''
        self.default_params = {'category':'0', 'page':'0', 'orderby':'99'}
        self.supported_searchs = [FILM_FLAG, SHOW_FLAG, ANIME_FLAG]

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
        soup = BeautifulSoup(content, 'html.parser')
        ttable = soup.findAll('table', {'id':'searchResult'})

        # Retrieving individual values from the search result
        if ttable != []:
            print ('%s retrieving individual values from the table' % self.name)

            for items in ttable:
                tbody = items.findAll('tr')

                for tr in tbody[1:]:
                    title = (tr.findAll('a'))[2].text
                    magnet_link = (tr.findAll('a'))[2]['href']

                    # Changing 0 to 1 to avoid ratio problem
                    seed = (tr.findAll('td'))[2].text
                    if seed == '0':
                        seed = '1'

                    # Changing 0 to 1 to avoid ratio problem
                    leech = (tr.findAll('td'))[3].text
                    if leech == '0':
                        leech = '1'

                    # Converting GB to MB, to easily manage the pandas structure
                    size_string = (tr.findAll('font',{'class':'detDesc'}))
                    size = (size_string[0].text).split(',')[1][6:]

                    if 'MiB' in size:
                        size = size.replace('MiB','MB')
                        size = float(size[:-2])
                    elif 'GiB' in size:
                        size = size.replace('GiB', 'GB')
                        size = float(size[:-2]) * 1000

                    if debug:
                        print('%s adding torrent entry ...\n title: [ %s ]\n size: [ %s ]\n seeds: [ %s ]\n leech: [ %s ]\n magnet: [ %s ]'
                              % (self.name, str(title).strip(), str(size), str(seed), str(leech), magnet_link))
                    torrent_instance.add_namelist(str(title).strip())
                    torrent_instance.add_seedlist(int(seed))
                    torrent_instance.add_leechlist(int(leech))
                    torrent_instance.add_magnetlist(str(self.main_page + magnet_link))
                    torrent_instance.add_sizelist(int(size))
        else:
            print ('%s unable to retrieve individual values from the table ...' % self.name)
        return torrent_instance

    def magnet_link_scrapper(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        div = (soup.findAll('div',{'class':'download'}))
        magnet = div[0].findAll('a')[0]['href']
        return (magnet)
