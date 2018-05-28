#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Custom Libraries
from lib.tvdbshowextension import TVDbShowExtension
from torrentscraper.scraper_engine import ScraperEngine

# Import Custom DataStruct
from torrentscraper.datastruct.websearch_instance import WebSearchInstance

# Import Custom Constants
from lib.fileflags import FileFlags as fflags


class TorrentScraper():
    def __init__(self, webscraper_dict=None):
        self.name = self.__class__.__name__

        # ScraperEngine Instance
        self.scraper_engine = ScraperEngine(webscraper_dict)

    def scrap(self, websearch, top=20, bath_mode=False):
        '''

        :param websearch:
        :param top:
        :return:
        '''
        p2p_instance_list = []
        try:
            print(websearch, websearch['title'], websearch['season'], websearch['episode'])
            p2p_instance_list = self.scraper_engine.search(websearch)
        except Exception as err:
            print(self.name, err)
        dataframe = self.scraper_engine.create_magnet_dataframe(p2p_instance_list)
        dataframe = self.scraper_engine.unique_magnet_dataframe(dataframe)
        dataframe = self.scraper_engine.get_dataframe(dataframe, top)
        return dataframe

    def scrap_batch(self, websearch):
        '''

        :param websearch:
        :return:
        '''
        episode = ''
        batch_list = []
        p2p_instance_list = []
        if websearch.search_type == fflags.SHOW_DIRECTORY_FLAG:
            try:
                tvdb = TVDbShowExtension()
                print('Generating Batch for title:',websearch['title'], 'season: ', websearch['season'])
                number_episodes = tvdb.get_number_of_season_episodes(websearch['title'], websearch['season'])
                for index in range(0, number_episodes, 1):
                    corrected_value = index + 1
                    if len(str(corrected_value)) == 1:
                        episode = '0'+str(corrected_value)
                    else:
                        episode = str(corrected_value)
                    aux_websearch = WebSearchInstance(title=websearch['title'],
                                                      season=websearch['season'],
                                                      episode=episode,
                                                      quality=websearch['quality'],
                                                      search_type=websearch['search_type'])
                    aux_websearch.validate()
                    print('Adding to the Batch title:', websearch['title'], 'season: ', websearch['season'],'episode: ', episode)
                    batch_list.append(aux_websearch)

                for websearch_item in batch_list:
                    print(websearch_item, websearch_item['title'], websearch_item['season'], websearch_item['episode'])

                    p2p_instance_list.append(self.scrap(websearch_item, top=3))

            except Exception as err:
                print(self.name, err)
            return p2p_instance_list

