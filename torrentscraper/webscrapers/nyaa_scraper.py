#!/usr/bin/env python

# future!

from bs4 import BeautifulSoup
from torrentscraper.datastruct import torrent_instance as ti

FILM_FLAG = 'FILM'
SHOW_FLAG = 'SHOW'
ANIME_FLAG = 'ANIME'

class RarbgScrapper():

    def __init__(self):
        self.name = 'NyaaScraper'
        self.proxy_list = ['https://nyaa.si']
        self.main_page = self.proxy_list[0]

        self.search_url = self.main_page + '/?f=0&c=0_0&q='
        self.supported_searchs = [FILM_FLAG, SHOW_FLAG]

    def build_url(self, websearch):
        if websearch.search_type is FILM_FLAG:
            return
        elif websearch.search_type is SHOW_FLAG:
            return
        else:
            return self.build_anime_request(quality=websearch.quality, title=websearch.title, episode=websearch.episode)

    def update_main_page(self, value):
        self.main_page = value
        self.default_url = value + '/?f=0&c=0_0&q='

    def build_film_request(self, quality='', title='', year=''):
        return (self.search_url + (title.replace(" ", "%20") + '%20' + str(year) + '%20' + str(quality)))

    def build_show_request(self, quality='', title='', season='', episode=''):
        return (self.search_url + (title.replace(" ", "+") + '+' + str(episode) + '+' + str(quality)))

    def build_anime_request(self, quality='', title='', episode=''):
        return (self.search_url + (title.replace(" ", "+") + '+' + str(episode) + '+' + str(quality)))

    def webscrapper(self, content=None, search_type=None, size_type=None):
        torrent_instance = ti.TorrentInstance(name=self.name, search_type=search_type, size_type=size_type)
        soup = BeautifulSoup (content, 'html.parser')
        ttable = soup.findAll('tr', {'class': 'lista2'})

        # Retrieving individual values from the search result
        if ttable != []:
            print ('%s retrieving individual values from the table' % self.name)

            # for items in ttable:
            #     title = (items.findAll('a')[1])['title']
            #     magnet_link = (items.findAll('a')[1])['href']
            #
            #     # Changing 0 to 1 to avoid ratio problem
            #     seed = items.findAll('td', {'class': 'lista'})[4].text
            #     if seed == '0':
            #         seed = '1'
            #
            #     # Changing 0 to 1 to avoid ratio problem
            #     leech = items.findAll('td', {'class': 'lista'})[5].text
            #     if leech == '0':
            #         leech = '1'
            #
            #     # Converting GB to MB, to easily manage the pandas structure
            #     size = items.findAll('td', {'class': 'lista'})[3].text
            #     if 'GB' in size:
            #         size = float(size[:-2]) * 1000
            #     else:
            #         size = float(size[:-2])
            #
            #     torrent_instance.add_namelist(str(title).strip())
            #     torrent_instance.add_sizelist(int(size))
            #     torrent_instance.add_seedlist(int(seed))
            #     torrent_instance.add_leechlist(int(leech))
            #     torrent_instance.add_magnetlist(str(self.main_page + magnet_link))
            #

        else:
            print ('%s unable to retrieve individual values from the table ...' % self.name)
        return torrent_instance

    def magnet_link_scrapper(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        table = (soup.findAll('table',{'class':'lista'}))
        td = table[0].findAll('td',{'class':'lista'})[0]
        magnet = td.findAll('a')[1]['href']
        return (magnet)
