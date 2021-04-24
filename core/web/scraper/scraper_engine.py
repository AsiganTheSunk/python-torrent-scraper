#!/usr/bin/env python3

# Import System Libraries
from logging import DEBUG, INFO
import logging

# Import External Libraries
# import cfscrape
import pandas as pd
# Import Custom Data Structure
from core.web.scraper.data_struct.p2p_instance import P2PInstance

# Import Custom Logger
from logger.custom_logger import CustomLogger

# Import Custom WebScraper
from core.web.scraper.endpoint_scraper.pirate_bay_scraper import PirateBayScraper
from core.web.scraper.endpoint_scraper.torrent_funk_scraper import TorrentFunkScraper
from core.web.scraper.endpoint_scraper.kick_ass_torrent_scraper import KickAssTorrentsScraper
# from core.scraper_engine.web_scraper import kat_scraper as kata, nyaa_scraper as nyaa
# from core.scraper_engine.web_scraper import pirate_bay_scraper as tpb, torrent_funk_scraper as funk

# Import Custom Exceptions: WebScraper Exceptions
from core.web.scraper.exceptions.webscraper_error import (
    WebScraperProxyListError, WebScraperParseError, WebScraperContentError
)


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
from core.web.scraper.magnet_dataframe_helper import MagnetDataFrameHelper
from core.web.search.search_engine import SearchEngine
from core.web.search.search_engine_session import SearchEngineSession
import concurrent.futures
from logger.logger_master import tracker_scraper_logger


# Pandas Terminal Configuration
pd.set_option('display.max_rows', 750)
pd.set_option('display.max_columns', 750)
pd.set_option('display.width', 1400)

# Constants
line = '-----------------------' * 8

DEBUG0 = 15
VERBOSE = 5


class ScraperEngine:
    def __init__(self, web_scraper_dict=None):
        self.name = self.__class__.__name__
        self.magnet_dataframe_helper = MagnetDataFrameHelper()

        if web_scraper_dict is not None:
            self.web_scrapers = self.load_web_scraper(web_scraper_dict)
        else:
            # self.logger.info('Genera Lista con NyaaScraper')
            # self.webscrapers = [nyaa.NyaaScraper(self.logger), tpb.PirateBayScraper(self.logger),
            # funk.TorrentFunkScraper(self.logger), kata.KatScrapper(self.logger)]
            self.web_scrapers = [
                PirateBayScraper(),
                TorrentFunkScraper(),
                # KickAssTorrentsScraper()
            ]
            # self.web_scrapers = [KickAssTorrentsScrapper(self.logger)]

    def load_web_scraper(self, web_scraper_dict=None):
        # aux_list = []
        # for item in web_scraper_dict:
        #     if item == 'thepiratebay' and web_scraper_dict[item] == '1':
        #         aux_list.append(tpb.PirateBayScraper(self.logger))
        #     elif item == 'kickass' and web_scraper_dict[item] == '1':
        #         aux_list.append(kata.KatScrapper(self.logger))
        #     elif item == 'torrentfunk' and web_scraper_dict[item] == '1':
        #         aux_list.append(funk.TorrentFunkScraper(self.logger))
        #     elif item == 'nyaa' and web_scraper_dict[item] == '1':
        #         aux_list.append(nyaa.NyaaScraper(self.logger))
        return [PirateBayScraper()]

    def get_sessions(self, web_search_instance):
        search_engine_sessions = dict()
        for web_scraper in self.web_scrapers:
            search_engine = SearchEngine(SearchEngineSession(web_scraper, web_search_instance))
            search_engine_sessions[web_scraper.__class__.__name__] = search_engine
        return search_engine_sessions

    def get_raw_data(self, web_search_instance, executor, search_engine_sessions):
        web_scraper_futures = dict()

        for web_scraper in self.web_scrapers:
            futures = []
            if web_search_instance['search_type'] in web_scraper.supported_searches:
                tracker_scraper_logger.logger.info(f'{web_scraper.__class__.__name__} '
                                                   f'Selected Proxy from Proxy List [ {web_scraper.main_page} ]')
                try:
                    futures.append(executor.submit(search_engine_sessions[web_scraper.__class__.__name__].gather))

                except WebScraperProxyListError as error:
                    tracker_scraper_logger.logger.error(f'{error}')
                    tracker_scraper_logger.logger.error(f'{web_scraper.__class__.__name__}: '
                                                        f'Moving To Next Scraper, Try Again Later ...')
                except Exception as error:
                    tracker_scraper_logger.logger.fatal(f'get_raw_data: FatalError {error}')

            web_scraper_futures[web_scraper.__class__.__name__] = futures

        return web_scraper_futures

    def get_p2p_instances(self, web_search_instance, web_scraper_futures, search_engine_sessions):
        p2p_instance_list = []
        for web_scraper in web_scraper_futures:
            for future in concurrent.futures.as_completed(web_scraper_futures[web_scraper]):
                try:
                    magnet_instance_list = search_engine_sessions[web_scraper].normalize(future.result())
                    tracker_scraper_logger.logger.info(f'{self.__class__.__name__} Found {len(magnet_instance_list)} '
                                                       f'Results on {web_scraper} selected endpoint')
                    p2p_instance_list.append(P2PInstance(web_scraper, web_search_instance['search_type'],
                                                         web_search_instance['lower_size_limit'],
                                                         web_search_instance['upper_size_limit'],
                                                         web_search_instance['ratio_limit'], magnet_instance_list))
                except WebScraperContentError as error:
                    tracker_scraper_logger.logger.error(error.message)

                except WebScraperParseError as error:
                    tracker_scraper_logger.logger.error(error.message)

                except WebScraperProxyListError as error:
                    tracker_scraper_logger.logger.error(f'{error}')
                    tracker_scraper_logger.logger.error(f'{web_scraper.__class__.__name__}: ' 
                                                        f'Moving To Next Scraper, Try Again Later ...')
                except Exception as error:
                    tracker_scraper_logger.logger.fatal(f'get_raw_data: FatalError {error}')

        return p2p_instance_list

    def search(self, web_search_instance):
        """
        This functions, will run a search process, retrieving the raw_data from a main search page, later normalize
        the recovered entries as magnet_instances wrapped in a p2p_instance.
        :param web_search_instance: this value, represents the title of multimedia file
        :type web_search_instance: WebSearchInstance
        :return: this function returns, a list with a bunch of TorrentInstances
        :rtype: p2p_instance
        """

        sessions = self.get_sessions(web_search_instance)
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.web_scrapers)) as executor:
            try:
                web_scraper_futures = self.get_raw_data(web_search_instance, executor, sessions)
                p2p_instance_list = self.get_p2p_instances(web_search_instance, web_scraper_futures, sessions)
                return p2p_instance_list
            except Exception as error:
                tracker_scraper_logger.info(f'{error}')
                tracker_scraper_logger.info(f'{self.__class__.__name__}: FatalError')
