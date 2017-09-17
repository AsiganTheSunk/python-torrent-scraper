#!/usr/bin/env python

from bs4 import BeautifulSoup
from torrentscrapper import TorrentInstance as ti

class KatScrapper():

    def __init__(self):
        self.name = 'KatScrapper'
        self.proxy_list = ['https://kickass.cm', 'https://kickass2.nz','https://thekat.se']
        self.main_landing_page = self.proxy_list[0]
        self.show_landing_page = self.main_landing_page + '/tv/'
        self.film_landing_page = self.main_landing_page + '/movies/'

        self.search_url = self.main_landing_page + '/usearch/'
        self.serie_categories = '%20category:tv/'
        self.film_categories = '%20category:movies/'

    def _build_film_request(self, quality='',title='', year=''):
        return (self.search_url + (title.replace(" ", "%20") + '%20' + str(year) + '%20' + str(quality)) )#+ '%20' + self.film_categories)

    def _build_show_request(self, quality='',title='', season='', episode=''):
        return (self.search_url + (title.replace(" ", "%20") + '%20S' + str(season) + 'E' + str(episode) + '%20' + str(quality)) + '/')

    def webscrapper (self, content=None, search_type=None, size_type=None):
        torrent_instance = ti.TorrentInstance(name=self.name, search_type=search_type, size_type=size_type)
        soup = BeautifulSoup (content, 'html.parser')
        ttable = soup.findAll('tr', {"id": "torrent_latest_torrents"})

        if ttable != []:
            print 'KatScrapper retrieving individual values from the table\n'
            for items in ttable:
                title = (items.findAll('a', {'class': 'cellMainLink'}))[0].text
                size = (items.findAll('td', {'class': 'nobr center'}))[0].text
                if 'GB' in size:
                    size = float(size[:-3]) * 1000
                else:
                    size = float(size[:-3].strip())
                magnet = (items.findAll('a', {'title': 'Torrent magnet link'}))[0]['href']

                torrent_instance.add_namelist(str(title).strip())
                torrent_instance.add_sizelist(int(size))
                torrent_instance.add_magnetlist(str(magnet))

            seeds = (soup.findAll('td', {'class': 'green center'}))
            for seed in seeds:
                if seed.text == '0':
                    torrent_instance.add_seedlist(1)
                else:
                    torrent_instance.add_seedlist(int(seed.text))

            leechs = (soup.findAll('td', {'class': 'red lasttd center'}))
            for leech in leechs:
                if str(leech.text) == '0':
                    torrent_instance.add_leechlist(1)
                else:
                    torrent_instance.add_leechlist(int(leech.text))

        else:
            print 'KatScrapper seems to not be working at the moment, please try again later ...\n'

        return torrent_instance

    def _magnet_link(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        table = (soup.findAll('table',{'class':'lista'}))
        td = table[0].findAll('td',{'class':'lista'})[0]
        magnet = td.findAll('a')[1]['href']
        return (magnet)
