#!/usr/bin/env python

from bs4 import BeautifulSoup
from torrentscrapper.utils.torcurl import TorPyCurl as tpc
from torrentscrapper import TorrentInstance as ti

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

        torrent_instance = ti.TorrentInstance()
        soup = BeautifulSoup(content, 'html.parser')
        ttable = soup.findAll('table', {'id':'searchResult'})

        if ttable != []:
            print 'PirateBayScrapper retrieving individual values from the table\n'

            for items in ttable:
                tbody = items.findAll('tr')

                for tr in tbody[1:]:
                    title = (tr.findAll('a'))[2].text
                    seed = (tr.findAll('td'))[2].text
                    leech = (tr.findAll('td'))[3].text
                    magnet_link = (tr.findAll('a'))[2]['href']
                    size_string = (tr.findAll('font',{'class':'detDesc'}))
                    size = (size_string[0].text).split(',')[1][6:]
                    if 'MiB' in size:
                        size = size.replace('MiB','MB')
                    elif 'GiB' in size:
                        size = size.replace('GiB', 'GB')

                    torrent_instance.add_namelist(title)
                    torrent_instance.add_seedlist(seed)
                    torrent_instance.add_leechlist(leech)
                    torrent_instance.add_magnetlist(magnet_link)
                    torrent_instance.add_sizelist(size)
        else:
            print 'PirateBayScrapper seems to not be working at the moment, please try again later'
        return torrent_instance


    def _magnet_link(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        div = (soup.findAll('div',{'class':'download'}))
        magnet = div[0].findAll('a')[0]['href']
        return (magnet)


