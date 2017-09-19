#!/usr/bin/env python

from bs4 import BeautifulSoup
from torrentscrapper import TorrentInstance as ti

FILM_FLAG = 'FILM'
SHOW_FLAG = 'SHOW'
ANIME_FLAG = 'ANIME'

class KatScrapper():

    def __init__(self):
        self.name = 'KatScrapper'
        self.proxy_list = ['https://kickass.cm', 'https://kickass2.nz','https://thekat.se']
        self.main_page = self.proxy_list[0]
        self.show_page = self.main_page + '/tv/'
        self.film_page = self.main_page + '/movies/'

        self.search_url = self.main_page + '/usearch/'
        self.serie_categories = '%20category:tv/'
        self.film_categories = '%20category:movies/'
        self.supported_searchs = [FILM_FLAG, SHOW_FLAG]

    def build_url(self, websearch):
        if websearch.search_type is FILM_FLAG:
            return self.build_film_request(title=websearch.title, year=websearch.year, quality=websearch.quality)
        elif websearch.search_type is SHOW_FLAG:
            return self.build_show_request(title=websearch.title, season=websearch.season, episode=websearch.episode, quality=websearch.quality)
        else:
            print 'Anime?'

    def update_main_page(self, value):
        self.main_page = value
        self.default_url = value + '/usearch/'

    def build_film_request(self, quality='', title='', year=''):
        return (self.search_url + (title.replace(" ", "%20") + '%20' + str(year) + '%20' + str(quality)) )#+ '%20' + self.film_categories)

    def build_show_request(self, quality='', title='', season='', episode=''):
        return (self.search_url + (title.replace(" ", "%20") + '%20S' + str(season) + 'E' + str(episode) + '%20' + str(quality)) + '/')

    def webscrapper (self, content=None, search_type=None, size_type=None):
        torrent_instance = ti.TorrentInstance(name=self.name, search_type=search_type, size_type=size_type)
        soup = BeautifulSoup (content, 'html.parser')
        ttable = soup.findAll('tr', {"id": "torrent_latest_torrents"})

        # Retrieving individual values from the search result
        if ttable != []:
            print ('%s retrieving individual values from the table \n' % self.name)

            for items in ttable:
                title = (items.findAll('a', {'class': 'cellMainLink'}))[0].text
                size = (items.findAll('td', {'class': 'nobr center'}))[0].text

                # Converting GB to MB, to easily manage the pandas structure
                if 'GB' in size:
                    size = float(size[:-3]) * 1000
                else:
                    size = float(size[:-3].strip())
                magnet = (items.findAll('a', {'title': 'Torrent magnet link'}))[0]['href']

                torrent_instance.add_namelist(str(title).strip())
                torrent_instance.add_sizelist(int(size))
                torrent_instance.add_magnetlist(str(magnet))

            # Changing 0 to 1 to avoid ratio problem
            seeds = (soup.findAll('td', {'class': 'green center'}))
            for seed in seeds:
                if seed.text == '0':
                    torrent_instance.add_seedlist(1)
                else:
                    torrent_instance.add_seedlist(int(seed.text))

            # Changing 0 to 1 to avoid ratio problem
            leechs = (soup.findAll('td', {'class': 'red lasttd center'}))
            for leech in leechs:
                if str(leech.text) == '0':
                    torrent_instance.add_leechlist(1)
                else:
                    torrent_instance.add_leechlist(int(leech.text))

        else:
            print ('%s unable to retrieve individual values from the table ...\n' % self.name)

        return torrent_instance

    def magnet_link_scrapper(self, content):
        return
