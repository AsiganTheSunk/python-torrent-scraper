#!/usr/bin/env python3

# Import System Libraries
from collections.abc import Mapping
import urllib.parse
from colorama import init, Fore
from typing import Iterator
# Init Colorama: For Windows Systems
from python_magnet_builder.constants.magnet_announce_type import MagnetAnnounceType
init()


class MagnetInstance(Mapping):
    def __init__(self, _hash: str, display_name: str, announce_list: list[list], size: int = 0,
                 seed: int = 1, leech: int = 1):

        self.name: str = self.__class__.__name__
        self.hash: str = _hash
        self.display_name: str = display_name
        self.size = size
        self.seed: int = int(seed)
        self.leech: int = int(leech)
        self.announce_list: list[list] = self.pack_announce_list(announce_list)

        self.activity = {'seed': self.seed, 'leech': self.leech}
        self._storage = {
            'hash': self.hash,
            'display_name': self.display_name,
            'size': self.size,
            'seed': self.seed,
            'leech': self.leech,
            'ratio': self.seed/self.leech,
            'announce_list': {
                'https': self.announce_list[0],
                'http': self.announce_list[1],
                'udp': self.announce_list[2]
            }
        }

    def __getitem__(self, key):
        if key == 'magnet':
            return self.get_magnet_link()
        if key == 'status':
            return self.get_announce_list_count()
        if key == 'activity':
            return self.activity
        return self._storage[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._storage)

    def __len__(self) -> int:
        return len(self._storage)

    @staticmethod
    def announce_str_helper(announce_type: MagnetAnnounceType, announce_list: list[str]) -> str:
        announce_str_list = f'\t{announce_type.value} ({len(announce_list)}): [\n'
        for index, announce in enumerate(announce_list):
            announce_str_list += f'\t\t{announce}\n'
        return announce_str_list[:-1] + f'\n\t]\n'

    def __repr__(self) -> str:
        separator = '========' * 8
        https_announce_str_list = self.announce_str_helper(MagnetAnnounceType.HTTPS, self.announce_list[0])
        http_announce_str_list = self.announce_str_helper(MagnetAnnounceType.HTTP, self.announce_list[1])
        udp_announce_str_list = self.announce_str_helper(MagnetAnnounceType.UDP, self.announce_list[2])

        result = f'{separator}\n' \
                 f'{self.__class__.__name__} object at {hex(id(self))}\n' \
                 f'{separator}\n' \
                 f'Hash: {self.hash}\n' \
                 f'DisplayName: {self.display_name}\n' \
                 f'Size: {self.size}, Seed: {self.seed}, Leech: {self.leech}, Ratio: {self.seed/self.leech}\n' \
                 f'{separator}\n' \
                 f'AnnounceList: [\n' \
                 f'{https_announce_str_list}' \
                 f'{http_announce_str_list}' \
                 f'{udp_announce_str_list}]'
        return result

    def unpack_announce_list(self):
        return self['announce_list']['https'] + self['announce_list']['http'] + self['announce_list']['udp']

    @staticmethod
    def pack_announce_list(announce_list):
        udp_announce_list = []
        http_announce_list = []
        https_announce_list = []
        for item in announce_list:
            if 'udp://' in item:
                udp_announce_list.append(item)
            elif 'http://' in item:
                http_announce_list.append(item)
            elif 'https://' in item:
                https_announce_list.append(item)
        return [https_announce_list, http_announce_list, udp_announce_list]

    def set_announce_list(self, announce_list):
        """
        This function, sets the announce_list to the magnet instance
        :param announce_list:
        :return: None
        """
        self.update_announce_list(self.pack_announce_list(announce_list))

    def add_announce_list(self, announce_list):
        """
        This function, updates the announce_list while adding new content
        :param announce_list: this value, represents the new announce_list to add
        :return: this function, returns bool if successful, otherwise exception
        :rtype: bool
        """
        try:
            self.update_announce_list(
                self.pack_announce_list(self.announce_list[0] +
                                        self.announce_list[1] +
                                        self.announce_list[2] +
                                        announce_list))
        except Exception as err:
            return False
        return True

    def get_announce_list_count(self):
        """
        This function, returns each announce_list on a list[ of lists]
        :return: this function, returns a list [ of list ]containing the number of https, http or udp announcers from
        internet resources.
        :rtype: list
        """
        https = len(self.announce_list[0])
        http = len(self.announce_list[1])
        udp = len(self.announce_list[2])
        print('%s: \n\t- https [ %s ], http [ %s ], udp [ %s ]' % (self.name, https, http, udp))
        return [https, http, udp]

    def update_announce_list(self, announce_list):
        """
        This function, helps to prevent the data on the announce_list from being discarted, updating the information
        :param announce_list: this value, represents a announce_list
        :return: this function, returns a list [of list], with all the announcers sorted
        :rtype: list
        """
        self.announce_list = announce_list
        self._storage['announce_list'] = announce_list

    def get_magnet_link(self):
        """
        This function, returns a magnet_link based on the values that the magnet instance was able to retrieve.
        :return: this function, returns a string, with the magnet_link
        :rtype: str
        """
        # [['&tr='+ str(announce) for announce in announce_subtype] for announce_subtype in self.announce_list]
        magnet_link = ''
        announce_list = ''
        try:
            for announce_subtype in self.announce_list:
                for announce in announce_subtype:
                    announce_list += '&tr=' + urllib.parse.quote(announce)

            magnet_link += f'magnet:?xt=urn:btih:{self.hash}&dn={self.display_name}{announce_list}'
        except Exception as e:
            print('%s: ErrorGeneratingMagnetUri %s' % (self.name, e))
        return magnet_link
