#!/usr/bin/env python3

# Import System Libraries
from time import sleep
from random import randint
from logging import DEBUG, INFO, WARNING
import logging
import traceback

# Import External Libraries
import requests
import cfscrape
import pandas as pd
from pandas import DataFrame
from fake_useragent import UserAgent

# Import Custom Data Structure
from torrentscraper.datastruct.p2p_instance import P2PInstance

# Import Custom Logger
from torrentscraper.utils.custom_logger import CustomLogger

# Import Custom WebScraper
from torrentscraper.webscrapers import kat_scraper_type_a as kata
from torrentscraper.webscrapers import pirate_bay_scraper as tpb
from torrentscraper.webscrapers import torrent_funk_scraper as funk
from torrentscraper.webscrapers import nyaa_scraper as nyaa
from torrentscraper.webscrapers import mejortorrent_scraper as mjrt

# Import Custom Exceptions: WebScraper Exceptions
from torrentscraper.webscrapers.exceptions.webscraper_error import WebScraperProxyListError
from torrentscraper.webscrapers.exceptions.webscraper_error import WebScraperContentError
from torrentscraper.webscrapers.exceptions.webscraper_error import WebScraperParseError

# # Import Custom Exceptions: MagnetBuilder Torrent KeyError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderTorrentKeyHashError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderTorrentKeyDisplayNameError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderTorrentAnnounceListKeyError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderTorrentAnnounceKeyError
#
# # Import Custom Exceptions: MagnetBuilder Magnet KeyError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderMagnetKeyDisplayNameError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderMagnetKeyAnnounceListError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderMagnetKeyHashError
#
# # Import Custom Exceptions: MagnetBuilder Torrent NetworkError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderNetworkAnnounceListKeyError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderNetworkError


# Import Custom Exceptions: ScraperEngine
# from torrentscraper.exceptions.scraper_engine_error import ScraperEngineNetworkError
from torrentscraper.exceptions.scraper_engine_error import ScraperEngineUnknowError
from torrentscraper.exceptions.scraper_engine_error import ScraperEngineCookieError


# Import Custom Utils
from torrentscraper.webscrapers.utils.uri_builder import UriBuilder
from torrentscraper.webscrapers.utils.magnet_builder import MagnetBuilder
from lib.fileflags import FileFlags as fflags

# Pandas Terminal Configuration
pd.set_option('display.max_rows', 750)
pd.set_option('display.max_columns',750)
pd.set_option('display.width', 1400)

# Constants
line = '-----------------------' * 8
FILM_FLAG = fflags.FILM_DIRECTORY_FLAG
SHOW_FLAG = fflags.SHOW_DIRECTORY_FLAG
ANIME_FLAG = fflags.ANIME_DIRECTORY_FLAG
DEBUG0 = 15
VERBOSE = 5

TORRENT_EXTENSION = '.torrent'
MAGNET_EXTENSION = 'magnet:'

# TODO Terminar de Prograpagar Excepciones!!!
# TODO Hacer los examples para las mismas
# TODO Resolver problema de webdrivers. rbg.RarbgScrapper()
class ScraperEngine(object):
    def __init__(self, webscraper_dict=None):
        self.name = self.__class__.__name__
        self.cache_path = './cache/temp_torrent.torrent'
        # Create & Config CustomLogger
        self.logger = CustomLogger(name=__name__, level=DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s -  [%(levelname)s]: %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')
        file_handler = logging.FileHandler('log/scraper_engine.log', 'w')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level=DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(DEBUG)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        if webscraper_dict is not None:
            self.webscrapers = self.load_webscraper(webscraper_dict)
        else:
            self.webscrapers = [mjrt.MejorTorrentScraper(self.logger)]
            # tpb.PirateBayScraper(self.logger), kata.KatScrapperTypeA(self.logger), kata.KatScrapperTypeA(self.logger), nyaa.NyaaScraper(self.logger), funk.TorrentFunkScraper(self.logger)


    def load_webscraper(self, webscraper_dict):
        aux_list = []
        for item in webscraper_dict:
            if item == 'thepiratebay' and webscraper_dict[item] == '1':
                aux_list.append(tpb.PirateBayScraper(self.logger))
            elif item == 'kickass'  and webscraper_dict[item] == '1':
                aux_list.append(kata.KatScrapperTypeA(self.logger))
            elif item == 'torrentfunk' and webscraper_dict[item] == '1':
                aux_list.append(funk.TorrentFunkScraper(self.logger))
            elif item == 'nyaa' and webscraper_dict[item] == '1':
                aux_list.append(nyaa.NyaaScraper(self.logger))
            elif item == 'mejortorrent' and webscraper_dict[item] == '1':
                aux_list.append(mjrt.MejorTorrentScraper(self.logger))
        return aux_list

    def _normalize_magnet_entries(self, raw_data, websearch, webscraper):
        '''
        This function, will retrieve the missing magnet on a parsed source, if it's unable to retrieve a conventional
        magnet
        :param raw_data: this value, represents a raw values
        :type raw_data: RawDataInstance
        :param webscraper: this value, represents the webscraper class being used
        :type webscraper WebScraper
        :return: this function, returns the *.torrent file or missing magnet associated
        :rtype: *.torrent or magnet
        '''
        magnet_instance_list = []
        source_link = ''
        self.logger.info('{0} Retrieving Info Source from Proxy [ {1} ]'.format(webscraper.name, webscraper.main_page))
        for index in range(0, len(raw_data.magnet_list), 1):
            try:
                source_link = self.resolve_hops(websearch, webscraper, raw_data.magnet_list[index])
                magnet_instance_list = self.add_magnet_instance_entry(
                    websearch, webscraper, magnet_instance_list, source_link,
                    raw_data.size_list[index], raw_data.seed_list[index], raw_data.leech_list[index])
            except Exception as err:
                self.logger.error('{0} Unable to Retrieve Info Source [{1}]\n Error: {2}'.format(webscraper.name, source_link, str(err)))
        return magnet_instance_list

    def add_magnet_instance_entry(self, websearch, webscraper, magnet_instance_list, source_link, size, seed, leech):
        mbuilder = MagnetBuilder(self.logger)
        if MAGNET_EXTENSION in source_link:
            self.logger.info('{0} {1} Detected:\n {2}'.format(self.name, 'magnet', source_link))
            magnet_instance_list.append(mbuilder.parse_from_magnet(source_link, size, seed, leech))

        else:
            torrent_file = self.dynamic_search(websearch, webscraper, source_link)
            self.logger.info('{0} {1} Detected:\n {2}'.format(self.name, 'torrent', source_link))
            self.write_cache(torrent_file)
            magnet_instance_list.append(mbuilder.parse_from_file(self.cache_path, size=size, seed=seed, leech=leech))

        return magnet_instance_list

    def resolve_hops(self, websearch, webscraper, nextHop, hopCount=0):
        if len(webscraper.hops) -1 >= hopCount:
            print('HOPPPPPPPPINGGGGGGGGG', hopCount)
            response = self.dynamic_search(websearch, webscraper, nextHop)
            nextHop = webscraper.hops[hopCount](response.text, websearch)
            return self.resolve_hops(websearch, webscraper, nextHop, hopCount + 1)
        else:
            print('LAST HOP', nextHop)
            return nextHop

    def clean_cache(self):
        pass

    def write_cache(self, torrent_info):
        try:
            with open(self.cache_path, 'wb', encoding=torrent_info.encoding) as file:
                file.write(torrent_info.content)
        except Exception as err:
            try:
                with open(self.cache_path, 'wb') as file:
                    file.write(torrent_info.content)
            except Exception as err:
                self.logger.error('Unable to write torrent in cache', err)

    def search(self, websearch):
        '''
        This functions, will run a search process, retrieving info from internet sources
        :param websearch: this value, represents the title of multimedia file
        :type websearch: WebSearchInstance
        :return: this function returns, a list with a bunch of TorrentInstances
        :rtype: list
        '''
        p2p_instance_list = []
        for webscraper in self.webscrapers:
            raw_data = None
            magnet_instance_list = []

            if websearch['search_type'] in webscraper.supported_searchs:
                self.logger.info('{0} Selected Proxy from Proxy List [ {1} ]'.format(webscraper.name, webscraper.main_page))
                try:
                    raw_data = self._gather_raw_data(websearch, webscraper)
                    magnet_instance_list = self._normalize_magnet_entries(raw_data, websearch, webscraper)  # Normalize Entries
                    p2p_instance_list.append(P2PInstance(webscraper.name, websearch['search_type'],
                                                         websearch['lower_size_limit'], websearch['upper_size_limit'],
                                                         websearch['ratio_limit'], magnet_instance_list))

                # Avoid Crash Went there it's no cotent or parse error message, so the systems it's able to construct
                # the DataFrame.
                except WebScraperContentError as err:
                    self.logger.error(err.message)
                    pass
                except WebScraperParseError as err:
                    self.logger.error(err.message)
                    pass
        return p2p_instance_list

    def _gather_raw_data(self, websearch, webscraper):
        '''

        :param websearch:
        :param webscraper:
        :return:
        '''
        raw_data = None
        response = self.dynamic_search(websearch, webscraper)
        sleep(randint(1, 2))  # Random Sleep to Avoid Flooding
        if response is not None:
            try:
                raw_data = webscraper.get_raw_data(response.text)  # Retrieving RawData from Source
                return raw_data
            except WebScraperContentError or WebScraperParseError as err:
                try:
                    response = self._retry_connection(websearch, webscraper, forced=True)
                    raw_data = webscraper.get_raw_data(response.text)  # Retrieving RawData from Source
                    return raw_data
                except WebScraperContentError or WebScraperProxyListError or WebScraperParseError as err:
                    raise WebScraperContentError(err.name, err.err)

    def _setup_uri(self, websearch, webscraper, append_uri=None):
        '''

        :param websearch:
        :param webscraper:
        :param append_uri:
        :return:
        '''
        if append_uri is None:
            uri_builder = UriBuilder(self.logger)
            return uri_builder.build_request_url(websearch, webscraper)
        else:
            return webscraper.proxy_list[webscraper._proxy_list_pos] + append_uri

    def _setup_cookie(self, search_uri, webscraper):
        '''

        :param search_uri:
        :param webscraper:
        :return:
        '''
        cookie = {}
        headers = {'User-Agent':str(UserAgent().random)}
        try:
            if webscraper.cloudflare_cookie:
                # TODO resolver problema de conexion no anonima
                cookie, user_agent = cfscrape.get_tokens(search_uri, headers['User-Agent'])
                self.logger.info('{0} Retrieving Cloudflare Cookie: \n{1}'.format(webscraper.name, cookie))
                return cookie, headers

            elif webscraper.thread_defense_bypass_cookie:
                # TODO resolver problema de conexion no anonima
                response = requests.get(search_uri, verify=True, headers=headers)
                if response.history:
                    self.logger.debug0('{0} Request Was Redirected:'.format(webscraper.name))
                    for resp in response.history:
                        self.logger.debug('{0} Response: [ Status Code: {1} ] from [ {2} ]'.format(
                            webscraper.name, resp.status_code, resp.url))

                    self.logger.debug0('{0} Final Destination [ Status Code: [ {1} ] from [ {2} ]'.format(
                        webscraper.name, response.status_code, response.url))
                    # thread_defense_bypass = ThreatDefenceBypass()
                    # cookie =  thread_defense_bypass(url=response.url)
                return cookie, headers
            else:
                return cookie, headers
        except Exception as err:
            raise ScraperEngineCookieError(webscraper.name, err, traceback.format_exc())

    def dynamic_search (self, websearch, webscraper, append_uri=None, counter=0, max_counter=3):
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
        :return:
        :rtype: Response
        '''
        response = None
        try:
            search_uri = self._setup_uri(websearch, webscraper, append_uri)
            cookie, headers = self._setup_cookie(search_uri, webscraper)

            self.logger.debug0('{0} Searching on Proxy [ {1} ]'.format(webscraper.name, search_uri))
            response = requests.get(search_uri, verify=True, headers=headers, cookies=cookie)
            return response

        except Exception as err:
            self.logger.debug0(err)
            return self._retry_connection(websearch, webscraper, append_uri, counter, max_counter)

    def _retry_connection(self, websearch, webscraper, append_uri=None, counter=0, max_counter=3, forced=False):
        if counter >= max_counter:
            try:

                webscraper.update_main_page()
                sleep(randint(1, 2))
                self.logger.info(
                    '{0} Connection Failed Multiple Times, Trying a New Proxy from Proxy List: [ {1} ]'.format(
                        webscraper.name, webscraper.proxy_list[webscraper._proxy_list_pos]))
                return self.dynamic_search(websearch, webscraper, append_uri, counter)

            except WebScraperProxyListError as err:
                self.logger.error(err.message)
                return None

        elif forced:
            try:
                webscraper.update_main_page()
                sleep(randint(1, 2))
                self.logger.info(
                    '{0} Corrupted Content, Trying a New Proxy from Proxy List: [ {1} ]'.format(
                        webscraper.name, webscraper.proxy_list[webscraper._proxy_list_pos]))
                return self.dynamic_search(websearch, webscraper, append_uri, counter)

            except WebScraperProxyListError as err:
                self.logger.error(err.message)
                return None

        else:
            counter += 1
            sleep(randint(1, 3))
            self.logger.info(
                '{0} [{1:d}/{2:d}] Connection Failed, Retrying in a Few Seconds wiht Proxy: [ {3} ]'.format(
                    webscraper.name, counter, max_counter, webscraper.proxy_list[webscraper._proxy_list_pos]))
            return self.dynamic_search(websearch, webscraper, append_uri, counter)

    def create_magnet_dataframe(self, p2p_instance_list):
        '''
        This function, creates a transforms p2p instance list into a dataframe
        :param p2p_instance_list: this values, respresents a list of p2p instances
        :type p2p_instance_list: list
        :return: this function, returns a dataframe object with the magnet values
        :rtype: DataFrame
        '''
        try:
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
        except Exception as err:
            err_msg = ScraperEngineUnknowError(self.name, err, traceback.format_exc())
            self.logger.error(err_msg.message)
            return DataFrame()

    def unique_magnet_dataframe(self, dataframe):
        '''
        This function returns unique hash values from a list of p2p instances
        :param dataframe: this value, represents the dataframe of p2p instances
        :type dataframe: DataFrame
        :return: this function, returns a DataFrame with unique hash values
        :rtype: DataFrame
        '''
        tmp_dataframe = dataframe
        try:
            mbuilder = MagnetBuilder(self.logger)
            cmmn_hash = dataframe.groupby(['hash'])
            new_dataframe = DataFrame()
            modified_hash = []

            self.logger.info('{0} Creating Unique Magnet DataFrame:'.format(self.name))
            for item_hash in cmmn_hash.groups:
                if len(cmmn_hash.get_group(item_hash)) > 1:
                    modified_hash.append(item_hash)
                    self.logger.debug('{0} GroupHash: {1} GroupLen: {2}'.format(self.name, item_hash, len(cmmn_hash.get_group(item_hash))))
                    aux_index = cmmn_hash.get_group(item_hash).index.tolist()[0]
                    tmp_dn = dataframe.iloc[int(aux_index)]['name']
                    tmp_hash = dataframe.iloc[int(aux_index)]['hash']
                    tmp_magnet = dataframe.iloc[int(aux_index)]['magnet']
                    tmp_size = dataframe.iloc[int(aux_index)]['size']
                    tmp_seed = dataframe.iloc[int(aux_index)]['seed']
                    tmp_leech = dataframe.iloc[int(aux_index)]['leech']
                    self.logger.debug('{0} Magnet Master Values: {1} {2} {3} {4} {5}'.format(self.name, tmp_dn, tmp_hash, tmp_size, tmp_seed, tmp_leech))
                    aux_magnet_instance = mbuilder.parse_from_magnet(tmp_magnet, tmp_size, tmp_seed, tmp_leech)

                    self.logger.debug('{0} Index: {1}'.format(self.name, cmmn_hash.get_group(item_hash).index.tolist(), cmmn_hash.get_group(item_hash)))
                    self.logger.debug('{0} Common DataFrame: {1}\n'.format(self.name, cmmn_hash.get_group(item_hash).index.tolist(), cmmn_hash.get_group(item_hash)))
                    for index in cmmn_hash.get_group(item_hash).index.tolist()[1:]:
                        tmp_dn = dataframe.iloc[int(index)]['name']
                        tmp_hash = dataframe.iloc[int(index)]['hash']
                        tmp_magnet = dataframe.iloc[int(index)]['magnet']
                        tmp_size = dataframe.iloc[int(index)]['size']
                        tmp_seed = dataframe.iloc[int(index)]['seed']
                        tmp_leech = dataframe.iloc[int(index)]['leech']
                        self.logger.debug('{0} Magnet Slave Values: {1} {2} {3} {4} {5}'.format(self.name, tmp_dn, tmp_hash, tmp_size, tmp_seed, tmp_leech))

                        magnet_instance = mbuilder.parse_from_magnet(tmp_magnet, tmp_size, tmp_seed, tmp_leech)
                        aux_magnet_instance = mbuilder.merge_announce_list(aux_magnet_instance, magnet_instance)
                    self.logger.debug('{0} Final Magnet Values: {1} {2} {3} {4} {5}'.format(self.name,
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
                    self.logger.debug('{0} Adding Merged GroupHash to Temp DataFrame: [ {1} ]\n'.format(self.name, item_hash))
                    new_dataframe = new_dataframe.append(new_row_df, ignore_index=True)

            self.logger.debug0('{0} New DataFrame Rows:\n{1}\n{2}\n'.format(self.name, line, new_dataframe))
            for item_hash in modified_hash:
                self.logger.debug('{0} Filtering GroupHash from Main DataFrame with Hash: [ {1} ]'.format(self.name, item_hash))
                dataframe = dataframe[dataframe['hash'] != item_hash]

            self.logger.debug0('{0} Adding Merged New DataFrame to Main DataFrame:'.format(self.name))
            dataframe = dataframe.append(new_dataframe, ignore_index=True)
            return dataframe

        except KeyError:
            self.logger.warning('{0} Unable to Create a Unique Magnet DataFrame: Empty'.format(self.name))
            return tmp_dataframe
        except Exception as err:
            err_msg = ScraperEngineUnknowError(self.name, err, traceback.format_exc())
            self.logger.error(err_msg.message)
            return tmp_dataframe

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
        tmp_dataframe = dataframe
        try:
            # Filtering by Ratio
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
            self.logger.warning('{0} Unable to Filter Magnet DataFrame: Empty'.format(self.name))
            return tmp_dataframe
        except Exception as err:
            err_msg = ScraperEngineUnknowError(self.name, err, traceback.format_exc())
            self.logger.error(err_msg.message)
            return tmp_dataframe

    def get_dataframe(self, dataframe, top=3):
        '''
        This function, will output the top results from the Webscraping Search
        :param dataframe: this value, represents the dataframe with the magnet values
        :type dataframe: DataFrame
        :param top: this value, represents the number of top magnets from the dataframe
        :type top: int
        :return: this function, returns a DataFrame with the top values
        :rtype: DataFrame
        '''
        tmp_dataframe = dataframe
        try:
            dataframe = self.filter_magnet_dataframe(dataframe)
            dataframe = dataframe.sort_values(by=['seed', 'ratio'], ascending=False)
            result_dataframe = dataframe[:top].reset_index(drop=True)

            self.logger.debug0('{0} Magnet WebScraping Search:\n{1}\n{2}\n'.format(self.name, line, tmp_dataframe))
            self.logger.info('{0} Magnet Candidates from WebScraping:\n{1}\n{2}'.format(self.name, line, result_dataframe))
            return result_dataframe
        except KeyError:
            self.logger.warning('{0} Unable to Filter Magnet DataFrame: Empty'.format(self.name))
            return tmp_dataframe
        except Exception as err:
            err_msg = ScraperEngineUnknowError(self.name, err, traceback.format_exc())
            self.logger.error(err_msg.message)
            return tmp_dataframe
