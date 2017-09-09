#!/usr/bin/env python

from torrentscrapper.webscrappers import RarbgScrapper as rs
from torrentscrapper.webscrappers import PirateBayScrapper as pbs

import requests
from pandas import DataFrame
from fake_useragent import UserAgent
from time import sleep
from random import randint



rarbg_file = open('/home/asigan/python-torrent-scrapper/examples/rarbgexample.html')
piratebay_file = open('/home/asigan/python-torrent-scrapper/examples/thepiratebayexample.html')
rarbg_magnet = open('/home/asigan/python-torrent-scrapper/examples/ttlkrarbg.html')
piratebay_magnet = open('/home/asigan/python-torrent-scrapper/examples/gotTPB.html')

class ScrapperEngine():

    def __init__(self):
        # rs.RarbgScrapper(),
        self.webscrappers = [pbs.PirateBayScrapper()]
        return

    # it takes torrrent instances and takes de decisions!
    def multi_search(self, quality, title, season, subber):
        return


    def single_search(self, quality, title, year, season, episode, subber):
        torrent_list = []

        try:
            for webscrappers in self.webscrappers:
                web_url = webscrappers._build_film_request(title=title, year=year)  # add quality to the search
                print web_url
                response = self.websearch(url=web_url)
                torrent_instance = webscrappers.webscrapper(content=response.text)
                torrent_list.append(torrent_instance)

            return
        except:
            print 'There was a problem in single_search function!'
            return

    def search(self, quality, title, year, season, episode, subber):
        torrent_list = []

        if (title and year) is not None:
            for webscrappers in self.webscrappers:
                sleep(randint(2, 3))
                web_url = webscrappers._build_film_request(quality=quality, title=title, year=year)  # add quality to the search
                print web_url
                response = self.websearch(url=web_url)
                torrent_instance = webscrappers.webscrapper(content=response.text)
                torrent_list.append(torrent_instance)
                sleep(randint(1, 2))
            return torrent_list

        elif ((title and episode) is not None) and subber is True:
            print 'This is a anime show'
            return

        elif (title and season and episode) is not None:
            for webscrappers in self.webscrappers:
                sleep(randint(2, 3))
                web_url = webscrappers._build_show_request(quality=quality, title=title, season=season, episode=episode)  # add quality to the search
                print web_url
                response = self.websearch(url=web_url)
                torrent_instance = webscrappers.webscrapper(content=response.text)
                torrent_list.append(torrent_instance)
                sleep(randint(1, 2))
            return torrent_list

        elif (title and season) is not None:
            print 'This is a season of a show'
            return

        return

        # PANDAS
        # df=DataFrame({'tname':myNameList,'tsize':mySizeList,'tseed':mySeedList,'tleech':myLeechList,'tmagnet':myMagnetList})
        # df['thealth'] = (df['tseed']*100)/(df['tseed']+df['tleech']+0.00000001) # Calculating Torrent Health
        # df = df[df['thealth'] > 50]     #Filter THealth > 50%
        # df = df[df['tsize'] > 500]      #Filter Tam < 600MB
        # df = df.reset_index(drop=True)  #Reset the index to avoid (0,4,7...)
    def websearch (self, url):
        headers = {'UserAgent':str(UserAgent().random)}
        try:
            r = requests.get (url, verify=True, headers=headers)
            return r
        except Exception as e:
            print 'Unable to stablish connection'


    def create_data_frame(self, torrent=None):


        dict = {'name': torrent.namelist,
                'size': torrent.sizelist,
                'seed': torrent.seedlist,
                'leech': torrent.leechlist,
                'magnet': torrent.magnetlist
                }

        dataframe = DataFrame(dict)
        print(dataframe)
        return dataframe