#!/usr/bin/env python3

# Import System Libraries
import traceback

# Import External Libraries
from bs4 import BeautifulSoup

# Import Custom Data Structure
from core.web.scraper.data_struct.rawdata_instance import RAWDataInstance
from core.constants.fileflags import FileFlags

# Import Custom Exceptions
from core.web.scraper.exceptions.webscraper_error import WebScraperParseError
from core.web.scraper.endpoint_scraper.scraper_instance import ScraperInstance
from core.web.search.procedures.constants.web_scrap_procedure import WebScrapProcedure
from logger.logger_master import tracker_scraper_logger


class PirateBayScraper(ScraperInstance):
    def __init__(self):
        # super().__init__(logger, ['https://piratebay.dos', 'https://piratebay.uno', 'https://pirateproxy.ltda'],
        super().__init__(['https://piratebay.uno'], [FileFlags.FILM_DIRECTORY_FLAG, FileFlags.SHOW_DIRECTORY_FLAG])

        self.cloudflare_cookie = False
        self.query_type = True
        self.disable_quality = False
        self.thread_defense_bypass_cookie = False
        self.torrent_file = False
        self.torrent_link = False
        self.magnet_link = True

        self.default_search = '/search.php'
        self.default_tail = ''
        self.default_params = {
            'cat': '0'
            # 'page': '0',
            # 'orderby': '99'
        }
        self.procedure = WebScrapProcedure.MAGNET_LINK

    def get_raw_data(self, content=None) -> RAWDataInstance:
        """
        This Function will try to retrieve the raw data from a target proxy, during a search operation
        :param content:
        :return:
        """
        raw_data = RAWDataInstance(self.__class__.__name__)
        if content is not None:
            try:
                # Retrieving individual raw values from the search result
                soup = BeautifulSoup(content, 'html.parser')
                torrent_table = soup.findAll('ol', {'id': 'torrents'})
                if torrent_table:
                    tracker_scraper_logger.logger.info(f'{self.__class__.__name__} Retrieving Raw Values from Search '
                                                       f'Result Response:')
                    for items in torrent_table:
                        lo_body = items.findAll('li', {'class': 'list-entry'})
                        for li in lo_body:
                            # Peer Data
                            seed_str = li.findAll('span', {'class': 'list-item item-seed'})[0].text
                            seed = self.validate_peer_value(seed_str)
                            leech_str = li.findAll('span', {'class': 'list-item item-leech'})[0].text
                            leech = self.validate_peer_value(leech_str)

                            # Size
                            size_str = li.findAll('span', {'class': 'list-item item-size'})[0].text
                            size = self.validate_size_value(size_str)

                            # Magnet Link
                            magnet_link = (li.findAll('span', {'class': 'item-icons'}))[0].find('a')['href']

                            # Add New Row to the raw_data instance
                            raw_data.add_new_row(seed, leech, size, magnet_link)
                            tracker_scraper_logger.logger.info(f'{self.__class__.__name__} New Entry Raw Values: '
                                                               f'{str(size):7} {str(seed):>4}/{str(leech):4} '
                                                               f'{magnet_link}')
                    return raw_data
                else:
                    raise WebScraperParseError(self.__class__.__name__, 'ParseError: unable to parse values',
                                               traceback.format_exc())
            except WebScraperParseError as err:
                raise WebScraperParseError(self.__class__.__name__, err, traceback.format_exc())
