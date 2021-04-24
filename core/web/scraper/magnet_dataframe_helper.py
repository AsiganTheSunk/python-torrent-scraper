#!/usr/bin/env python3

# Import System Libraries
import traceback

# Import External Libraries
# import cfscrape
from pandas import DataFrame

# Import Custom Data Structure
from core.web.scraper.data_struct.p2p_instance import P2PInstance

# Import Custom Exceptions: ScraperEngine
from core.exceptions.scraper_engine_error import ScraperEngineUnknownError

# Import Custom Utils
# from core.scraper_engine.web_scraper.utils.magnet_builder import MagnetBuilder
from python_magnet_builder.magnet_builder import MagnetBuilder
from logger.logger_master import tracker_scraper_logger


class MagnetDataFrameHelper:
    def process_p2p_instance_list(self, p2p_instance_list: list[P2PInstance], top: int = 10) -> DataFrame:
        magnet_dataframe = self.create_magnet_dataframe_from_p2p_instance(p2p_instance_list)
        tracker_scraper_logger.logger.info(f'{self.__class__.__name__} UnFiltered MagnetDataframe:')
        tracker_scraper_logger.logger.info(f'\n{magnet_dataframe}')
        magnet_dataframe = self.unique_magnet_dataframe(magnet_dataframe)
        return self.get_magnet_dataframe(magnet_dataframe, top)

    @staticmethod
    def sort_magnet_dataframe_by_seed_and_ratio(magnet_dataframe: DataFrame, magnet_number_limit: int) -> DataFrame:
        magnet_dataframe = magnet_dataframe.sort_values(by=['seed', 'ratio'], ascending=False)
        return magnet_dataframe[:magnet_number_limit].reset_index(drop=True)

    def get_magnet_dataframe(self, magnet_dataframe, magnet_number_limit: int = 10) -> DataFrame:
        """
        This function, will output the top results from the WebScraping Search
        :param magnet_dataframe: this value, represents the dataframe with the magnet values
        :type magnet_dataframe: DataFrame
        :param magnet_number_limit: this value, represents the number of top magnets from the dataframe
        :type magnet_number_limit: int
        :return: this function, returns a DataFrame with the top values
        :rtype: DataFrame
        """
        original_dataframe = magnet_dataframe
        try:
            # magnet_dataframe = self.filter_magnet_dataframe(magnet_dataframe)
            return self.sort_magnet_dataframe_by_seed_and_ratio(magnet_dataframe, magnet_number_limit)
        except KeyError:
            tracker_scraper_logger.logger.warning(f'{self.__class__.__name__}: Unable to Filter Magnet DataFrame: Empty')
            return original_dataframe
        except Exception as err:
            err_msg = ScraperEngineUnknownError(self.__class__, err, traceback.format_exc())
            tracker_scraper_logger.logger.fatal(f'{self.__class__.__name__}: FatalError')
            return original_dataframe

    @staticmethod
    def filter_magnet_ratio(magnet_dataframe, magnet_ratio_limit):
        return magnet_dataframe[magnet_dataframe['ratio'] >= magnet_ratio_limit]

    @staticmethod
    def filter_size_limit(magnet_dataframe, magnet_lower_size_limit, magnet_upper_size_limit):
        magnet_dataframe = magnet_dataframe[magnet_dataframe['size'] >= magnet_lower_size_limit]
        magnet_dataframe = magnet_dataframe[magnet_dataframe['size'] <= magnet_upper_size_limit]
        return magnet_dataframe

    def filter_magnet_dataframe(self, magnet_dataframe: DataFrame,
                                magnet_lower_size_limit=1, magnet_upper_size_limit=1, magnet_ratio_limit=1):
        """
        This function, filters the size and ratio values in a dataframe
        :param magnet_lower_size_limit: this value, represents the lower size limit of a multimedia file
        :type magnet_lower_size_limit: int
        :param magnet_upper_size_limit: this value, represents the upper size limit of a multimedia file
        :type magnet_upper_size_limit: int
        :param magnet_ratio_limit:  this value, represents the ratio limit of a multimedia file
        :type magnet_ratio_limit: int
        :param magnet_dataframe: this value, represents the dataframe with the magnet values
        :type magnet_dataframe: DataFrame
        :return: this function, returns a DataFrame with filtered values
        :rtype: DataFrame
        """
        original_magnet_dataframe = magnet_dataframe
        try:
            magnet_dataframe = self.filter_magnet_ratio(magnet_dataframe, magnet_ratio_limit)
            magnet_dataframe = self.filter_size_limit(magnet_dataframe, magnet_lower_size_limit, magnet_upper_size_limit)
            return magnet_dataframe.reset_index(drop=True)
        except KeyError:
            # self.logger.warning('{0} Unable to Filter Magnet DataFrame: Empty'.format(self.name))
            return original_magnet_dataframe
        except Exception as err:
            err_msg = ScraperEngineUnknownError(self.__class__.__name__, err, traceback.format_exc())
            # self.logger.error(err_msg.message)
            return original_magnet_dataframe

    @staticmethod
    def iloc_magnet_dataframe_from_index(hash_index, magnet_dataframe):
        dn = magnet_dataframe.iloc[int(hash_index)]['name']
        _hash = magnet_dataframe.iloc[int(hash_index)]['hash']
        magnet = magnet_dataframe.iloc[int(hash_index)]['magnet']
        size = magnet_dataframe.iloc[int(hash_index)]['size']
        seed = magnet_dataframe.iloc[int(hash_index)]['seed']
        leech = magnet_dataframe.iloc[int(hash_index)]['leech']
        return dn, _hash, magnet, size, seed, leech

    @staticmethod
    def remove_hashes_from_magnet_dataframe(magnet_dataframe, hash_list):
        for magnet_hash in hash_list:
            magnet_dataframe = magnet_dataframe[magnet_dataframe['hash'] != magnet_hash]
        return magnet_dataframe

    def unique_magnet_dataframe(self, magnet_dataframe):
        """
        This function returns unique hash values from a list of p2p instances
        :param magnet_dataframe: this value, represents the dataframe of p2p instances
        :type magnet_dataframe: DataFrame
        :return: this function, returns a DataFrame with unique hash values
        :rtype: DataFrame
        """
        magnet_builder = MagnetBuilder()
        processed_hash_list = []
        unique_magnet_dataframe = DataFrame()
        original_magnet_dataframe = magnet_dataframe
        magnet_dataframe_group_by_hash = magnet_dataframe.groupby(['hash'])

        try:
            for magnet_hash in magnet_dataframe_group_by_hash.groups:
                if len(magnet_dataframe_group_by_hash.get_group(magnet_hash)) > 1:
                    tracker_scraper_logger.logger.info(
                        f'{self.__class__.__name__}: Found Hash {magnet_hash}'
                        f'with {len(magnet_dataframe_group_by_hash.get_group(magnet_hash).index.tolist())} '
                        f'Repeated Values')
                    processed_hash_list.append(magnet_hash)

                    hash_index = magnet_dataframe_group_by_hash.get_group(magnet_hash).index.tolist()[0]
                    dn, _hash, magnet, size, seed, leech = \
                        self.iloc_magnet_dataframe_from_index(hash_index, magnet_dataframe)
                    magnet_instance = magnet_builder.read(magnet, size, seed, leech)

                    for _hash_index in magnet_dataframe_group_by_hash.get_group(magnet_hash).index.tolist()[1:]:

                        tmp_dn, tmp_hash, tmp_magnet, tmp_size, tmp_seed, tmp_leech = \
                            self.iloc_magnet_dataframe_from_index(_hash_index, magnet_dataframe)
                        tmp_magnet_instance = magnet_builder.read(tmp_magnet, tmp_size, tmp_seed, tmp_leech)
                        magnet_instance = \
                            magnet_builder.magnet_announce_builder.merge(magnet_instance, tmp_magnet_instance)

                    # Add DataFrame Row to unique_magnet_dataframe
                    unique_magnet_dataframe = self.add_magnet_dataframe_row(unique_magnet_dataframe, magnet_instance)

            tracker_scraper_logger.logger.info(f'{self.__class__.__name__}: '
                                               f'Unique Magnets DataFrame Len: {len(unique_magnet_dataframe)}')
            tracker_scraper_logger.logger.info(f'{self.__class__.__name__}: '
                                               f'Processed Hash Number: {len(processed_hash_list)}')
            # Remove _hash from magnet_dataframe
            magnet_dataframe = self.remove_hashes_from_magnet_dataframe(magnet_dataframe, processed_hash_list)

            tracker_scraper_logger.logger.info(f'{self.__class__.__name__}: '
                                               f'Final DataFrame Len: {len(magnet_dataframe)}')
            # Add unique_dataframe_row and return
            return magnet_dataframe.append(unique_magnet_dataframe, ignore_index=True)

        except KeyError:
            tracker_scraper_logger.logger.error(f'{self.__class__.__name__}: '
                                                f'Unable to Create a Unique Magnet DataFrame: Empty')
            return original_magnet_dataframe
        except Exception as error:
            err_msg = ScraperEngineUnknownError(self.__class__.__name__, error, traceback.format_exc())
            tracker_scraper_logger.logger.error(f'{self.__class__.__name__}: {error}')
            return original_magnet_dataframe

    @staticmethod
    def magnet_instance_dataframe_row(magnet_instance):
        return {
            'name': [magnet_instance['display_name']],
            'hash': [magnet_instance['hash']],
            'size': [magnet_instance['size']],
            'seed': [magnet_instance['seed']],
            'leech': [magnet_instance['leech']],
            'ratio': [magnet_instance['ratio']],
            'magnet': [magnet_instance['magnet']]
        }

    def add_magnet_dataframe_row(self, magnet_dataframe, magnet_instance):
        new_magnet_dataframe_row = DataFrame(self.magnet_instance_dataframe_row(magnet_instance),
                                             columns=['name', 'hash', 'size', 'seed', 'leech', 'ratio', 'magnet'])

        return magnet_dataframe.append(new_magnet_dataframe_row, ignore_index=True)

    def create_magnet_dataframe_from_p2p_instance(self, p2p_instance_list):
        """
        This function, creates a transforms p2p instance list into a dataframe
        :param p2p_instance_list: this values, respresents a list of p2p instances
        :type p2p_instance_list: list
        :return: this function, returns a dataframe object with the magnet values
        :rtype: DataFrame
        """

        magnet_dataframe = DataFrame()
        try:
            for p2p_instance in p2p_instance_list:
                for magnet_instance in p2p_instance.magnet_instance_list:
                    magnet_dataframe = self.add_magnet_dataframe_row(magnet_dataframe, magnet_instance)

                # Todo: Apply Filters
                # magnet_dataframe2 = self.filter_magnet_dataframe(magnet_dataframe,
                #                                                  p2p_instance.lower_size_limit,
                #                                                  p2p_instance.upper_size_limit,
                #                                                  p2p_instance.ratio_limit)

        except Exception as error:
            err_msg = ScraperEngineUnknownError(self.__class__.__name__, error, traceback.format_exc())
            tracker_scraper_logger.logger.error(f'{self.__class__.__name__}: {error}')

        return magnet_dataframe
