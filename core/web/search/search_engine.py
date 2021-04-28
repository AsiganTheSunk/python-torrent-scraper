#!/usr/bin/env python3

# Import System Libraries

# Import External Libraries

# import cfscrape
# Import Custom Data Structure

# Import Custom Logger

# Import Custom WebScraper
# from core.scraper_engine.web_scraper import kat_scraper as kata, nyaa_scraper as nyaa
# from core.scraper_engine.web_scraper import pirate_bay_scraper as tpb, torrent_funk_scraper as funk

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

# Import Custom Utils

# Import Custom Exceptions: WebScraper Exceptions
from core.web.scraper.exceptions.webscraper_error import (
    WebScraperContentError, WebScraperParseError, WebScraperProxyListError
)

from core.web.search.procedures.brower_driver import BrowserDriver
from core.web.search.procedures.gatherer import Gatherer
from functools import partial
import concurrent.futures
import requests
from logger.logger_master import tracker_scraper_logger


class SearchEngine:
    def __init__(self, search_session):
        self.search_session = search_session

    def gather(self, resource_link=None):
        try:
            response = self.browser_request(resource_link)
            raw_data = self.search_session.web_scraper.get_raw_data(response)
            return raw_data
        except WebScraperContentError as error:
            tracker_scraper_logger.logger.fatal(f'{self.__class__.__name__} gather: {error.message}')

        except WebScraperParseError as error:
            tracker_scraper_logger.logger.fatal(f'{self.__class__.__name__} gather: {error.message}')

        except WebScraperProxyListError as error:
            # Todo make it so it can be processes and ignored in the upper functions
            raise WebScraperProxyListError(error.name, error.message, error.trace)

    def browser_request(self, resource_link=None):
        """
        :param resource_link:
        :return:
        """
        response = None
        while response is None:
            try:
                browser_driver = BrowserDriver()
                response = browser_driver.get(self.search_session.endpoint(resource_link))
            except WebScraperContentError:
                self.search_session.increase_counter()

            except WebScraperProxyListError as error:
                # Todo make it so it can be processes and ignored in the upper functions
                raise WebScraperProxyListError(error.name, error.message, error.trace)
        return response

    def request_file(self, resource_link):
        cookie, headers = self.search_session.compose_cookie_and_headers()
        # print(self.search_session.endpoint(resource_link))
        response = requests.get(self.search_session.endpoint(resource_link), verify=True, headers=headers, cookies=cookie)
        return response

    def normalize(self, raw_data):
        magnet_instance_list = []
        try:
            futures = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for resource_index, resource_link in enumerate(raw_data.resource_link_list):
                    composed_procedure = partial(
                        Gatherer(self, self.search_session.web_scraper.procedure).execute,
                        resource_index=resource_index, resource_link=resource_link, raw_data=raw_data)
                    futures.append(executor.submit(composed_procedure))

                for future in concurrent.futures.as_completed(futures):
                    magnet_instance_list.append(future.result())

                return magnet_instance_list
        except Exception as error:
            tracker_scraper_logger.logger.warning(f'{self.__class__.__name__}: {error}')
