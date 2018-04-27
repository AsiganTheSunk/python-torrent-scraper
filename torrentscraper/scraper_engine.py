#!/usr/bin/env python

# Import System Libraries
from time import sleep
from random import randint
from logging import setLoggerClass
import logging

# Import External Libraries
import requests
import cfscrape
import pandas as pd
from pandas import DataFrame
from fake_useragent import UserAgent

# Import Custom Data Structure
from torrentscraper.datastruct.websearch import WebSearch
from torrentscraper.datastruct.p2p_instance import P2PInstance

# Import Custom Logger
from torrentscraper.utils.custom_logger import CustomLogger

# Import Custom WebScraper
from torrentscraper.webscrapers import kat_scraper_type_a as kata
from torrentscraper.webscrapers import pirate_bay_scraper as tpb
from torrentscraper.webscrapers import torrent_funk_scraper as funk

# Import Custom Exceptions
from torrentscraper.webscrapers.exceptions.web_scraper_error import WebScraperProxyListError
from torrentscraper.webscrapers.exceptions.web_scraper_error import WebScraperParseError

# Import Custom Utils
from torrentscraper.webscrapers.utils.uri_builder import UriBuilder
from torrentscraper.webscrapers.utils.magnet_builder import MagnetBuilder

# Pandas Terminal Configuration
pd.set_option('display.max_rows', 750)
pd.set_option('display.max_columns',750)
pd.set_option('display.width', 1400)

# Constants
line = '-----------------------' * 8
FILM_FLAG = 'FILM'
SHOW_FLAG = 'SHOW'
ANIME_FLAG = 'ANIME'


# TODO Resolver problema de webdrivers. rbg.RarbgScrapper()
class ScrapperEngine(object):
    def __init__(self):
        self.name = self.__class__.__name__
        self.webscrapers = [kata.KatScrapperTypeA(), tpb.PirateBayScraper(), funk.TorrentFunkScraper()]

        # Create & Config CustomLogger
        self.logger = CustomLogger(__name__, logging.INFO)
        formatter = logging.Formatter(fmt='%(asctime)s -  [%(levelname)s]: - %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')
        file_handler = logging.FileHandler('scraper_engine.log', 'w')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)

    def retrieve_cloudflare_cookie(self, uri, debug=False):
        '''
        This function, retrieves the cloudflare_cookie using the cfscrape library
        :param uri: this value, represents the http, https request
        :type uri: str
        :param debug: this value, sets the function in debug mode, printing some additional info about the operations
        :type debug: bool
        :return: the function, returns the cookie, and the user_agent associated with the request
        :rtype: cloudflare_cookie, user_agent
        '''
        cloudflare_cookie, user_agent = cfscrape.get_tokens(uri, UserAgent().random)
        if debug:
            print('{0} Retrieving Cloudflare Cookie: \n{1}'.format(self.name, cloudflare_cookie))
        return cloudflare_cookie, user_agent

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

        # TODO Buscar una manera mejor de hacerlo, mover el retrieval y luego ver que es y hacer la accion pertinente.
        if 'torrentfunk' in raw_data.magnet_list[0]:
            print('[INFO]: {0} Retrieving Torrent File from Proxy [ {1} ]'.format(webscraper.name, webscraper.main_page))
            self.logger.info('{0} Retrieving Torrent File from Proxy [ {1} ]'.format(webscraper.name, webscraper.main_page))
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
                    print('{0} Unable to Retrieve Torrent File from Search Result, Try Again Later\n Error: {1}'.format(webscraper.name, str(e)))
                    self.logger.error('{0} Unable to Retrieve Torrent File from Search Result, Try Again Later\n Error: {1}'.format(webscraper.name, str(e)))

        elif 'magnet:' not in raw_data.magnet_list[0]:
            print('[INFO]: {0} Retrieving Magnet from Proxy [ {1} ]'.format(webscraper.name, webscraper.main_page))
            self.logger.info('{0} Retrieving Magnet from Proxy [ {1} ]'.format(webscraper.name, webscraper.main_page))
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
                    print('{0} Unable to Retrieve Magnets from Search Result, Try Again Later 1\n Error: {1}'.format(webscraper.name, str(e)))
                    #self.logger.error('{0} Unable to Retrieve Magnets from Search Result, Try Again Later\n Error: {1}'.format(webscraper.name, str(e)))
        else:
            for index in range(0, len(raw_data.magnet_list), 1):
                try:
                    magnet_instance_list.append(mbuilder.parse_from_magnet(raw_data.magnet_list[index],
                                                                           raw_data.size_list[index],
                                                                           raw_data.seed_list[index],
                                                                           raw_data.leech_list[index]))
                except Exception as e:
                    print('{0} Unable to Retrieve Magnets from Search Result, Try Again Later 2\n Error: {1}'.format(webscraper.name, str(e)))
                    #self.logger.error('{0} Unable to Retrieve Magnets from Search Result, Try Again Later\n Error: {1}'.format(webscraper.name, str(e)))
        return magnet_instance_list

    def search(self, title='', year='', season='', episode='', quality='', header='', search_type='', lower_size_limit=-1, upper_size_limit=-1, ratio_limit=-1, debug=False):
        '''
        This functions, will run a search process, retrieving info from internet sources
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
        :param lower_size_limit: this value, represents the lower size limit of a multimedia file
        :type lower_size_limit: int
        :param upper_size_limit: this value, represents the upper size limit of a multimedia file
        :type upper_size_limit: int
        :param ratio_limit: this value, represents the ratio limit of a multimedia file
        :type ratio_limit: int
        :param debug: this value, sets the function in debug mode, printing some additional info about the operations
        :type debug: bool
        :return: this function returns, a list with a bunch of TorrentInstances
        :rtype: list
        '''
        websearch = WebSearch(title, year, season, episode, quality, header, search_type, lower_size_limit, upper_size_limit, ratio_limit)
        p2p_instance_list = []
        for webscraper in self.webscrapers:
            magnet_instance_list = []
            raw_data = None
            response = None
            if search_type in webscraper.supported_searchs:
                print('[INFO]: {0} Selected Proxy from List [ {1} ]'.format(webscraper.name, webscraper.main_page))
                response = self.dynamic_search(websearch, webscraper, debug)
                if response is not None:
                    try:
                        raw_data = webscraper.get_raw_data(response.text, debug)

                        # Random Sleep to Avoid Flooding
                        sleep(randint(1, 3))
                        magnet_instance_list = self._normalize_magnet_entries(raw_data, webscraper)
                        p2p_instance_list.append(P2PInstance(webscraper.name, websearch.search_type,
                                                             websearch.lower_size_limit, websearch.upper_size_limit,
                                                             websearch.ratio_limit, magnet_instance_list))
                    except WebScraperParseError as err:
                        print(err.message)
                        self.logger.error(err.message)

        return p2p_instance_list

    def dynamic_search (self, websearch, webscraper, counter=0, max_counter=3, debug=False):
        '''
        This function, executes the core process of each search, using all avaliable scrapers in the system
        :param websearch:
        :type webscraper: WebSearch
        :param webscraper:
        :type webscraper: WebScraper
        :param counter:
        :type counter: int
        :param max_counter:
        :type max_counter: int
        :param debug: this value, sets the function in debug mode, printing some additional info about the operations
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
            search_uri = uri_builder.build_request_url(websearch, webscraper, debug)

            try:
                if webscraper.cloudflare_cookie:
                    cloudflare_cookie, user_agent = self.retrieve_cloudflare_cookie(search_uri, debug)
                    headers = {'User-Agent': user_agent}
                else:
                    headers = user_agent

            except Exception as e:
                print('[INFO]: {0} Error, Something Went Wrong with Cloudflare Cookie Retrieval:\n{1}'.format(webscraper.name, str(e)))

            print('[INFO]: {0} Searching on Proxy [ {1} ]'.format(webscraper.name, search_uri))
            self.logger.info('{0} Searching on Proxy [ {1} ]'.format(webscraper.name, search_uri))
            response = requests.get(search_uri, verify=True, headers=headers, cookies=cloudflare_cookie)

            # if debug and webscraper.thread_defense_bypass_cookie:
            #     if response.history:
            #         print('[INFO]: {0} Request Was Redirected:'.format(self.name))
            #         for resp in response.history:
            #             print('Status Code [ {0} ] :: Uri [ {1} ]'.format(resp.status_code, resp.url))
            #         print('[INFO]: {0} Final Destination:\nStatus Code [ {1} ] :: Uri [ {2} ]'.format(self.name,
            #                                                                                   response.status_code,
            #                                                                                   response.url))
            #         # thread_defense_bypass = ThreatDefenceBypass()
            #         # thread_defense_bypass_cookie =  thread_defense_bypass(url=response.url)
            return response

        except Exception:
            if counter >= max_counter:
                try:
                    sleep(randint(1, 2))
                    webscraper.update_main_page()
                    print('[INFO]: {0} Connection Failed Multiple Times, Trying a New Proxy: [ {1} ]'.format(
                        webscraper.name, webscraper.proxy_list[webscraper._proxy_list_pos]))
                    self.logger.info('{0} Connection Failed Multiple Times, Trying a New Proxy: [ {1} ]'.format(
                        webscraper.name, webscraper.proxy_list[webscraper._proxy_list_pos]))
                    return self.dynamic_search(websearch, webscraper, counter)
                except WebScraperProxyListError as error:
                    self.logger.error(error.message)
                    return None
                except Exception as e:
                    self.logger.error('WebScraperUnkownError, in {0}:\n{1}'.format(self.name, e))
                    return None
            else:
                print('[INFO]: {0} [{1:d}/{2:d}] Connection Failed, Retrying in a Few Seconds [ {3} ]'.format(
                    webscraper.name, counter + 1, max_counter, webscraper.proxy_list[webscraper._proxy_list_pos]))
                self.logger.info('{0} [{1:d}/{2:d}] Connection Failed, Retrying in a Few Seconds [ {3} ]'.format(
                    webscraper.name, counter + 1, max_counter, webscraper.proxy_list[webscraper._proxy_list_pos]))

                counter += 1
                sleep(randint(1, 3))
                return self.dynamic_search(websearch, webscraper, counter)

    def create_magnet_dataframe(self, p2p_instance_list):
        '''
        This function, creates a transforms p2p instance list into a dataframe
        :param p2p_instance_list: this values, respresents a list of p2p instances
        :type p2p_instance_list: list
        :return: this function, returns a dataframe object with the magnet values
        :rtype: DataFrame
        '''
        dataframe = DataFrame()
        for item_list in p2p_instance_list:
            for item in item_list.magnet_instance_list:
                new_row = {'name': [item['display_name']],
                           'hash': [item['hash']],
                           'size': [item['size']],
                           'seed': [item['seed']],
                           'leech': [item['leech']],
                           'ratio': [item['ratio']],
                           'magnet': [item['magnet']]}

                new_row_df = DataFrame(new_row, columns=['name', 'hash', 'size', 'seed', 'leech', 'ratio', 'magnet'])
                dataframe = dataframe.append(new_row_df, ignore_index=True)
        return dataframe

    def unique_magnet_dataframe(self, dataframe, debug=False):
        '''
        This function returns unique hash values from a list of p2p instances
        :param dataframe: this value, represents the dataframe of p2p instances
        :type dataframe: DataFrame
        :param debug: this value, sets the function in debug mode, printing some additional info about the operations
        :type debug: bool
        :return: this function, returns a DataFrame with unique hash values
        :rtype: DataFrame
        '''
        try:
            mbuilder = MagnetBuilder()
            cmmn_hash = dataframe.groupby(['hash'])
            new_dataframe = DataFrame()
            modified_hash = []


            for item_hash in cmmn_hash.groups:
                if len(cmmn_hash.get_group(item_hash)) > 1:
                    modified_hash.append(item_hash)
                    print('[DEBUG]: {0} GroupHash: {1} GroupLen: {2}'.format(self.name, item_hash, len(cmmn_hash.get_group(item_hash))))
                    aux_index = cmmn_hash.get_group(item_hash).index.tolist()[0]
                    tmp_dn = dataframe.iloc[int(aux_index)]['name']
                    tmp_hash = dataframe.iloc[int(aux_index)]['hash']
                    tmp_magnet = dataframe.iloc[int(aux_index)]['magnet']
                    tmp_size = dataframe.iloc[int(aux_index)]['size']
                    tmp_seed = dataframe.iloc[int(aux_index)]['seed']
                    tmp_leech = dataframe.iloc[int(aux_index)]['leech']
                    print('[DEBUG]: {0} Magnet0 Values: {1} {2} {3} {4} {5}'.format(self.name, tmp_dn, tmp_hash, tmp_size, tmp_seed, tmp_leech))
                    aux_magnet_instance = mbuilder.parse_from_magnet(tmp_magnet, tmp_size, tmp_seed, tmp_leech)

                    print('[DEBUG]: {0} Index: {1}\n[DEBUG]: {0} Common DataFrame: {2}\n'.format(self.name, cmmn_hash.get_group(item_hash).index.tolist(), cmmn_hash.get_group(item_hash)))
                    for index in cmmn_hash.get_group(item_hash).index.tolist()[1:]:
                        tmp_dn = dataframe.iloc[int(index)]['name']
                        tmp_hash = dataframe.iloc[int(index)]['hash']
                        tmp_magnet = dataframe.iloc[int(index)]['magnet']
                        tmp_size = dataframe.iloc[int(index)]['size']
                        tmp_seed = dataframe.iloc[int(index)]['seed']
                        tmp_leech = dataframe.iloc[int(index)]['leech']
                        print('[DEBUG]: {0} MagnetAux Values: {1} {2} {3} {4} {5}'.format(self.name, tmp_dn, tmp_hash, tmp_size, tmp_seed, tmp_leech))

                        magnet_instance = mbuilder.parse_from_magnet(tmp_magnet, tmp_size, tmp_seed, tmp_leech)
                        aux_magnet_instance = mbuilder.merge_announce_list(aux_magnet_instance, magnet_instance)
                    print('[DEBUG]: {0} Result MagnetAux Values: {1} {2} {3} {4} {5}'.format(self.name,
                                                                                    aux_magnet_instance['display_name'],
                                                                                    aux_magnet_instance['hash'],
                                                                                    aux_magnet_instance['size'],
                                                                                    aux_magnet_instance['seed'],
                                                                                    aux_magnet_instance['leech']))

                    new_row = {'name': [aux_magnet_instance['display_name']],
                               'hash': [aux_magnet_instance['hash']],
                               'size': [aux_magnet_instance['size']],
                               'seed': [aux_magnet_instance['seed']],
                               'leech': [aux_magnet_instance['leech']],
                               'ratio': [aux_magnet_instance['ratio']],
                               'magnet': [aux_magnet_instance['magnet']]}

                    new_row_df = DataFrame(new_row, columns=['name', 'hash', 'size', 'seed', 'leech', 'ratio', 'magnet'])
                    print('[DEBUG]: {0} Adding Merged GroupHash to Temp DataFrame: [ {1} ]\n'.format(self.name, item_hash))
                    new_dataframe = new_dataframe.append(new_row_df, ignore_index=True)

            print('[DEBUG]: {0} New DataFrame Rows:{1}\n'.format(self.name, new_dataframe))
            for item_hash in modified_hash:
                print('[DEBUG]: {0} Filtering GroupHash from Main DataFrame: [ {1} ]'.format(self.name, item_hash))
                dataframe = dataframe[dataframe['hash'] != item_hash]

            print('[DEBUG]: {0} Adding Merged GroupHash to Main DataFrame\n'.format(self.name))
            dataframe = dataframe.append(new_dataframe, ignore_index=True)
            return dataframe

        except KeyError:
            print('[WARNING]: {0} Unable to Create a Unique Magnet DataFrame: Empty'.format(self.name))
            return dataframe

    def filter_magnet_dataframe(self, dataframe, lower_size_limit=-1, upper_size_limit=-1, ratio_limit=-1):
        '''
        This function, filters the size and ratio values in a dataframe
        :param dataframe: this value, represents the dataframe with the magnet values
        :type dataframe: DataFrame
        :param lower_size_limit: this value, represents the lower size limit of a multimedia file
        :type lower_size_limit: int
        :param upper_size_limit: this value, represents the upper size limit of a multimedia file
        :type upper_size_limit: int
        :param ratio_limit: this value, represents the ratio limit of a multimedia file
        :type ratio_limit: int
        :return: this function, returns a DataFrame with filtered values
        :rtype: DataFrame
        '''
        # Filtering by Health
        # df['health'] = (df['seed']*100)/(df['seed']+df['leech']+0.00000001)
        # df = df[df['health'] > 60]

        # Filtering by Ratio
        try:
            if ratio_limit > 1:
                dataframe = dataframe[dataframe['ratio'] > ratio_limit]

            # Filtering by Size
            if lower_size_limit > 1:
                dataframe = dataframe[dataframe['size'] > lower_size_limit]

            if upper_size_limit > 1:
                dataframe = dataframe[dataframe['size'] < upper_size_limit]

            dataframe = dataframe.reset_index(drop=True)
            return dataframe
        except KeyError:
            print('[WARNING]: {0} Unable to Filter Magnet DataFrame: Empty'.format(self.name))
            return dataframe


    def get_dataframe(self, dataframe, top=3, debug=False):
        '''
        This function, will output the top results from the Webscraping Search
        :param dataframe: this value, represents the dataframe with the magnet values
        :type dataframe: DataFrame
        :param top: this value, represents the number of top magnets from the dataframe
        :type top: int
        :param debug: this value, sets the function in debug mode, printing some additional info about the operations
        :type debug: bool
        :return: this function, returns a DataFrame with the top values
        :rtype: DataFrame
        '''
        try:
            tmp_dataframe = dataframe
            dataframe = self.filter_magnet_dataframe(dataframe)
            dataframe = dataframe.sort_values(by=['seed', 'ratio'], ascending=False)
            result_dataframe = dataframe[:top].reset_index(drop=True)

            if debug:
                print('\n{0} Magnet WebScraping Search:\n {1}\n {2}'.format(self.name, line, tmp_dataframe))
                print('\n {0} \n{1} Magnet Candidates from WebScraping:\n{2}\n{3}'.format(line, self.name, result_dataframe, line))
            return result_dataframe
        except KeyError:
            print('[WARNING]: {0} Unable to Filter Magnet DataFrame: Empty'.format(self.name))
            return tmp_dataframe
    # TODO ---------------------
    # for index in range(0, len(aux_names.index), 1):
    #     name = aux_names.iloc[int(index)]['name']
    #     ini_magnet = ini_dataframe.magnet[ini_dataframe['name'] == name]
    #     tmp_magnet = tmp_dataframe.magnet[tmp_dataframe['name'] == name]
    # TODO ---------------------
    # ini_dataframe['ratio'] = (ini_dataframe['seed'] / ini_dataframe['leech'])
    # tmp_dataframe = self.create_table(torrents[i])
    # tmp_dataframe['ratio'] = (tmp_dataframe['seed'] / tmp_dataframe['leech'])
    #
    # # Create the intersection of the 2 tables so we can retrieve the common entries
    # cmmn_dataframe = pd.merge(ini_dataframe, tmp_dataframe, how='inner', on=['name'])
    #
    # conditions = [cmmn_dataframe['ratio_x'] > cmmn_dataframe['ratio_y'],
    #               cmmn_dataframe['ratio_y'] > cmmn_dataframe['ratio_x'],
    #               cmmn_dataframe['ratio_x'] == cmmn_dataframe['ratio_y']]
    #
    # leech_choices = [cmmn_dataframe['leech_x'], cmmn_dataframe['leech_y'], cmmn_dataframe['leech_x']]
    # seed_choices = [cmmn_dataframe['seed_x'], cmmn_dataframe['seed_y'], cmmn_dataframe['seed_y']]
    # magnet_choices = [cmmn_dataframe['magnet_x'], cmmn_dataframe['magnet_y'], cmmn_dataframe['magnet_y']]
    # size_choices = [cmmn_dataframe['size_x'], cmmn_dataframe['size_y'], cmmn_dataframe['size_y']]
    #
    # # Calculate the winners
    # cmmn_dataframe['size'] = np.select(conditions, size_choices, default=np.nan)

