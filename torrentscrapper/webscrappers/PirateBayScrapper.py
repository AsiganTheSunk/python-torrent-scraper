#!/usr/bin/env python

from bs4 import BeautifulSoup
from torrentscrapper.utils.torcurl import TorPyCurl as tpc
import requests

class PirateBayScrapper():
    def __init__(self):
        self.default_url = 'https://unblockedbay.info/s/?q='
        self.default_category = '&category=0&page=0&orderby=99'
        return

    def _build_film_request(self, title='', year=''):
        return (self.default_url + (title.replace(" ", "+") + '+' + str(year)) + self.default_category)

    def _build_show_request(self, title='', season='', episode=''):
        return (self.default_url + (title.replace(" ", "+") + '+S' + str(season) + 'E' + str(episode)) + self.default_category)

    def _build_anime_request(self):
        return

    def thepiratebay_webscrapper(self, content):

        soup = BeautifulSoup(content, 'html.parser')
        print soup.prettify()

        ttable = soup.findAll('table', {'searchResult'})
        print ttable


        if ttable != []:
            print 'Retrieving individual values from the table'

        return

    def retrieve_seeders(self):
        return

    def retrieve_leechers(self):
        return

    def retrieve_magnet(self):
        return



