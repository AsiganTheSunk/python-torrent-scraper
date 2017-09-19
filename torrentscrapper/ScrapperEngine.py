#!/usr/bin/env python

from torrentscrapper.webscrappers import RarbgScrapper as rs
from torrentscrapper.webscrappers import PirateBayScrapper as pbs
from torrentscrapper.webscrappers import KatScrapper as kats
from torrentscrapper import WebSearch as ws

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

FILM_FLAG = 'FILM'
SHOW_FLAG = 'SHOW'
ANIME_FLAG = 'ANIME'

# TODO FALTAN CASOS BASICOS; SI DEVUELVE VACIO; O SI EL PROXY ESTA CAIDO; REINTENTARLO CON UN SEGUNDO

class ScrapperEngine():

    def __init__(self):
        # TODO CLOUDFLARE PROBLEM!
        self.webscrappers = [pbs.PirateBayScrapper(), kats.KatScrapper()] #, rs.RarbgScrapper()
        return

    def human_handshake(self, webscrapper, search_type):
        headers = {'UserAgent': str(UserAgent().random)}
        try:
            print ('%s visiting main page ...' % webscrapper.name)
            requests.get(url=str(webscrapper.main_page + '/'), verify=True, headers=headers)
            sleep(randint(1, 2))

            print ('%s visiting %s page ...' % ((webscrapper.name), str(search_type).lower()))
            if search_type is FILM_FLAG and webscrapper.film_page != '':
               requests.get(url=str(webscrapper.film_page + '/'), verify=True, headers=headers)
               sleep(randint(1, 2))
               return

            elif search_type is SHOW_FLAG and webscrapper.show_page != '':
                requests.get(url=str(webscrapper.show_page + '/'), verify=True, headers=headers)
                sleep(randint(1, 2))
                return

            elif search_type is ANIME_FLAG:
                return
        except Exception as e:
            print e
            print ('%s unable to make human handshake, site may be down ...' % webscrapper.name)
            return

    def search(self, title=None, year=None, season=None, episode=None, quality=None, subber=None):
        torrent_list = []

        if (title and year) is not None:
            websearch = ws.WebSearch(title=title, year=year, season=season, episode=episode, quality=quality, subber=subber, search_type=FILM_FLAG)
            for webscrapper in self.webscrappers:
                if FILM_FLAG in webscrapper.supported_searchs:
                    print('%s selected proxy [ %s ]' % (webscrapper.name, webscrapper.main_page))
                    # Human Handshake, visiting the main page first, then the subsection before we make the search
                    self.human_handshake(webscrapper, FILM_FLAG)
                    response = self.web_search(websearch, webscrapper)
                    if response is not None:
                        torrent_instance = webscrapper.webscrapper(content=response.text, search_type=FILM_FLAG, size_type=websearch.quality)
                        torrent_list.append(self.retrieve_missing_magnets(torrent_instance, webscrapper))
                        sleep(randint(1, 2))

            return torrent_list

        elif (title and season and episode) is not None:
            websearch = ws.WebSearch(title=title, year=year, season=season, episode=episode, quality=quality, subber=subber, search_type=SHOW_FLAG)

            for webscrapper in self.webscrappers:
                print('%s selected proxy [ %s ]' % (webscrapper.name, webscrapper.main_page))
                #Human Handshake, visiting the main page first, then the subsection before we make the search
                self.human_handshake(webscrapper, SHOW_FLAG)
                response = self.web_search(websearch, webscrapper)

                if response is not None:
                    torrent_instance = webscrapper.webscrapper(content=response.text, search_type=SHOW_FLAG, size_type=websearch.quality)
                    torrent_list.append(self.retrieve_missing_magnets(torrent_instance, webscrapper))
                    sleep(randint(1, 2))

            return torrent_list

        elif ((title and episode) is not None) and subber is True:
            print 'This is a anime show'
            return

        elif (title and season) is not None:
            print 'This is a season of a show'
            return
        return

    def web_search (self, websearch, webscrapper, counter = 0, proxy = 0):
        response = None
        headers = {'UserAgent':str(UserAgent().random)}

        try:

            search_url = webscrapper.build_url(websearch=websearch)
            print('%s searching: [ %s ]' % (webscrapper.name, search_url))
            response = requests.get(search_url, verify=True, headers=headers)
            return response

        except Exception as e:
            if counter >= 2:
                proxy += 1
                counter = 0

                if len(webscrapper.proxy_list) > proxy:
                    sleep(randint(1, 2))
                    print('%s connection failed multiple times, trying a new proxy [ %s ]' % (webscrapper.name,  webscrapper.proxy_list[proxy]))
                    webscrapper.update_main_page(webscrapper.proxy_list[proxy])
                    return self.web_search(websearch, webscrapper, counter, proxy)
                else:
                    return None

            else:
                print('%s connection failed, retrying in a few seconds ...' % webscrapper.name)
                counter += 1
                sleep(randint(1, 2))
                return self.web_search(websearch, webscrapper, counter, proxy)

    def retrieve_missing_magnets(self, torrent, webscrapper):
        headers = {'UserAgent': str(UserAgent().random)}

        if torrent.magnetlist is not [] and len(torrent.magnetlist) > 1:
            # Avoiding checking sites that don't need the second search to retrieve the data
            if 'magnet:' not in torrent.magnetlist[0] :
                print ('%s retrieving magnet links ...\n' % webscrapper.name)
                for index in range(0, len(torrent.magnetlist), 1):
                    if 'magnet:' not in torrent.magnetlist[index]:
                        try:
                            response = requests.get(torrent.magnetlist[index], verify=True, headers=headers)
                            magnet = webscrapper.magnet_link_scrapper(response.text)
                            torrent.magnetlist[index] = magnet
                        except:
                            print ('%s unable to retrieve the magnets, try again later ...\n' % webscrapper.name)
                return torrent
        return torrent

    '''
        
        DATAFRAME SECCTION
        
        Functions to treat the data we obtain from the scrapping.
        
    '''

    def create_table(self, torrent=None):

        raw_data = {'name': torrent.namelist,
                    'size': torrent.sizelist,
                    'seed': torrent.seedlist,
                    'leech': torrent.leechlist,
                    'magnet': torrent.magnetlist
                    }

        dataframe = DataFrame(raw_data, columns=['name', 'size', 'seed', 'leech', 'magnet'])
        return dataframe

    def filter_data_frame(self, dataframe, size_limit=False):

        # Old ratio
        # df['health'] = (df['seed']*100)/(df['seed']+df['leech']+0.00000001)
        # df = df[df['health'] > 60]

        # Setting up the ratio
        dataframe['ratio'] = (dataframe['seed'] / dataframe['leech'])
        dataframe = dataframe[dataframe['ratio'] > 0.1]

        # Filtering by Size
        # TODO read from .cfg so you can implement the range for 480p.Anime, 480p.Serie ...
        if size_limit is True:

            dataframe = dataframe[dataframe['size'] > 300]
            dataframe = dataframe[dataframe['size'] < 500]

        # Reset the index to avoid (0, 4, 7, ...)
        dataframe = dataframe.reset_index(drop=True)
        return dataframe

    def unifiy_torrent_table(self, torrents, size_limit=False):
        # Pre-calculating the ratio on the tables to use it on the filtering
        ini_dataframe = self.create_table(torrents[0])

        if (len(torrents) > 1 or torrents is []):
            for i in range(1, len(torrents), 1):
                # print 'iteracion: ', i
                ini_dataframe['ratio'] = (ini_dataframe['seed'] / ini_dataframe['leech'])
                tmp_dataframe = self.create_table(torrents[i])
                tmp_dataframe['ratio'] = (tmp_dataframe['seed'] / tmp_dataframe['leech'])

                # Create the intersection of the 2 tables so we can retrieve the common entries
                cmmn_dataframe = pd.merge(ini_dataframe, tmp_dataframe, how='inner', on=['name'])

                conditions = [cmmn_dataframe['ratio_x'] > cmmn_dataframe['ratio_y'],
                              cmmn_dataframe['ratio_y'] > cmmn_dataframe['ratio_x'],
                              cmmn_dataframe['ratio_x'] == cmmn_dataframe['ratio_y']]

                leech_choices = [cmmn_dataframe['leech_x'], cmmn_dataframe ['leech_y'], cmmn_dataframe['leech_x']]
                seed_choices = [cmmn_dataframe['seed_x'], cmmn_dataframe ['seed_y'], cmmn_dataframe['seed_y']]
                magnet_choices = [cmmn_dataframe['magnet_x'], cmmn_dataframe['magnet_y'], cmmn_dataframe['magnet_y']]
                size_choices = [cmmn_dataframe['size_x'], cmmn_dataframe['size_y'], cmmn_dataframe['size_y']]

                # Calculate the winners
                cmmn_dataframe['size'] = np.select(conditions, size_choices, default=np.nan)
                cmmn_dataframe['seed'] = np.select(conditions, seed_choices, default=np.nan)
                cmmn_dataframe['leech'] = np.select(conditions, leech_choices, default=np.nan)
                cmmn_dataframe['magnet'] = np.select(conditions, magnet_choices, default=np.nan)

                # print 'cmmn_dataframe'
                # print cmmn_dataframe
                # print '------------------' * 5

                # Reshape the table, there it's no longer need for the _x and _y entries
                tmp_result = cmmn_dataframe[['name', 'size', 'seed', 'leech', 'magnet']]

                # Remove cmmn name entries from the 2 tables that we're crossing
                aux_names = DataFrame()
                aux_names['name'] = tmp_result['name']

                for index in range(0, len(aux_names.index), 1):
                    name = aux_names.iloc[int(index)]['name']
                    ini_dataframe = ini_dataframe[ini_dataframe.name != name]
                    tmp_dataframe = tmp_dataframe[tmp_dataframe.name != name]

                # merging the filtered results
                ini_dataframe = pd.concat([tmp_result, ini_dataframe, tmp_dataframe])

                # Reset the index to avoid (0, 4, 7, ...) and Re-arrange the columns in a proper way
                ini_dataframe = ini_dataframe[['name', 'size', 'seed', 'leech', 'magnet']].reset_index(drop=True)

        return ini_dataframe

    def calculate_top_spot(self, dataframe):

        print '-----------------' * 8 + '\n'
        print 'Full Search'
        print dataframe
        dataframe = self.filter_data_frame(dataframe)
        dataframe = dataframe.sort_values(by=['seed', 'ratio'], ascending=False)
        print '\n'
        print '-----------------' * 8 + '\n'
        print 'Top Candidates selected from WebScrapping'
        result_dataframe = dataframe[:1].reset_index(drop=True)
        print result_dataframe
        print '-----------------' * 8 + '\n'
        return result_dataframe
