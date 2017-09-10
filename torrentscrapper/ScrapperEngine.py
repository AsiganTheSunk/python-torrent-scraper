#!/usr/bin/env python

from torrentscrapper.webscrappers import RarbgScrapper as rs
from torrentscrapper.webscrappers import PirateBayScrapper as pbs

import requests
import pandas as pd
import numpy as np
from pandas import DataFrame
from fake_useragent import UserAgent
from time import sleep
from random import randint

pd.set_option('display.max_rows', 750)
pd.set_option('display.max_columns',750)
pd.set_option('display.width', 1400)

rarbg_file = open('/home/asigan/python-torrent-scrapper/examples/Baywatch2017.html')
piratebay_file = open('/home/asigan/python-torrent-scrapper/examples/thepiratebayexample.html')
rarbg_magnet = open('/home/asigan/python-torrent-scrapper/examples/ttlkrarbg.html')
piratebay_magnet = open('/home/asigan/python-torrent-scrapper/examples/gotTPB.html')


class ScrapperEngine():

    def __init__(self):
        # rs.RarbgScrapper(),
        self.webscrappers = [rs.RarbgScrapper(),pbs.PirateBayScrapper()]
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
                # Main Page
                self.websearch(url = webscrappers.main_landing_page)
                sleep(randint(2, 3))
                print ('%s visiting main landing page ...' % webscrappers.name)
                # Shows Page
                if webscrappers.film_landing_page != '':
                    self.websearch(url = webscrappers.film_landing_page)
                    sleep(randint(1, 3))
                    print ('%s visiting films landing page ...' % webscrappers.name)
                # Searched Page
                web_url = webscrappers._build_film_request(quality=quality, title=title, year=year)
                response = self.websearch(url=web_url)
                if webscrappers.name is 'RarbgScrapper':
                    torrent_instance = webscrappers.webscrapper(content=rarbg_file)
                else:
                    torrent_instance = webscrappers.webscrapper(content=response.text)
                torrent_list.append(torrent_instance)
                sleep(randint(1, 2))
            return torrent_list

        elif ((title and episode) is not None) and subber is True:
            print 'This is a anime show'
            return

        elif (title and season and episode) is not None:
            for webscrappers in self.webscrappers:
                # Main Page
                self.websearch(url = webscrappers.main_landing_page)
                sleep(randint(2, 3))
                print ('%s visiting main landing page ...' % webscrappers.name)
                # Shows Page
                if webscrappers.film_landing_page != '':
                    self.websearch(url = webscrappers.film_landing_page)
                    sleep(randint(1, 3))
                    print ('%s visiting films landing page ...' % webscrappers.name)
                # Searched Page
                web_url = webscrappers._build_show_request(quality=quality, title=title, season=season, episode=episode)
                response = self.websearch(url=web_url)
                torrent_instance = webscrappers.webscrapper(content=response.text)
                torrent_list.append(torrent_instance)
                sleep(randint(1, 2))
            return torrent_list

        elif (title and season) is not None:
            print 'This is a season of a show'
            return

        return


    def websearch (self, url):
        headers = {'UserAgent':str(UserAgent().random)}
        try:
            r = requests.get (url, verify=True, headers=headers)
            return r
        except Exception as e:
            print 'Unable to stablish connection'


    def create_data_frame(self, torrent=None):

        raw_data = {'name': torrent.namelist,
                    'size': torrent.sizelist,
                    'seed': torrent.seedlist,
                    'leech': torrent.leechlist,
                    'magnet': torrent.magnetlist
                    }

        dataframe = DataFrame(raw_data, columns=['name', 'size', 'seed', 'leech', 'magnet'])
        print(dataframe)

        return dataframe


    def filter_data_frame(self, df):

        df['health'] = (df['seed']*100)/(df['seed']+df['leech']+0.00000001)
        df['ratio'] = (df['seed']/df['leech'])
        #print ('\n')
        #print df

        df = df[df['ratio'] > 1.0]
        df = df[df['health'] > 60]
        df = df[df['size'] > 1500]
        df = df[df['size'] < 3000]

        df = df.reset_index(drop=True)  #Reset the index to avoid (0,4,7...)
        return df

    def unify_torrent_table(self, torrent0, torrent1):
        t0 = self.create_data_frame(torrent0)
        t0['ratio'] = (t0['seed'] / t0['leech'])
        t1 = self.create_data_frame(torrent1)
        t1['ratio'] = (t1['seed'] / t1['leech'])
        dataframe = pd.merge(t0, t1, how='inner', on=['name'])

        df = dataframe

        print 'original'
        print df

        conditions = [df['ratio_x'] > df['ratio_y'], df['ratio_y'] > df['ratio_x'] ]
        leech_choices = [df['leech_x'], df['leech_y']]
        seed_choices = [df['seed_x'], df['seed_y']]
        magnet_choices = [df['magnet_x'], df['magnet_y']]
        size_choices = [df['size_x'], df['size_y']]

        df['leech'] = np.select(conditions, leech_choices, default=np.nan)
        df['seed'] = np.select(conditions, seed_choices, default=np.nan)
        df['magnet'] = np.select(conditions, magnet_choices, default=np.nan)
        df['size'] = np.select(conditions, size_choices, default=np.nan)

        del df['seed_x']
        del df['leech_x']
        del df['seed_y']
        del df['leech_y']
        del df['magnet_x']
        del df['magnet_y']
        del df['size_x']
        del df['size_y']
        del df['ratio_x']
        del df['ratio_y']

        print df

        print 'clean the other tables'
        names = DataFrame()
        names['name'] = df['name']
        # print names

        for index in range(0, len(names.index), 1):
            name = names.iloc[int(index)]['name']
            t0 = t0[t0.name != name]
            t1 = t1[t1.name != name]

        print '--------------' * 10
        dataframe = pd.concat([df, t0, t1])

        dataframe = dataframe[['name', 'size', 'seed', 'leech', 'magnet']]
        print '\n'
        print 'Full Search Unfiltered'
        print dataframe
        dataframe = self.filter_data_frame(dataframe)
        print '\n'
        print 'Full Search Filtered'
        print '\n'
        result = dataframe.sort_values(by=['seed','ratio'],ascending=False)
        print result
        print '\n'
        print 'Top 5 Torrents Selected from this search'
        print result[:10].reset_index(drop=True)


