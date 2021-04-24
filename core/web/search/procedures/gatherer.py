#!/usr/bin/env python3

from core.web.search.procedures.custom_states.context_state import Context
from core.web.search.procedures.custom_states.task_states import TaskInitialized
from core.web.search.procedures.constants.web_scrap_procedure import WebScrapProcedure


# Import Custom Exceptions: WebScraper Exceptions

# Import Custom Exceptions: MagnetBuilder Torrent KeyError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderTorrentKeyHashError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderTorrentKeyDisplayNameError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderTorrentAnnounceListKeyError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderTorrentAnnounceKeyError

# # Import Custom Exceptions: MagnetBuilder Magnet KeyError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderMagnetKeyDisplayNameError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderMagnetKeyAnnounceListError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderMagnetKeyHashError

# # Import Custom Exceptions: MagnetBuilder Torrent NetworkError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderNetworkAnnounceListKeyError
# from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderNetworkError

# Import Custom Exceptions: ScraperEngine
# from torrentscraper.exceptions.scraper_engine_error import ScraperEngineNetworkError


# Import Custom Utils
from python_magnet_builder.magnet_builder import MagnetBuilder


class Gatherer:
    def __init__(self, search_engine, mode: WebScrapProcedure):
        self.mode = mode
        self.search_engine = search_engine
        self.magnet_builder = MagnetBuilder()

    def torrent_file(self, resource_index, resource_link, raw_data):
        task_status = Context(TaskInitialized(), f'Gather TorrentFile {resource_link}')
        task_status.advance()
        try:
            task_status.advance()
            response = self.search_engine.browser_request(resource_link)
            torrent_link = self.search_engine.search_session.web_scraper.get_magnet_link(response)
            torrent_response = self.search_engine.request_file(torrent_link)
            task_status.advance()
            _, size, seed, leech = raw_data.get_row_data(resource_index)
            return self.magnet_builder.process_torrent_from_response(torrent_response, size, seed, leech)
        except Exception as error:
            print(error)
            pass

    def torrent_link(self, resource_index, resource_link, raw_data):
        task_status = Context(TaskInitialized(), f'Gather TorrentFile {resource_link}')
        task_status.advance()
        try:
            task_status.advance()
            response = self.search_engine.browser_request(resource_link)
            magnet = self.search_engine.search_session.web_scraper.get_magnet_link(response)
            task_status.advance()
            _, size, seed, leech = raw_data.get_row_data(resource_index)
            return self.magnet_builder.read(magnet, size, seed, leech)
        except Exception as error:
            print(error)
            pass

    def magnet_link(self, resource_index, resource_link, raw_data):
        task_status = Context(TaskInitialized(), f'Gather TorrentFile {resource_link}')
        task_status.advance()
        try:
            task_status.advance()
            magnet, size, seed, leech = raw_data.get_row_data(resource_index)
            task_status.advance()
            return self.magnet_builder.read(magnet, size, seed, leech)
        except Exception as error:
            print(f'MagnetLink Procedure: {error}')

    def execute(self, resource_index, resource_link, raw_data):
        return self.mode.execute(self, resource_index, resource_link, raw_data)
