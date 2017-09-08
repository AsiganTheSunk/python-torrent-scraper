#!/usr/bin/python

import os
import sys
from bs4 import BeautifulSoup
from torrentscrapper.utils.torcurl import TorPyCurl as tpc

SHOW_FLAG = '6'
FILM_FLAG = '14'
ANIME_FLAG = '10'

DEFAULT_RARBG_URL = 'https://www.rarbg.to/torrents.php?search='

def build_film_request(title='', year=''):
    return (DEFAULT_RARBG_URL + (title.replace(" ", "%20") + '%20' + str(year)))

def build_show_request(title='', season='', episode=''):
    return (DEFAULT_RARBG_URL + (title.replace(" ", "%20") + '%20S' + str(season) + 'E' + str(episode)) + '&category%5B%5D=18&category%5B%5D=41&category%5B%5D=49')


def rarbg_scrap(url=''):

    session = tpc.TorPyCurl()
    try:
        response = session.get(url=url, ssl=True)
        print response.code
        print response.data
    except Exception as e:
        print 'rarbg_scrap failed'
    finally:
        if response.code == 200:
            print '200 OK'
            return response


def rarbg_parser (content=None):
    soup = BeautifulSoup (content, 'html.parser')
    # print soup.prettify()
    ttable = soup.findAll('tr', {'class': 'lista2'})
    # print ttable
    raw_input('Press [ENTER] To Continue...')

    if ttable != []:
    # TODO anadir un callback o algo si no lo encuentra de la primera forma.
        print 'Retrieving individual values from the table'
        for items in ttable:
            title = (items.findAll('a')[1])['title']
            tamano = items.findAll('td', {'class': 'lista'})[3].text
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

