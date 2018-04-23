#!/usr/bin/env python

from torrentscraper.webscrapers import pirate_bay_scraper as tpb
from torrentscraper.webscrapers import kat_scraper_type_a as kata
from torrentscraper.webscrapers import kat_scraper_type_b as katb
from torrentscraper.webscrapers import torrent_funk_scraper as funk

from torrentscraper.datastruct.websearch import WebSearch
from torrentscraper.datastruct.p2p_instance import P2PInstance
from torrentscraper.webscrapers.utils.uri_builder import UriBuilder
from torrentscraper.webscrapers.utils.rarbg_bypass.thread_defence_bypass import ThreatDefenceBypass
from torrentscraper.webscrapers.utils.magnet_builder import MagnetBuilder

import requests
import pandas as pd
import numpy as np
from pandas import DataFrame
from fake_useragent import UserAgent
from time import sleep
from random import randint
import cfscrape
import tempfile
import shutil

pd.set_option('display.max_rows', 750)
pd.set_option('display.max_columns',750)
pd.set_option('display.width', 1400)

FILM_FLAG = 'FILM'
SHOW_FLAG = 'SHOW'
ANIME_FLAG = 'ANIME'


class ScrapperEngine(object):
    def __init__(self):
        self.name = self.__class__.__name__
        # Queda por resolver el problema de los webdrivers. rbg.RarbgScrapper()
        self.webscrapers = [tpb.PirateBayScraper(), funk.TorrentFunkScraper()]

    def retrieve_cloudflare_cookie(self, uri, debug=False):
        '''
        This function, retrieves the cloudflare_cookie using the cfscrape library
        :param uri: this value, represents the http, https request
        :type uri: str
        :param debug:
        :type debug: bool
        :return: the function, returns the cookie, and the user_agent associated with the request
        :rtype: cloudflare_cookie, user_agent
        '''
        cloudflare_cookie, agent = cfscrape.get_tokens(uri, UserAgent().random)
        if debug:
            print('%s retrieving cloudflare cookie: \n %s' % (self.name, cloudflare_cookie))
        return cloudflare_cookie, agent

    def _normalize_magnet_entries(self, raw_data, webscraper):
        '''
        This function, will retrieve the missing magnet on a parsed source, if it's unable to retrieve a conventional
        magnet
        :param torrent: this value, represents a TorrentInstance
        :type torrent: TorentInstance
        :param webscraper: this value, represents the webscraper class being used
        :type webscraper WebScraper
        :return: this function, returns the *.torrent file or missing magnet associated
        :rtype: *.torrent or magnet
        '''
        magnet_instance_list = []
        mbuilder = MagnetBuilder()
        headers = {'User-Agent': str(UserAgent().random)}

        if '.torrent' in raw_data.magnet_list[0]:
            for index in range(0, len(raw_data.magnet_list), 1):
                try:
                    temp_torrent = './temp_torrent.torrent'
                    response = requests.get(raw_data.magnet_list[index], verify=True, headers=headers)
                    torrent = webscraper.get_magnet_link(response.text)
                    raw_data.magnet_list[index] = torrent
                    torrent_response = requests.get(torrent, verify=True, headers=headers)
                    with open(temp_torrent, 'wb', encoding=torrent_response.encoding) as file:
                        file.write(torrent_response.content)

                    mbuilder.parse_from_file(temp_torrent)
                    magnet_instance_list.append(mbuilder.parse_from_file(temp_torrent, size=raw_data.size_list[index],
                                                                         seed=raw_data.seed_list[index],
                                                                         leech=raw_data.leech_list[index]))
                except Exception as e:
                    print('{0}: Unable to Retrieve Magnets from Search Result, Try Again Later\n Error: {1}'.format(webscraper.name, str(e)))

        elif 'magnet:' not in raw_data.magnet_list[0]:
            for index in range(0, len(raw_data.magnet_list), 1):
                try:
                    response = requests.get(raw_data.magnet_list[index], verify=True, headers=headers)
                    magnet = webscraper.get_magnet_link(response.text)
                    raw_data.magnet_list[index] = magnet
                    magnet_instance_list.append(mbuilder.parse_from_magnet(raw_data.magnet_list[index],
                                                                           raw_data.size_list[index],
                                                                           raw_data.seed_list[index],
                                                                           raw_data.leech_list[index]))
                except Exception as e:
                    print('{0}: Unable to Retrieve Magnets from Search Result, Try Again Later\n Error: {1}'.format(webscraper.name, str(e)))
        else:
            for index in range(0, len(raw_data.magnet_list), 1):
                try:
                    magnet_instance_list.append(mbuilder.parse_from_magnet(raw_data.magnet_list[index],
                                                                           raw_data.size_list[index],
                                                                           raw_data.seed_list[index],
                                                                           raw_data.leech_list[index]))
                except Exception as e:
                    print('{0}: Unable to Retrieve Magnets from Search Result, Try Again Later\n Error: {1}'.format(webscraper.name, str(e)))
        return magnet_instance_list

    def search(self, title='', year='', season='', episode='', quality='', header='', search_type='', size_limit='', debug=False):
        '''
        This functions generates the search process
        :param title: this value, represents the title of multimedia file
        :type title: str
        :param year: this value, represents the year of a multimedia file
        :type year: str
        :param season: this value, represents the season of a multimedia file
        :type season: str
        :param episode: this value, represents the episode of a multimedia file
        :type episde: str
        :param quality: this value, represents the quality of a multimedia file
        :type quality: str
        :param header: this value, represents the header of a multimedia file
        :type header: str
        :param search_type: this value, represents the type of a multimedia file
        :type search_type: str
        :param debug: COPY PASTE FROM OTHER FUNCTIONS
        :type debug: bool
        :return: this function returns, a list with a bunch of TorrentInstances
        :rtype: list
        '''
        websearch = WebSearch(title, year, season, episode, quality, header, search_type, size_limit)
        p2p_instance_list = []
        for webscraper in self.webscrapers:
            magnet_instance_list = []
            raw_data = None
            response = None
            if search_type in webscraper.supported_searchs:
                print('%s selected proxy: [ %s ]' % (webscraper.name, webscraper.main_page))
                response = self.dynamic_search(websearch, webscraper, debug)
                if response is not None:
                    raw_data = webscraper.get_raw_data(content=response.text)
                    sleep(randint(0, 2))  # Random Sleep to avoid flooding
                    magnet_instance_list = self._normalize_magnet_entries(raw_data, webscraper)
                    #raw_data.list()

            p2p_instance_list.append(P2PInstance(webscraper.name, websearch.search_type,
                                                 websearch.size_limit, magnet_instance_list))

        return p2p_instance_list

    def dynamic_search (self, websearch, webscraper, counter=0, max_counter=3, debug=True):
        '''
        This function executes the core process of each search, using all avaliable scrapers in the system
        :param websearch:
        :type webscraper: WebSearch
        :param webscraper:
        :type webscraper: WebScraper
        :param counter:
        :type counter: int
        :param max_counter:
        :type max_counter: int
        :param debug:
        :type debug: bool
        :return:
        :rtype: Response
        '''
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
                # return None
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

    def create_dataframe(self, p2p_instance):
        for item_list in p2p_instance.magnet_instance_list:
            for item in item_list:
                print()
        return


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
        mbuilder = MagnetBuilder()

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

                # Reshape the table, there it's no longer need for the _x and _y entries
                tmp_result = cmmn_dataframe[['name', 'size', 'seed', 'leech', 'magnet']]

                separator = '*********' * 5
                print('%s\nCommon DataFrame:\n%s\n%s ' % (separator, tmp_result, separator))

                # Remove cmmn name entries from the 2 tables that we're crossing
                aux_names = DataFrame()
                aux_names['name'] = tmp_result['name']

                for index in range(0, len(aux_names.index), 1):
                    name = aux_names.iloc[int(index)]['name']
                    ini_magnet = ini_dataframe.magnet[ini_dataframe['name'] == name]
                    tmp_magnet = tmp_dataframe.magnet[tmp_dataframe['name'] == name]

                    print(ini_magnet, tmp_magnet)
                    fst_magnet = mbuilder.parse_from_magnet(ini_magnet)
                    snd_magnet = mbuilder.parse_from_magnet(tmp_magnet)

                    zero_magnet = mbuilder.merge_announce_list(fst_magnet, snd_magnet)
                    print(zero_magnet['magnet'], zero_magnet['display_name'])

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
