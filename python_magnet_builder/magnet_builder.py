#!/usr/bin/env python3

# Import System Libraries

# Import External Libraries
#

# Import Custom DataStructures

# Import Custom Exceptions: MagnetBuilder Torrent KeyError

# Import Custom Exceptions: MagnetBuilder Magnet KeyError

# Import Custom Exceptions: MagnetBuilder Torrent NetworkError
from python_magnet_builder.exceptions.magnet_builder_error import MagnetBuilderNetworkAnnounceListKeyError
from python_magnet_builder.exceptions.magnet_builder_error import MagnetBuilderNetworkError

# Import Utils Libraries
from python_magnet_builder.magnet_announce_builder import MagnetAnnounceBuilder
from python_magnet_builder.constants.magnet_announce_type import MagnetAnnounceType
from python_magnet_builder.magnet_reader import MagnetReader

TORRENT_PATH = './cache/temp_torrent.torrent'


class MagnetBuilder(object):
    def __init__(self):
        self.magnet_announce_builder = MagnetAnnounceBuilder()
        self.magnet_reader = MagnetReader()

    def build(self, resource: str):
        return self.process(self.read(resource))

    def read(self, resource: str, size: int = 0, seed: int = 1, leech: int = 1):
        if '.torrent' == resource[len(resource) - 8:]:
            return self.magnet_reader.read_byte_from_file(resource)
        return self.magnet_reader.read_from_magnet(resource, size, seed, leech)

    def process(self, magnet_instance, announce_type=MagnetAnnounceType.ALL):
        original_magnet_instance = magnet_instance
        try:
            announce_list = self.magnet_announce_builder.get_announce_list_from_endpoint(announce_type)
            magnet_instance = self.magnet_announce_builder.clean(magnet_instance)
            magnet_instance.add_announce_list(announce_list)

        except MagnetBuilderNetworkAnnounceListKeyError or MagnetBuilderNetworkError:
            return original_magnet_instance
        return magnet_instance

    def process_torrent_from_response(self, torrent_response, torrent_size, torrent_seed, torrent_leech):
        with open(TORRENT_PATH, 'wb', encoding=torrent_response.encoding) as torrent_file:
            torrent_file.write(torrent_response.content)
        return self.read(TORRENT_PATH, torrent_size, torrent_seed, torrent_leech)
