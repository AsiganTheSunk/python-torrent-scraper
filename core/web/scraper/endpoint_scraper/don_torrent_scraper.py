#!/usr/bin/env python3

# Import System Libraries
import traceback

# Import External Libraries
from bs4 import BeautifulSoup

# Import Custom Data Structure
from core.web.scraper.data_struct.rawdata_instance import RAWDataInstance

# Import Custom Exceptions
from core.web.scraper.exceptions.webscraper_error import WebScraperParseError
from core.web.scraper.endpoint_scraper.scraper_instance import ScraperInstance
from core.web.search.procedures.constants.web_scrap_procedure import WebScrapProcedure
from logger.logger_master import tracker_scraper_logger
# Constants
from core.constants.fileflags import FileFlags


class DonTorrentScraper(ScraperInstance):
    def __init__(self):
        super().__init__(['https://dontorrent.one'], [FileFlags.FILM_DIRECTORY_FLAG, FileFlags.SHOW_DIRECTORY_FLAG])

        self.cloudflare_cookie = False
        self.query_type = False
        self.disable_quality = False
        self.thread_defense_bypass_cookie = False
        self.torrent_file = True
        self.torrent_link = False
        self.magnet_link = False

        self.default_params = {}
        self.default_search = '/buscar/'
        self.default_tail = ''

        self.procedure = WebScrapProcedure.TORRENT_FILE

    def get_raw_data(self, content=None) -> RAWDataInstance:
        raw_data = RAWDataInstance(self.__class__.__name__)
        if content is not None:
            try:
                soup = BeautifulSoup(content, 'html.parser')
                # Retrieving individual values from the search result
                torrent_table = soup.findAll('div', {'class': 'card-body'})[0]
                if torrent_table:
                    resource_links = torrent_table.findAll('a', {'class': 'text-decoration-none'})
                    tracker_scraper_logger.logger.info(f'{self.__class__.__name__} Retrieving Raw Values from Search '
                                                       f'Result Response:')
                    for item in resource_links:
                        print(item['href'])

                    # # self.logger.info('{0} Retrieving Raw Values from Search Result Response:'.format(self.name))
                    # for items in ttable:
                    #     tbody = items.findAll('tr')[1:]
                    #     for tr in tbody:
                    #         # Size
                    #         size = self.validate_size_value((tr.findAll('td'))[2].text)
                    #
                    #         # Peer Data
                    #         seed = self.validate_peer_value((tr.findAll('td'))[3].text)
                    #         leech = self.validate_peer_value((tr.findAll('td'))[4].text)
                    #
                    #         magnet_link = (tr.findAll('a'))[0]['href']
                    #         raw_data.add_new_row(seed, leech, size, magnet_link)
                    #         self.logger.info(f'{self.name} New Entry Raw Values: '
                    #                          f'{str(size):7} {str(seed):>4}/{str(leech):4} {magnet_link}')
                    return raw_data
                else:
                    raise WebScraperParseError(self.__class__.__name__,
                                               'ParseError: unable to parse values', traceback.format_exc())
            except WebScraperParseError as err:
                raise WebScraperParseError(self.__class__.__name__, err, traceback.format_exc())

    def get_magnet_link(self, content=None) -> str:
        try:
            soup = BeautifulSoup(content, 'html.parser')
            resource_link = soup.findAll('a', {
                'class': 'text-white bg-primary rounded-pill d-block shadow text-decoration-none p-1'
            })[0]['href']

            if resource_link:
                return f'https:{resource_link}'
            else:
                raise WebScraperParseError(self.__class__.__name__,
                                           'ParseError: unable to parse values', traceback.format_exc())
        except WebScraperParseError as err:
            raise WebScraperParseError(self.__class__.__name__, err, traceback.format_exc())
