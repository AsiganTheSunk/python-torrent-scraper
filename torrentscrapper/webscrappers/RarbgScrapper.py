#!/usr/bin/python

import os
import sys
from bs4 import BeautifulSoup
from torrentscrapper.utils.torcurl import TorPyCurl as tpc
from torrentscrapper import TorrentInstance as ti


SHOW_FLAG = '6'
FILM_FLAG = '14'
ANIME_FLAG = '10'

class RarbgScrapper():

    def __init__(self):
        self.default_url = 'https://www.rarbg.to/torrents.php?search='
        self.default_serie_categories = '&category%5B%5D=18&category%5B%5D=41&category%5B%5D=49'
        self.default_film_categories = '&category[]=14&category[]=48&category[]=17&category[]=44&category[]=45&category[]=47&category[]=50&category[]=51&category[]=52&category[]=42&category[]=46'

    def _build_film_request(self, quality='',title='', year=''):
        return (self.default_url + (title.replace(" ", "%20") + '%20' + str(year) + '%20' + str(quality)) + self.default_film_categories)

    def _build_show_request(self, quality='',title='', season='', episode=''):
        return (self.default_url + (title.replace(" ", "%20") + '%20S' + str(season) + 'E' + str(episode) + '%20' + str(quality)) + self.default_serie_categories)


    def webscrapper (self, content=None):

        torrent_instance = ti.TorrentInstance()
        soup = BeautifulSoup (content, 'html.parser')
        ttable = soup.findAll('tr', {'class': 'lista2'})

        if ttable != []:
            print 'RarbgScrapper retrieving individual values from the table\n'

            for items in ttable:
                title = (items.findAll('a')[1])['title']
                size = items.findAll('td', {'class': 'lista'})[3].text
                seed = items.findAll('td', {'class': 'lista'})[4].text
                leech = items.findAll('td', {'class': 'lista'})[5].text
                magnet_link = (items.findAll('a')[1])['href']

                torrent_instance.add_namelist(title)
                torrent_instance.add_seedlist(seed)
                torrent_instance.add_leechlist(leech)
                torrent_instance.add_magnetlist(magnet_link)
                torrent_instance.add_sizelist(size)

        else:
            print 'RarbgScrapper seems to not be working at the moment, please try again later ...\n'
        return torrent_instance

    def _magnet_link(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        table = (soup.findAll('table',{'class':'lista'}))
        td = table[0].findAll('td',{'class':'lista'})[0]
        magnet = td.findAll('a')[1]['href']
        return (magnet)