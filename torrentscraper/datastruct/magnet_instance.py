#!/usr/bin/env python

from collections.abc import Mapping
import urllib.parse

class MagnetInstance(Mapping):
    def __init__(self, _hash, display_name, announce_list):
        self.name = self.__class__.__name__
        self.hash = _hash
        self.display_name = display_name
        self.announce_list = self._get_announce_list(announce_list)
        self._storage = {'hash': self.hash,
                 'display_name': self.display_name,
                 'announce_list':{'https':self.announce_list[0],
                                  'http':self.announce_list[1],
                                  'udp':self.announce_list[2]}}

    def __getitem__(self, key):
        if key == 'magnet':
            return self._get_magnet()
        if key == 'stats':
            return self._get_stats()
        return self._storage[key]

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)

    def __repr__(self):
        '''
        This function, overrides the default function method.
        :return: this function, returns every component in the magnet instance
        :rtype: str
        '''
        return

    def set_announce_list(self, announce_list):
        '''
        This function, sets the announce_list to the magnet instance
        :param announce_list:
        :return: -
        :rtype: -
        '''
        self._update_announce_list(self._get_announce_list(announce_list))

    def add_announce_list(self, announce_list):
        '''
        This funtion, updates the announce_list while adding new content
        :param announce_list: this value, represents the new announce_list to add
        :return: this function, returns bool if successful, otherwise exception
        :rtype: bool
        '''
        try:
            self._update_announce_list(
                self._get_announce_list(self.announce_list[0] +
                                        self.announce_list[1] +
                                        self.announce_list[2] +
                                        announce_list))
        except Exception as e:
            print('%s: Unable to Add Announce %s' % (self.name, e))
        return True

    def _get_stats(self):
        '''
        This function, returns each announce_list on a list[ of lists]
        :return: this function, returns a list [ of list ]containing the number of https, http or udp announcers from
        internet resources.
        :rtype: list
        '''
        https = len(self.announce_list[0])
        http = len(self.announce_list[1])
        udp = len(self.announce_list[2])
        print('%s: \n\t- https [ %s ], http [ %s ], udp [ %s ]' % (self.name, https, http, udp))
        return [https, http, udp]

    def _update_announce_list(self, announce_list):
        '''
        This function, helps to prevent the data on the announce_list from being discarted, updating the information
        :param announce_list: this value, represents a announce_list
        :type announce_list: list
        :return: this function, returns a list [of list], with all the announcers sorted
        :rtype: list
        '''
        self.announce_list = announce_list
        self._storage['announce_list'] = announce_list

    def _get_announce_list(self, announce_list):
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

    def _get_magnet(self):
        '''
        This function, returns a magnet_link based on the values that the magnet instance was able to retrieve.
        :return: this function, returns a string, with the magnet_linj
        :rtype: str
        '''
        # [['&tr='+ str(announce) for announce in announce_subtype] for announce_subtype in self.announce_list]
        magnet_uri = ''
        announce_list = ''
        try:
            for announce_subtype in self.announce_list:
                for announce in announce_subtype:
                    announce_list += '&tr=' + announce
            magnet_uri += 'magnet:?xt=urn:btih:' + self.hash + '&dn='\
                          + self.display_name + (urllib.parse.quote(announce_list))
        except Exception as e:
            print('%s: ErrorGeneratingMagnetUri %s' % (self.name, e))
        return magnet_uri
