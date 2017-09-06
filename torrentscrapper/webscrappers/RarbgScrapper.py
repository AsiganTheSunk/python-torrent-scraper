#!/usr/bin/python

import os
import sys
from bs4 import BeautifulSoup
from torrentscrapper.utils.torcurl import TorPyCurl as tpc

SHOW_FLAG = '6'
FILM_FLAG = '14'
ANIME_FLAG = '10'

class RarbgScrapper():

    def __init__(self):
        self.default_url = 'https://www.rarbg.to/torrents.php?search='
        self.default_serie_categories = '&category%5B%5D=18&category%5B%5D=41&category%5B%5D=49'
        self.default_film_categories = '&category[]=14&category[]=48&category[]=17&category[]=44&category[]=45&category[]=47&category[]=50&category[]=51&category[]=52&category[]=42&category[]=46'

    def _build_film_request(self, title='', year=''):
        return

    def _build_show_request(self, title='', season='', episode=''):
        return (self.default_url + (title.replace(" ", "%20") + '%20S' + str(season) + 'E' + str(episode)) + self.default_serie_categories)


def rarbg_parser (data=None):
    soup = BeautifulSoup (data, 'html.parser')
    ttable = soup.findAll('tr', {'class': 'lista2'})

    if ttable != []:
        print 'Retrieving individual values from the table'

        for items in ttable:
            title = (items.findAll('a')[1])['title']
            size = items.findAll('td', {'class': 'lista'})[3].text

            # leechs = tamano = items.findAll('td', {'class': 'lista'})[5].text
            # print title, tamano
            # print '****' * 20

        for items in ttable:
            # href =  items.findAll('td', {'class': 'lista'})[1]
            href = (items.findAll('a')[1])['href']
            print '+++HREF 1: ' + str(href)
            #href1 = items.findAll('td', {'class': 'lista'})[2]['href']
            #print '+++HREF 2: ' + str(href1)
            seeds = items.findAll('td', {'class': 'lista'})[4].text
            print '***SEEDS: ' + str(seeds)
            leechs = items.findAll('td', {'class': 'lista'})[5].text
            print '***LEECHS: ' + str(leechs)

    else:
        print 'rarbg.to seems to not be working at the moment, please try again later'

    '''
    soup = BeautifulSoup(content.text, 'html.parser')
    magnet = soup.findAll('a', href=True)
    #magnet2 = (soup.findAll('a', href=True)[21])['href']

    print '____' * 20
    #print magnet2
    print '____' * 20

    contador = 1
    for item in magnet:

        #print contador, item
        contador = contador + 1

        #print '____'*3
        #print magnet
    '''