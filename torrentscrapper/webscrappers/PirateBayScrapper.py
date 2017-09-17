#!/usr/bin/env python

from bs4 import BeautifulSoup
from torrentscrapper import TorrentInstance as ti
from torrentscrapper import WebSearch as ws

FILM_FLAG = 'FILM'
SHOW_FLAG = 'SHOW'
ANIME_FLAG = 'ANIME'

class PirateBayScrapper():
    def __init__(self):
        self.name = 'PirateBayScrapper'
        self.proxy_list = ['https://unblockedbay.inf', 'https://ukpirate.org', 'https://thehiddenbay.info']
        self.main_landing_page = self.proxy_list[0]
        self.show_landing_page = ''
        self.film_landing_page = ''

        self.default_url = self.main_landing_page + '/s/?q='
        self.default_category = '&category=0&page=0&orderby=99'
        return

    def build_url(self, websearch):
        print websearch.search_type
        if websearch.search_type is FILM_FLAG:
            return self._build_film_request(title=websearch.title, year=websearch.year, quality=websearch.quality)
        elif websearch.search_type is SHOW_FLAG:
            return self._build_show_request(title=websearch.title, season=websearch.season, episode=websearch.episode, quality=websearch.quality)
        else:
            print 'Anime?'

    def update_landing_page(self, value):
        self.main_landing_page = value
        self.default_url = value + '/s/?q='

    def _build_film_request(self, title='', year='',  quality=''):
        return (self.default_url + (title.replace(" ", "+") + '+' + str(year) + '+' + str(quality)) + self.default_category)

    def _build_show_request(self,title='', season='', episode='',  quality=''):
        return (self.default_url + (title.replace(" ", "+") + '+S' + str(season) + 'E' + str(episode) + '+' + str(quality)) + self.default_category)

    def _build_anime_request(self):
        return


    def webscrapper (self, content=None, search_type=None, size_type=None):
        torrent_instance = ti.TorrentInstance(name=self.name, search_type=search_type, size_type=size_type)
        soup = BeautifulSoup(content, 'html.parser')
        ttable = soup.findAll('table', {'id':'searchResult'})

        if ttable != []:
            print 'PirateBayScrapper retrieving individual values from the table\n'

            for items in ttable:
                tbody = items.findAll('tr')

                for tr in tbody[1:]:
                    title = (tr.findAll('a'))[2].text
                    seed = (tr.findAll('td'))[2].text
                    if seed == '0':
                        seed = '1'
                    leech = (tr.findAll('td'))[3].text
                    if leech == '0':
                        leech = '1'
                    magnet_link = (tr.findAll('a'))[2]['href']
                    size_string = (tr.findAll('font',{'class':'detDesc'}))
                    size = (size_string[0].text).split(',')[1][6:]
                    if 'MiB' in size:
                        size = size.replace('MiB','MB')
                        size = float(size[:-2])
                    elif 'GiB' in size:
                        size = size.replace('GiB', 'GB')
                        size = float(size[:-2]) * 1000

                    torrent_instance.add_namelist(str(title).strip())
                    torrent_instance.add_seedlist(int(seed))
                    torrent_instance.add_leechlist(int(leech))

                    torrent_instance.add_magnetlist(magnet_link)
                    torrent_instance.add_sizelist(int(size))
        else:
            print '%s unable to parse arguments ...\n' % self.name
        return torrent_instance


    def _get_magnet_link(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        div = (soup.findAll('div',{'class':'download'}))
        magnet = div[0].findAll('a')[0]['href']
        return (magnet)


