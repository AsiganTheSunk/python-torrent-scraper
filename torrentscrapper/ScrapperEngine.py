#!/usr/bin/env python

from torrentscrapper.webscrappers import PirateBayScraper as pbs
from torrentscrapper.webscrappers import KatScraperTypeA as katsta
from torrentscrapper.webscrappers import KatScraperTypeB as katstb
from torrentscrapper.webscrappers import TorrentFunkScraper as tfs
from torrentscrapper.webscrappers import RarbgScraper as rbgs
from torrentscrapper.struct import WebSearch as ws
from torrentscrapper.webscrappers.utils.UriBuilder import UriBuilder
from torrentscrapper.webscrappers.utils.rarbg_bypass.ThreadDefenceBypass import ThreatDefenceBypass

import requests
import pandas as pd
import numpy as np
from pandas import DataFrame
from fake_useragent import UserAgent
from time import sleep
from random import randint
import cfscrape

pd.set_option('display.max_rows', 750)
pd.set_option('display.max_columns',750)
pd.set_option('display.width', 1400)

FILM_FLAG = 'FILM'
SHOW_FLAG = 'SHOW'
ANIME_FLAG = 'ANIME'

class ScrapperEngine():
    def __init__(self):
        self.name = self.__class__.__name__
        self.webscrappers =  [rbgs.RarbgScrapper()] #[tfs.TorrentFunkScraper(), katsta.KatScrapperTypeA(), katstb.KatScrapperTypeB(), pbs.PirateBayScraper()]

    def retrieve_cloudflare_cookie(self, uri, debug=False):
        cloudflare_cookie, agent = cfscrape.get_tokens(uri, UserAgent().random)
        if debug:
            print('%s retrieving cloudflare cookie: \n %s' % (self.name, cloudflare_cookie))
        return cloudflare_cookie, agent

    def retrieve_missing_magnets(self, torrent, webscrapper):
        headers = {'User-Agent': str(UserAgent().random)}
        if torrent.magnetlist is not [] and len(torrent.magnetlist) >= 1:
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
                            print ('%s unable to retrieve the magnets, try again later ...' % webscrapper.name)
                return torrent
        return torrent

    def search(self, title='', year='', season='', episode='', quality='', header='', search_type='', debug=False):
        torrent_list = []
        websearch = ws.WebSearch(title=title, year=year, season=season, episode=episode, quality=quality, header=header, search_type=search_type)
        for webscrapper in self.webscrappers:
            if search_type in webscrapper.supported_searchs:
                print('%s selected proxy: [ %s ]' % (webscrapper.name, webscrapper.main_page))
                response = self.dynamic_search(websearch, webscrapper, debug=debug)
                if response is not None:
                    torrent_instance = webscrapper.webscrapper(content=response.text, search_type=search_type, size_type=websearch.quality, debug=debug)
                    torrent_list.append(self.retrieve_missing_magnets(torrent_instance, webscrapper))
                    sleep(randint(0, 1))
        return torrent_list

    def dynamic_search (self, websearch, webscraper, counter=0, max_counter=3, debug=True):
        response = None
        headers = {}
        cloudflare_cookie = {}
        user_agent = {'User-Agent':str(UserAgent().random)}
        try:
            uri_builder = UriBuilder()
            search_uri = uri_builder.build_request_url(websearch=websearch, webscraper=webscraper, debug=debug)

            try:
                if webscraper.cloudflare_cookie:
                    cloudflare_cookie, user_agent = self.retrieve_cloudflare_cookie(uri=search_uri, debug=debug)
                    headers = {'User-Agent':user_agent}
                else:
                    headers = user_agent
            except Exception as e:
                # print(e)
                if debug:
                    print('Something went wrong with cloud flare cookie retrieval')

            print('%s searching: [ %s ]' % (webscraper.name, search_uri))
            response = requests.get(search_uri, verify=True, headers=headers, cookies=cloudflare_cookie)

            if webscraper.thread_defense_bypass_cookie:
                if response.history:
                    print('Request was redirected')
                    for resp in response.history:
                        print(resp.status_code, resp.url)
                    print('Final destination:')
                    print(response.status_code, response.url)
                    thread_defense_bypass = ThreatDefenceBypass()
                    #thread_defense_bypass_cookie =  thread_defense_bypass(url=response.url)

            return response

        except Exception as e:
            print('error:',e)
            if counter >= max_counter:
                try:
                    sleep(randint(1, 2))
                    print('%s connection failed multiple times, trying a new proxy: [ %s ]' % (webscraper.name,  webscraper.proxy_list[webscraper._proxy_list_pos]))
                    updated_webscraper = webscraper.update_main_page()
                    return self.dynamic_search(websearch, updated_webscraper, counter)
                except Exception:
                    return None
            else:
                print('%s connection failed, retrying in a few seconds ...\n [%s]' % (webscraper.name, webscraper.proxy_list[webscraper._proxy_list_pos]))
                counter += 1
                sleep(randint(1, 2))
                return self.dynamic_search(websearch, webscraper, counter)

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

        print ('-----------------' * 8 + '\n')
        print ('Full Search')
        print (dataframe)
        dataframe = self.filter_data_frame(dataframe)
        dataframe = dataframe.sort_values(by=['seed', 'ratio'], ascending=False)
        print ('\n')
        print ('-----------------' * 8 + '\n')
        print ('Top Candidates selected from WebScrapping')
        result_dataframe = dataframe[:1].reset_index(drop=True)
        print (result_dataframe)
        print ('-----------------' * 8 + '\n')
        return result_dataframe
