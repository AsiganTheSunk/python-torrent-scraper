#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importing Scraper Engine: search()
from core.web.scraper.scraper_engine import ScraperEngine

# Importing MagnetDataFrameHelper: process_p2p_instance_list()
from core.web.scraper.magnet_dataframe_helper import MagnetDataFrameHelper

# Importing LoggerMaster: tracker_scraper_logger
from logger.logger_master import tracker_scraper_logger


class TrackerScraper:
    def __init__(self, web_scraper_dict=None):
        self.name = self.__class__.__name__
        self.scraper_engine = ScraperEngine(web_scraper_dict)
        self.scraper_dataframe_helper = MagnetDataFrameHelper()

    def scrap(self, web_search, top=20, batch_mode=False):
        """
        :param web_search:
        :param top:
        :param batch_mode:
        :return:
        """
        p2p_instance_list = []
        try:
            tracker_scraper_logger.logger.info(f'{self.__class__.__name__}: Starting Scrap ...')
            p2p_instance_list = self.scraper_engine.search(web_search)
        except Exception as err:
            print(self.name, err)

        tracker_scraper_logger.logger.info(f'{self.__class__.__name__}: Processing Results ...')
        magnet_dataframe = self.scraper_dataframe_helper.process_p2p_instance_list(p2p_instance_list)

        # if batch_mode:
        #     batch_dataframe = self.scrap_batch(websearch)
        #     dataframe =  self.scraper_engine.merge_dataframe_list([dataframe, batch_dataframe])
        #
        #
        # surrogated_view = dataframe[dataframe.surrogated_id != '']
        # alias_view = self.scraper_engine.generate_alias_dataframe_row(dataframe, websearch)
        # clean_view = self.scraper_engine.merge_dataframe_list([dataframe[dataframe.surrogated_id == ''], alias_view])

        # print('********'*5, '  Clean View      ', '********'*5,'\n', clean_view)
        # print('********'*5, '  Surrogated View ', '********'*5,'\n', surrogated_view)

        return magnet_dataframe

    # def scrap_batch(self, websearch, top=1):
    #     '''
    #
    #     :param websearch:
    #     :return:
    #     '''
    #     episode = ''
    #     batch_list = []
    #     dataframe_list = []
    #     p2p_instance_list = []
    #     if websearch.search_type == fflags.SHOW_DIRECTORY_FLAG:
    #         try:
    #             tvdb = TVDbShowExtension()
    #             print('Generating Batch for title: ', websearch['title'], 'season: ', websearch['season'])
    #             number_episodes = tvdb.get_number_of_season_episodes(websearch['title'], websearch['season'])
    #
    #             for index in range(0, number_episodes, 1):
    #
    #                 corrected_value = index + 1
    #                 if len(str(corrected_value)) == 1:
    #                     episode = '0'+str(corrected_value)
    #                 else:
    #                     episode = str(corrected_value)
    #
    #                 aux_websearch = WebSearchInstance(title=websearch['title'],
    #                                                   season=websearch['season'],
    #                                                   episode=episode,
    #                                                   quality=websearch['quality'],
    #                                                   search_type=websearch['search_type'],
    #                                                   surrogated_id='Generated Batch')
    #
    #                 aux_websearch.validate()
    #                 batch_list.append(aux_websearch)
    #
    #                 print('Adding to the Batch title0:',  aux_websearch['title'],
    #                       'season: ',  aux_websearch['season'],
    #                       'episode: ',  aux_websearch['episode'],
    #                       'quality: ',  aux_websearch['quality'],
    #                       'search_type: ',  aux_websearch['search_type'],
    #                       'surrogated_id: ',  aux_websearch['surrogated_id'])
    #
    #             for websearch_item in batch_list:
    #                 dataframe = self.scrap(websearch_item, top=top)
    #                 dataframe_list.append(dataframe)
    #
    #         except Exception as err:
    #             print(self.name, err)
    #         return self.scraper_engine.merge_dataframe_list(dataframe_list)
