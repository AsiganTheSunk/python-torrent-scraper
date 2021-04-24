#!/usr/bin/env python3

# Import System Libraries
import traceback

# Import External Libraries
from bs4 import BeautifulSoup

# Import Custom Data Structure
from core.web.scraper.data_struct.rawdata_instance import RAWDataInstance

# Import Custom Exceptions
# Import Custom Exceptions
from core.web.scraper.exceptions.webscraper_error import WebScraperParseError
from core.web.scraper.endpoint_scraper.scraper_instance import ScraperInstance
from core.web.search.procedures.constants.web_scrap_procedure import WebScrapProcedure

# Constants
from core.constants.fileflags import FileFlags
from logger.logger_master import tracker_scraper_logger


class KickAssTorrentsScraper(ScraperInstance):
    def __init__(self):
        super().__init__(['https://kickasss.to'], [FileFlags.FILM_DIRECTORY_FLAG, FileFlags.SHOW_DIRECTORY_FLAG])

        self.cloudflare_cookie = False
        self.query_type = False
        self.disable_quality = False
        self.thread_defense_bypass_cookie = False
        self.torrent_file = False
        self.torrent_link = True
        self.magnet_link = False

        self.default_search = '/search/'
        # self.default_tail = '/?sortby=seeders&sort=desc'
        self.default_tail = ''
        self.default_params = {}
        self.procedure = WebScrapProcedure.TORRENT_LINK

    def get_raw_data(self, content=None) -> RAWDataInstance:
        raw_data = RAWDataInstance(self.__class__.__name__)
        if content is not None:
            try:
                soup = BeautifulSoup(content, 'html.parser')
                torrent_table = soup.findAll('table', {'class': 'data frontPageWidget'})[0].findAll('tbody')[0].findAll('tr')[1:]
                # Retrieving Individual Raw Values From Search Result
                if torrent_table:
                    tracker_scraper_logger.logger.info(f'{self.__class__.__name__} Retrieving Raw Values from Search '
                                                       f'Result Response:')
                    for item in torrent_table:
                        size_str = item.findAll('td', {'class': 'nobr center'})[0].text.strip()
                        size = self.validate_size_value(size_str)
                        seed_str = item.findAll('td', {'class': 'green center'})[0].text.strip()
                        seed = self.validate_peer_value(seed_str)

                        leech_str = item.findAll('td', {'class': 'red lasttd center'})[0].text.strip()
                        leech = self.validate_peer_value(leech_str)

                        magnet_link = item.findAll('a', {'class': 'cellMainLink'})[0]['href'].strip()
                        raw_data.add_new_row(seed, leech, size, magnet_link)
                        tracker_scraper_logger.logger.info(f'{self.__class__.__name__} New Entry Raw Values: '
                                                           f'{str(size):7} {str(seed):>4}/{str(leech):4}'
                                                           f' {magnet_link}')
                    return raw_data
                else:
                    raise WebScraperParseError(self.__class__.__name__,
                                               'ParseError: unable to parse values', traceback.format_exc())
            except WebScraperParseError as err:
                raise WebScraperParseError(self.__class__.__name__, err, traceback.format_exc())

    def get_magnet_link(self, content=None) -> str:
        try:
            soup = BeautifulSoup(content, 'html.parser')
            resource_link = soup.findAll('a', {'class': 'kaGiantButton'})[0]['href']
            if resource_link:
                return resource_link
            else:
                raise WebScraperParseError(self.__class__.__name__,
                                           'ParseError: unable to parse values', traceback.format_exc())
        except WebScraperParseError as err:
            raise WebScraperParseError(self.__class__.__name__, err, traceback.format_exc())
