#!/usr/bin/env python3

# Import System Libraries
from time import sleep
from random import randint

# Import External Libraries
# import cfscrape
from fake_useragent import UserAgent
import trace
# Import Custom Data Structure

# Import Custom Logger

# Import Custom WebScraper
# from core.scraper_engine.web_scraper import kat_scraper as kata, nyaa_scraper as nyaa
# from core.scraper_engine.web_scraper import pirate_bay_scraper as tpb, torrent_funk_scraper as funk

# Import Custom Exceptions: WebScraper Exceptions
from core.web.scraper.exceptions.webscraper_error import WebScraperProxyListError
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
from core.exceptions.scraper_engine_error import ScraperEngineCookieError


# Import Custom Utils
from core.web.uri.uri_builder import UriBuilder


class SearchEngineSession:
    def __init__(self, web_scraper, web_search):
        self.web_scraper = web_scraper
        self.web_search = web_search
        self.counter = 0
        self.max_counter = 3

    def increase_counter(self):
        self.counter += 1

    def reset_counter(self):
        self.counter = 0

    def max_counter_reached(self):
        return self.counter >= self.max_counter

    def compose_uri(self, resource_link=None):
        """

        :param resource_link:
        :return:
        """
        if resource_link is None:
            uri_builder = UriBuilder()
            return uri_builder.build_request_url(self.web_scraper, self.web_search)
        return self.web_scraper.get_proxy_endpoint() + resource_link

    def compose_cookie_and_headers(self):
        """

        # :param search_uri:
        :param web_scraper:
        :return:
        """
        cookie = {}
        headers = {'User-Agent': str(UserAgent().random)}
        try:
            # if web_scraper.cloudflare_cookie:
            #     # TODO resolver problema de conexion no anonima
            #     cookie, user_agent = cfscrape.get_tokens(search_uri, headers['User-Agent'])
            #     self.logger.info('{0} Retrieving Cloudflare Cookie: \n{1}'.format(web_scraper.name, cookie))
            #     return cookie, headers
            #
            # elif web_scraper.thread_defense_bypass_cookie:
            #     # TODO resolver problema de conexion no anonima
            #     response = requests.get(search_uri, verify=True, headers=headers)
            #     if response.history:
            #         self.logger.debug0('{0} Request Was Redirected:'.format(web_scraper.name))
            #         for resp in response.history:
            #             self.logger.debug('{0} Response: [ Status Code: {1} ] from [ {2} ]'.format(
            #                 web_scraper.name, resp.status_code, resp.url))
            #
            #         self.logger.debug0('{0} Final Destination [ Status Code: [ {1} ] from [ {2} ]'.format(
            #             web_scraper.name, response.status_code, response.url))
            #         # thread_defense_bypass = ThreatDefenceBypass()
            #         # cookie =  thread_defense_bypass(url=response.url)
            #     return cookie, headers
            # else:
            return cookie, headers
        except Exception as err:
            raise ScraperEngineCookieError(self.web_scraper.name, err, trace)

    def endpoint(self, resource_link=None):
        if self.max_counter_reached():
            try:
                self.web_scraper.update_proxy_target()
                self.reset_counter()
                return self.compose_uri(resource_link)

            except WebScraperProxyListError as error:
                raise WebScraperProxyListError(error.name, error.message, error.trace)

        # Only Wait when not switching proxy endpoint
        sleep(randint(1, 3))
        # self.increase_counter()
        return self.compose_uri(resource_link)
