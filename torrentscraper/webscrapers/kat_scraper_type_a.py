#!/usr/bin/env python

from bs4 import BeautifulSoup
from torrentscraper.datastruct import p2p_instance as ti
from torrentscraper.datastruct.websearch import RAWData
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
        self.thread_defense_bypass_cookie = False

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

    def get_raw_data(self, content=None):
        raw_data = RAWData()

        soup = BeautifulSoup (content, 'html.parser')
        ttable = soup.findAll('tr', {'class':'odd'})

        # Retrieving individual raw values from the search result
        if ttable != []:
            print('{0}: Retrieving Raw Values from the Search Result'.format(self.name))
            for items in ttable:
                _pos = len(raw_data.magnet_list)
                #title = (items.findAll('a', {'class': 'cellMainLink'}))[0].text
                size = (items.findAll('td', {'class': 'nobr center'}))[0].text

                # Converting GB to MB, to easily manage the pandas structure
                if 'MiB' in size:
                    size = size.replace('MiB', 'MB')
                    size = float(size[:-3])
                elif 'GiB' in size:
                    size = size.replace('GiB', 'GB')
                    size = float(size[:-3]) * 1000


                # Bandage to the problem of getting the seeds and the leechs using _torrent_pos
                # Changing 0 to 1 to avoid ratio problem
                seed = (soup.findAll('td', {'class': 'green center'}))[ _pos].text
                if seed == '0':
                    seed = '1'

                # Changing 0 to 1 to avoid ratio problem
                leech = (soup.findAll('td', {'class': 'red lasttd center'}))[ _pos].text
                if leech == '0':
                    leech = '1'

                magnet_link = (items.findAll('a', {'title': 'Torrent magnet link'}))[0]['href']

                raw_data.add_magnet(magnet_link)
                raw_data.add_size(size)
                raw_data.add_seed(seed)
                raw_data.add_leech(leech)
        else:
            print('{0}: Unable to Retrieve Raw Values from the Search Result'.format(self.name))
        return raw_data

    def magnet_link_scrapper(self, content):
        return
