#!/usr/bin/python

import os
import sys
from bs4 import BeautifulSoup
from torrentscrapper.utils.torcurl import TorPyCurl as tpc
from torrentscrapper import TorrentInstance as ti

SHOW_FLAG = '6'
FILM_FLAG = '14'
ANIME_FLAG = '10'

class KatScrapper():

    def __init__(self):
        self.name = 'KatScrapper'
        self.main_landing_page = 'https://kickass.cm/'
        self.show_landing_page = 'https://kickass.cm/tv/'
        self.film_landing_page = 'https://kickass.cm/movies/'

        self.search_url = 'https://kickass.cm/usearch/'
        self.serie_categories = '%20category:tv/'
        self.film_categories = '%20category:movies/'

    def _build_film_request(self, quality='',title='', year=''):
        return (self.search_url + (title.replace(" ", "%20") + '%20' + str(year) + '%20' + str(quality)) )#+ '%20' + self.film_categories)

    def _build_show_request(self, quality='',title='', season='', episode=''):
        return (self.search_url + (title.replace(" ", "%20") + '%20S' + str(season) + 'E' + str(episode) + '%20' + str(quality)))

    def webscrapper (self, content=None):
        torrent_instance = ti.TorrentInstance(name=self.name)
        soup = BeautifulSoup (content, 'html.parser')
        ttable = soup.findAll('tr', {"id": "torrent_latest_torrents"})

        if ttable != []:
            print 'KatScrapper retrieving individual values from the table\n'
            for items in ttable:
                title = (items.findAll('a', {'class': 'cellMainLink'}))[0].text
                size = (items.findAll('td', {'class': 'nobr center'}))[0].text
                if 'GB' in size:
                    size = float(size[:-2]) * 1000
                else:
                    size = size.text[:-2]
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
