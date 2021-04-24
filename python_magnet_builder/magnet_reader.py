from typing import Iterable
from bencodepy import decode_from_file

from python_magnet_builder.exceptions.magnet_builder_error import MagnetBuilderTorrentKeyDisplayNameError, \
    MagnetBuilderTorrentAnnounceListKeyError, MagnetBuilderTorrentAnnounceKeyError, \
    MagnetBuilderMagnetKeyDisplayNameError, MagnetBuilderMagnetKeyHashError, \
    MagnetBuilderMagnetKeyAnnounceListError
from python_magnet_builder.magnet_byte_reader import MagnetByteAttributeReader
from python_magnet_builder.data_struct.magnet_instance import MagnetInstance
from python_magnet_builder.magnet_regex_parser import MagnetRegexAttributeParser
from python_magnet_builder.magnet_reader_helper import MagnetReaderHelper
from python_magnet_builder.constants.magnet_base_encode import MagnetBaseEncoding


class MagnetReader:
    def __init__(self):
        self.magnet_regex_attribute_parser = MagnetRegexAttributeParser()
        self.magnet_byte_attribute_reader = MagnetByteAttributeReader()
        self.magnet_reader_helper = MagnetReaderHelper()

    # def read_str_from_file(self, file: str) -> Union[dict, list, int, str, bytes]:
    #     """
    #     This function, will parse the content from a *.torrent file, retrieving all the values
    #     :param file: this value, represents the path to the *.torrent file
    #     :type file: str
    #     :return: this function, returns a dict with all the raw values from the *.torrent file
    #     :rtype: dict
    #     """
    #     data = {}
    #     try:
    #         data = parse_torrent_file(file)
    #     except Exception as err:
    #         print(err)
    #     return data

    def read_byte_from_file(self, file: str, base_encoding: MagnetBaseEncoding = MagnetBaseEncoding.Base16) -> MagnetInstance:
        """
        This function, will parse the content of a *.torrent file, retrieving the fundamental values
        :param file: this value, represents the path to the *.torrent file
        :param base_encoding: this value, represents the base of hash you're gonna use to encode, by default 16
        :return: this function, returns a magnet instance with the fundamental values from the *.torrent file
        :rtype: MagnetInstance
        """

        _hash: str = ''
        announce: str = ''
        display_name: str = ''
        announce_list = None

        try:
            # Decode Byte Metadata from Torrent File
            magnet_byte_metadata: Iterable = decode_from_file(file)

            try:
                # Get the MagnetInstance Hash from Torrent File Byte Metadata
                magnet_byte_info = self.magnet_byte_attribute_reader.read_info(magnet_byte_metadata)
                _hash = self.magnet_reader_helper.generate_hash(magnet_byte_info, base_encoding)
            except Exception as err:
                print(err)
                # self.logger.error(error)

            try:
                # Get the DisplayName from Torrent File Byte Metadata
                display_name = self.magnet_byte_attribute_reader.read_display_name(magnet_byte_metadata)
            except MagnetBuilderTorrentKeyDisplayNameError as error:
                pass
                # self.logger.warning(err.message)

            try:
                # Read Announce from Torrent File
                announce = self.magnet_byte_attribute_reader.read_announce(magnet_byte_metadata)
            except MagnetBuilderTorrentAnnounceKeyError as error:
                pass
                # self.logger.warning(error.message)

            try:
                # Read AnnounceList from Torrent Fire
                announce_list = self.magnet_byte_attribute_reader.read_announce_list(magnet_byte_metadata)
            except MagnetBuilderTorrentAnnounceListKeyError as error:
                pass
                # self.logger.warning(error.message)

            announce_list = (announce_list, announce)[announce_list is []]

            # ch_filter = chinese_filter()
            # display_name = ch_filter.sub('', str(display_name))
            # self.logger.debug0(
            #     '{0} Generated Uri from Torrent File: {1} with Hash [ {2} ]'.format(self.name, display_name, _hash))
            # self.logger.debug('* Announce List {0}'.format(announce_list))
            return MagnetInstance(_hash.lower(), str(display_name), announce_list)
        except Exception as err:
            pass

    def read_from_magnet(self, magnet_link: str, size: int = 0, seed: int = 1, leech: int = 1) -> MagnetInstance:
        """
        This function, will parse the content of any given magnet_link
        :param leech:
        :param seed:
        :param size:
        :param magnet_link: this value, represents a magnet_link
        :type magnet_link: str
        :return: this function, returns a magnet instance based on the magnet values that had been retrieved
        :rtype: MagnetInstance
        """
        try:
            _hash = ''
            display_name = ''
            announce_list = ''

            try:
                display_name = str(self.magnet_regex_attribute_parser.parse_display_name(magnet_link))
            except MagnetBuilderMagnetKeyDisplayNameError as err:
                pass
                # self.logger.error(err.message)

            try:
                _hash = self.magnet_regex_attribute_parser.parse_hash(magnet_link)
            except MagnetBuilderMagnetKeyHashError as err:
                pass
                # self.logger.error(err.message)

            try:
                announce_list = self.magnet_regex_attribute_parser.parse_announce_list(magnet_link)
            except MagnetBuilderMagnetKeyAnnounceListError as err:
                pass
                # self.logger.error(err.message)

            # ch_filter = chinese_filter()
            # display_name = ch_filter.sub('', str(display_name))
            #
            # self.logger.debug0(
            #     '{0} Generated Uri from Magnet Link: {1} with Hash [ {2} ]'.format(self.name, display_name, _hash))
            # self.logger.debug('* Announce List {0}'.format(announce_list))
            return MagnetInstance(_hash.lower(), display_name, announce_list, size, seed, leech)
        except Exception as err:
            pass
            # return MagnetInstance(_hash, )

