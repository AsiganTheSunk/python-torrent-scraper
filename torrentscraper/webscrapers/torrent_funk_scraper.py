#!/usr/bin/env python

from bs4 import BeautifulSoup
from torrentscraper.datastruct.websearch import RAWData

FILM_FLAG = 'FILM'
SHOW_FLAG = 'SHOW'
ANIME_FLAG = 'ANIME'

class TorrentFunkScraper():
    def __init__(self):
        self.name = self.__class__.__name__
        self.proxy_list = ['https://www.torrentfunk.com', 'https://torrentfunk.unblocked.mx', 'http://www.btdigg.in/torrentfunk']
        self._proxy_list_length = len(self.proxy_list)
        self._proxy_list_pos = 0
        self.cloudflare_cookie = False
        self.query_type = False
        self.disable_quality = False
        self.thread_defense_bypass_cookie = False

        self.default_params = {}
        self.main_page = self.proxy_list[self._proxy_list_pos]
        self.default_search = '/all/torrents/'
        self.default_tail = '.html'
        self.supported_searchs = [FILM_FLAG, SHOW_FLAG, ANIME_FLAG]

    def update_main_page(self):
        try:
            value = self._proxy_list_pos
            if self._proxy_list_length > self._proxy_list_pos:
                value += 1

            self._proxy_list_pos = value
            self.main_page = self.proxy_list[self._proxy_list_pos]
        except IndexError:
            raise IndexError

    def get_raw_data(self, content=None):
        raw_data = RAWData()
        soup = BeautifulSoup(content, 'html.parser')
        #print(soup.prettify())
        ttable = soup.findAll('table', {'class':'tmain'})

        # Retrieving individual values from the search result
        if ttable != []:
            print ('%s retrieving individual values from the table' % self.name)

            for items in ttable:
                #print('%s' % items)
                tbody = items.findAll('tr')

                for tr in tbody[1:]:
                    #title = (tr.findAll('a'))[0].text

                    # Changing 0 to 1 to avoid ratio problem
                    seed = (tr.findAll('td'))[3].text
                    if seed == '0':
                        seed = '1'

                    # Changing 0 to 1 to avoid ratio problem
                    leech = (tr.findAll('td'))[4].text
                    if leech == '0':
                        leech = '1'

                    # Converting GB to MB, to easily manage the pandas structure
                    size = (tr.findAll('td'))[2].text
                    size = float(size[:-3])

                    magnet_link = (tr.findAll('a'))[0]['href']

                    # LookUp for false torrents 'Full Download', 'High Definition' ...
                    # if ('download') in magnet_link:
                    #     print('%s skipping false magnet entry: [%s]' % (self.name, magnet_link))
                    # else:
                    #     print('%s adding magnet entry: [%s]' % (self.name, magnet_link))

                    if int(seed) < 1000:
                        raw_data.add_magnet(str(self.main_page + magnet_link))
                        raw_data.add_seed(int(seed))
                        raw_data.add_leech(int(leech))
                        raw_data.add_size(int(size))
        else:
            print ('%s unable to retrieve individual values from the table ...' % self.name)
        return raw_data

    def get_magnet_link(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        content = (soup.findAll('div',{'class':'content'}))
        magnet = content[2].findAll('a')[1]['href']
        return (self.main_page + magnet)


