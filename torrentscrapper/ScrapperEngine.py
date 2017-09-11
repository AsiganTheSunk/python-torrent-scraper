#!/usr/bin/env python

from torrentscrapper.webscrappers import RarbgScrapper as rs
from torrentscrapper.webscrappers import PirateBayScrapper as pbs
from torrentscrapper.webscrappers import KatScrapper as kats

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
        self.webscrappers = [kats.KatScrapper(), rs.RarbgScrapper(), pbs.PirateBayScrapper()]
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
                # TODO till cloudflare/bot detection solved we use dummy .html file for testing
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
        return dataframe


    def filter_data_frame(self, dataframe):

        # df['health'] = (df['seed']*100)/(df['seed']+df['leech']+0.00000001)
        # df = df[df['health'] > 60]

        dataframe['ratio'] = (dataframe['seed'] / dataframe['leech'])
        dataframe = dataframe[dataframe['ratio'] > 1.0]

        # Size limitations
        # TODO read from .cfg so you can implement the range for 480p.Anime, 480p.Serie ...
        dataframe = dataframe[dataframe['size'] > 1500]
        dataframe = dataframe[dataframe['size'] < 3000]

        # Reset the index to avoid (0, 4, 7, ...)
        dataframe = dataframe.reset_index(drop=True)
        return dataframe

    def unifiy_torrent_table(self, torrents):

        # Pre-calculating the ratio on the tables to use it on the filtering
        ini_dataframe = self.create_data_frame(torrents[0])

        for i in range(1, len(torrents), 1):
            ini_dataframe['ratio'] = (ini_dataframe['seed'] / ini_dataframe['leech'])
            tmp_dataframe = self.create_data_frame(torrents[i])
            tmp_dataframe['ratio'] = (tmp_dataframe['seed'] / tmp_dataframe['leech'])

            # Create the intersection of the 2 tables so we can retrieve the common entries
            cmmn_dataframe = pd.merge(ini_dataframe, tmp_dataframe, how='inner', on=['name'])

            conditions = [cmmn_dataframe['ratio_x'] > cmmn_dataframe['ratio_y'],
                          cmmn_dataframe['ratio_y'] > cmmn_dataframe['ratio_x'],
                          cmmn_dataframe['ratio_x'] == cmmn_dataframe['ratio_y']]

            leech_choices = [cmmn_dataframe['leech_x'], cmmn_dataframe ['leech_y'], cmmn_dataframe['leech_x']]
            seed_choices = [cmmn_dataframe['seed_x'], cmmn_dataframe ['seed_y'], cmmn_dataframe['leech_y']]
            magnet_choices = [cmmn_dataframe['magnet_x'], cmmn_dataframe['magnet_y'], cmmn_dataframe['magnet_y']]
            size_choices = [cmmn_dataframe['size_x'], cmmn_dataframe['size_y'], cmmn_dataframe['size_y']]

            # Calculate the winners
            cmmn_dataframe['size'] = np.select(conditions, size_choices, default=np.nan)
            cmmn_dataframe['seed'] = np.select(conditions, seed_choices, default=np.nan)
            cmmn_dataframe['leech'] = np.select(conditions, leech_choices, default=np.nan)
            cmmn_dataframe['magnet'] = np.select(conditions, magnet_choices, default=np.nan)

            print 'cmmn_dataframe'
            print cmmn_dataframe
            print '------------------' * 5

            # Reshape the table, there it's no longer need for the _x and _y entries
            tmp_result = cmmn_dataframe[['name', 'size', 'seed', 'leech', 'magnet']]
            print 'TEMP RESULT'
            print tmp_result
            print '::::::::::::::::::' * 5

            # Remove cmmn name entries from the 2 tables that we're crossing
            aux_names = DataFrame()
            aux_names['name'] = tmp_result['name']

            for index in range(0, len(aux_names.index), 1):
                name = aux_names.iloc[int(index)]['name']
                ini_dataframe = ini_dataframe[ini_dataframe.name != name]
                tmp_dataframe = tmp_dataframe[tmp_dataframe.name != name]

            ini_dataframe = pd.concat([tmp_result, ini_dataframe, tmp_dataframe])
            # Reset the index to avoid (0, 4, 7, ...) and Re-arrange the columns in a proper way
            ini_dataframe = ini_dataframe[['name', 'size', 'seed', 'leech', 'magnet']].reset_index(drop=True)

            print 'dataframe ini'
            print ini_dataframe
            print '000000000' * 7

        return ini_dataframe

    def calculate_top_spot(self, dataframe):

        print '-----------------' * 5
        print 'Full Search'
        print dataframe
        dataframe = self.filter_data_frame(dataframe)
        dataframe = dataframe.sort_values(by=['seed', 'ratio'], ascending=False)
        print dataframe
        print '\n'
        print 'Top 10 Torrents selected from Scrappers'
        result_dataframe = dataframe[:10].reset_index(drop=True)
        print result_dataframe
        print '-----------------' * 5
        return result_dataframe
