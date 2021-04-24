#!/usr/bin/env python3

# Import External Libraries
from NyaaPy.utils import Utils
from bs4 import BeautifulSoup

# Import System Libraries
import traceback

# Import Custom Data Structure
from datastruct.rawdata_instance import RAWDataInstance

# Import Custom Exceptions
from web.scraper.scraper_engine import WebScraperParseError
from web.scraper.scraper_engine import WebScraperContentError

from web.scraper.scraper_engine import ScraperInstance

# Constants
from lib.fileflags import FileFlags as fflags


class NyaaScraper(ScraperInstance):
    def __init__(self, logger):
        self.name = self.__class__.__name__
        super().__init__(logger, ['http://nyaa.si'], [fflags.FILM_DIRECTORY_FLAG, fflags.SHOW_DIRECTORY_FLAG])

        self.cloudflare_cookie = False
        self.query_type = True
        self.disable_quality = False
        self.thread_defense_bypass_cookie = False
        self.torrent_file = False
        self.magnet_link = True

        self.default_search = '/'
        self.default_tail = ''
        self.default_params = {'f': '0', 'c:': '0_0', 'p': '0'}
        self.supported_searchs = [fflags.ANIME_DIRECTORY_FLAG]

    def get_raw_data(self, content: str = None) -> RAWDataInstance:
        raw_data = RAWDataInstance(self.name)
        soup = BeautifulSoup(content, 'html.parser')
        if content is not None:
            try:
                ttable = soup.select('table tr')
                if ttable:
                    dict_result = Utils.parse_nyaa(ttable, limit=None)

                    for item in dict_result:
                        # Peer Data
                        seed = self.validate_peer_value(item['seeders'])
                        leech = self.validate_peer_value(item['leechers'])

                        # Size
                        size = self.validate_size_value(item['size'])

                        # Magnet
                        magnet_link = item['magnet']

                        raw_data.add_new_row(seed, leech, size, magnet_link)
                        self.logger.debug('{0} New Entry Raw Values: {1:7} {2:>4}/{3:4} {4}'.format(
                            self.name, str(size), str(seed), str(leech), magnet_link))
                else:
                    raise WebScraperContentError(self.name, 'ContentError: unable to retrieve values', traceback.format_exc())
            except WebScraperContentError as err:
                raise WebScraperContentError(err.name, err.err, err.trace)
            except Exception as e:
                raise WebScraperParseError(self.name, 'ParseError: unable to retrieve values', traceback.format_exc())
            return raw_data
