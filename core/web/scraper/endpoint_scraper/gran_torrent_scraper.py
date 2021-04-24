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
# Constants
from core.constants.fileflags import FileFlags
from logger.logger_master import tracker_scraper_logger


class GranTorrentScraper(ScraperInstance):
    def __init__(self):
        super().__init__(['https://grantorrent.nl'], [FileFlags.FILM_DIRECTORY_FLAG, FileFlags.SHOW_DIRECTORY_FLAG])

        self.cloudflare_cookie = False
        self.query_type = False
        self.disable_quality = False
        self.thread_defense_bypass_cookie = False
        self.torrent_file = True
        self.torrent_link = False
        self.magnet_link = False

        self.default_params = {}
        self.default_search = '?s='
        self.default_tail = ''

        self.procedure = WebScrapProcedure.TORRENT_FILE

    def get_raw_data(self, content=None) -> RAWDataInstance:

        raw_data = RAWDataInstance(self.__class__.__name__)
        if content is not None:
            try:
                soup = BeautifulSoup(content, 'html.parser')
                # Retrieving individual values from the search result
                torrent_table = soup.findAll('div', {'class': 'contenedor-home'})
                if torrent_table:
                    tracker_scraper_logger.logger.info(f'{self.__class__.__name__} Retrieving Raw Values from Search '
                                                       f'Result Response:')
                    for resource_link in torrent_table:
                        torrent_link = resource_link.findAll('div', {'class': 'imagen-post'})[0]
                        torrent_link = torrent_link.findAll('a')[0]['href']
                        print(torrent_link)

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
        soup = BeautifulSoup(content, 'html.parser')
        try:
            content = soup.findAll('table', {'class': 'demo'})
            # link: https://files.grantorrent.eu/torrents/peliculas/rayayelultimodragon.torrent
            if content:
                print(content)
                return 'torrent_file'
            else:
                raise WebScraperParseError(self.__class__.__name__,
                                           'ParseError: unable to parse values', traceback.format_exc())
        except WebScraperParseError as err:
            raise WebScraperParseError(self.__class__.__name__, err, traceback.format_exc())
