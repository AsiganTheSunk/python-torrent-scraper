#!/usr/bin/env python

# Import System Libraries
import urllib.parse
import hashlib
import base64
import re

# Import External Libraries
import torrent_parser as tp
import bencodepy
import requests

# Import Custom DataStructures
from torrentscraper.datastruct.magnet_instance import MagnetInstance

# Import Custom Exceptions: MagnetBuilder Torrent KeyError
from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderTorrentKeyHashError
from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderTorrentKeyDisplayNameError
from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderTorrentAnnounceListKeyError
from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderTorrentAnnounceKeyError

# Import Custom Exceptions: MagnetBuilder Magnet KeyError
from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderMagnetKeyDisplayNameError
from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderMagnetKeyAnnounceListError
from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderMagnetKeyHashError


# Import Custom Exceptions: MagnetBuilder Torrent NetworkError
from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderNetworkAnnounceListKeyError
from torrentscraper.webscrapers.exceptions.magnet_builder_error import MagnetBuilderNetworkError

# Import Utils Libraries
from torrentscraper.webscrapers.utils.chinese_filter import chinese_filter

# Constants
HTTPS_ANNOUNCE_LIST = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_https.txt'
HTTP_ANNOUNCE_LIST = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_http.txt'
UDP_ANNOUNCE_LIST = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_udp.txt'
IP_ANNOUNCE_LIST = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_ip.txt'
ALL_ANNOUNCE_LIST = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt'
BLACKLIST_ANNOUNCE_LIST = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/blacklist.txt'


class MagnetBuilder(object):
    def __init__(self, logger):
        self.name = self.__class__.__name__
        self.logger = logger
        #self.logger_lvl = self.logger.getLevelName(self.logger.getEffectiveLevel())

    # def __str__(self):
    #     return('{0} Id: {1}\n Logger Id:{2}, Logger Lvl:{3}\n'.format(
    #         self.name, id(self),
    #         self.logger.getLevelName(self.logger.getEffectiveLevel()),
    #         self.logger.getEffectiveLevel()))

    def is_empty(self, magnet):
        if magnet.hash and magnet.display_name != '':
            return True
        return False

    def _eval_announce_list(self, value):
        '''
        This function, will eval a dictionary entry, and search for a value, in this case, announce_list
        :param value: this value, represents the sub-sample of a dict
        :type value: dict
        :return: this function, returns the str with the announce_list
        :rtype: list
        '''
        _result = []
        try:
            if value[b'announce-list'] != b'announce-list':
                for items in value[b'announce-list']:
                    _result.append(str(items[0].decode('utf-8')))
        except Exception as err:
            raise MagnetBuilderTorrentAnnounceListKeyError(self.name, str(err))
        return _result

    def _eval_announce(self, value):
        '''
        This function, will eval a dictionary entry, and search for a value, in this case, announce
        :param value: this value, represents the sub-sample of a dict
        :type value: dict
        :return: this function, returns the str with the announce
        :rtype: str
        '''
        _result = ''
        try:
            if value[b'announce'].decode() != b'announce':
                _result = value[b'announce'].decode()
            _result += '&'
        except Exception as err:
            raise MagnetBuilderTorrentAnnounceKeyError(self.name, str(err))
        return _result

    def _eval_display_name(self, value):
        '''
        This function, will eval a dictionary entry, and search for a value, in this case, display_name
        :param value: this value, represents the sub-sample of a dict
        :type value: dict
        :return: this function, returns the str with the display_name
        :rtype: str
        '''
        _result = ''
        try:
            if value[b'info'][b'name'].decode() != b'name':
                _result = value[b'info'][b'name'].decode()
        except Exception as err:
            raise MagnetBuilderTorrentKeyDisplayNameError(self.name, str(err))
        return _result

    def retrieve_announce(self, announce_type='ALL'):
        '''
        This function, will connect to an online resource and retrieve a bytearray, containing the announce_list, based
        on the announce_type, that has been selected, by default using, ALL.
        :param announce_type: this value, sets the type of announce_list you're going to
        get from the internet resources.
        :type announce_type: str
        :return: this function, returns the bytearray with the announce_list.
        :rtype: bytearray
        '''
        # Create a loader
        try:
            if announce_type == 'HTTPS':
                return requests.get(HTTPS_ANNOUNCE_LIST, stream=True)
            elif announce_type == 'HTTP':
                return requests.get(HTTP_ANNOUNCE_LIST, stream=True)
            elif announce_type == 'UDP':
                return requests.get(UDP_ANNOUNCE_LIST, stream=True)
            elif announce_type == 'IP':
                return requests.get(IP_ANNOUNCE_LIST, stream=True)
            elif announce_type == 'BLACKLIST':
                return requests.get(BLACKLIST_ANNOUNCE_LIST, stream=True)
            elif announce_type == 'ALL':
                return requests.get(ALL_ANNOUNCE_LIST, stream=True)
        except Exception as err:
            raise MagnetBuilderNetworkError(self.name, err)

    def get_online_announce_list(self, announce_type='ALL'):
        '''
        This function, will retrieve all the announce_list items from the bytearray
        :param announce_type: this value, represents the announce_type, that you're going to try to retrieve
        from internet resources
        :type announce_type: str
        :return: this function, returns a clean announce_list
        :rtype: list
        '''
        _announce_list = []
        try:
            for line in self.retrieve_announce(announce_type).iter_lines():
                if line:
                    if announce_type == 'BLACKLIST':
                        line = (line.decode('utf-8').split('#')[0]).rstrip()    # Remove the comments from the line
                    else:
                        line = line.decode('utf-8')
                    _announce_list.append(line)
                    self.logger.debug('{0} Announce List Item Fetched: [ {1} ]'.format(self.name, line))
        except Exception as err:
            raise MagnetBuilderNetworkAnnounceListKeyError(self.name, err)
        return _announce_list

    def _get_hash(self, magnet_link):
        '''
        This function, uses re lib, to retrieve the value of a magnet hash, from a magnet_link
        :param magnet_link: this value, represents a magnet_link
        :type magnet_link: str
        :return: this function, returns the hash of a magnet_link
        :rtype: str
        '''
        _hash = ''
        try:
            _hash = re.search('(?<=(magnet:\?xt=urn:btih:)).*?(?=(&dn=))', magnet_link, re.IGNORECASE).group(0)
            self.logger.debug('{0} Hash [ {1} ]'.format(self.name , _hash))
        except Exception as err:
            raise MagnetBuilderMagnetKeyHashError(self.name, err)
        return _hash

    def _get_display_name(self, magnet_link):
        '''
        This function, uses re lib, to retrieve the value of display name, from a magnet_link
        :param magnet_link: this value, represents a magnet_link
        :type magnet_link: str
        :return: this, function, returns the display name of a magnet_link
        :rtype: str
        '''
        display_name = ''
        try:
            display_name = re.search('(?<=(\&dn=)).*?(?=(\&tr))', magnet_link, re.IGNORECASE).group(0)
            self.logger.debug('{0} Display Name: [ {1} ]'.format(self.name, display_name))
        except AttributeError as err:
            try:
                display_name = re.search('(?<=(\&dn=)).*', magnet_link, re.IGNORECASE).group(0)
                self.logger.debug('{0} Display Name: [ {1} ]'.format(self.name, display_name))
            except Exception as err:
                self.logger.error('[MagnetLink Error Source]: {0}'.format(magnet_link))
                raise MagnetBuilderMagnetKeyHashError(self.name, err)
        return display_name

    def _get_announce_list(self, magnet_link):
        '''
        This function, uses re lib, to retrieve the value of announce_list, from a magnet
        :param magnet_link: this value, represents a magnet_link
        :type magnet_link: str
        :return: this function, returns the announce_list of a magnet_link
        :rtype: list
        '''
        announce_list = []
        try:
            chunks = magnet_link.split('tr=')
            for chunk in chunks[1:]:
                announce_list.append(urllib.parse.unquote(chunk.rstrip('\&')))
                self.logger.debug('{0} Announce List Item: [ {1} ]'.format(self.name, urllib.parse.unquote(chunk.rstrip('\&'))))
        except Exception as e:
            self.logger.error('ErrorMagnetAnnounce Unable to Retrieve the Value {1}'.format(self.name, str(e)))
        return announce_list

    def clean_announce_list(self, magnet):
        '''
        This function, uses internal functions to retrieve a blacklist announce_list and clean the actual
        annouce_list, removing invalid announcers
        :param magnet: this value, represents a magnet instance
        :type magnet: MagnetInstance
        :return: this function, returns a magnet with the announce_list cleaned from invalid announcers
        :rtype: MagnetsIntance
        '''
        try:
            blacklist = self.get_online_announce_list('BLACKLIST')

            # Unpack the sorted list[ of list ] of announce
            announce_list = magnet.announce_list[0] + \
                            magnet.announce_list[1] + \
                            magnet.announce_list[2]
            clean_announce_list = list(set(announce_list).difference(set(blacklist)))   # Apply Logic difference
            magnet.set_announce_list(clean_announce_list)
        except MagnetBuilderNetworkError as err:
            raise MagnetBuilderNetworkError(err.class_name, err.message)
        except MagnetBuilderNetworkAnnounceListKeyError as err:
            raise MagnetBuilderMagnetKeyAnnounceListError( err.class_name, err.message)
        return magnet

    def merge_announce_list(self, magnet0, magnet1=None):
        '''
        This function, merge one magnet instance into another removing duplicated results
        :param magnet0: this value, represents a magnet instance
        :type magnet0: MagnetInstance
        :param magnet1: this value, represents a magnet instance
        :type magnet1: MagnetInstance
        :return: this function, returns a new magnet instance, with updated announce_list
        :rtype: MagnetInstance
        '''
        updated_announce_list = []
        seed = ''
        leech = ''
        size = ''
        if magnet1 is not None:

            try:
                # haz 3 veces la operacion, una para http, https y udp?
                # para no tener que volver a convertir la estructura y evitar comparaciones inutiles en los sets
                announce_list0 = magnet0.announce_list[0] + magnet0.announce_list[1] + magnet0.announce_list[2]
                announce_list1 = magnet1.announce_list[0] + magnet1.announce_list[1] + magnet1.announce_list[2]

                cmmn = list(set(announce_list1).intersection(set(announce_list0)))
                diff = list(set(announce_list1).difference(set(cmmn)))
                self.logger.debug('%s: Common\n\t\t- %s\n%s: Diference\n\t\t- %s' % (self.name, cmmn, self.name, diff))
                if diff is []:
                    updated_announce_list =  announce_list0
                else:
                    updated_announce_list = announce_list0 + diff
                self.logger.debug('%s: Result\n\t\t- %s' % (self.name, updated_announce_list))

                if magnet0['size'] >= magnet1['size']:
                    size = magnet0['size']
                else:
                    size = magnet1['size']

                if magnet0['seed'] > magnet1['seed']:
                    seed = magnet0['seed']
                else:
                    seed = magnet1['seed']
                if magnet0['leech'] > magnet1['leech']:
                    leech = magnet0['leech']
                else:
                    leech = magnet1['leech']

            except Exception as e:
                self.logger.error('{0} ErrorMergeMagnet Unable to Retrieve the Value {1}'.format(self.name, str(e)))
            return MagnetInstance(magnet0.hash, magnet0.display_name, updated_announce_list, size, seed, leech)

        else:
            return magnet0

    def raw_parse_from_file(self, file):
        '''
        This function, will parse the content from a *.torrent file, retriving all the values
        :param file: this value, represents the path to the *.torrent file
        :type file: str
        :return: this function, returns a dict with all the raw values from the *.torrent file
        :rtype: dict
        '''
        data = {}
        try:
            data = tp.parse_torrent_file(file)
        except Exception as err:
            print(err)
        return data

    def parse_from_file(self, file, base='16', size=0, seed=1, leech=1):
        '''
        This function, will parse the content of a *.torrent file, retrieving the fundamental values
        :param file: this value, represents the path to the *.torrent file
        :param base: this value, represents the base of hash you're gonna use to encode, by default 16
        :return: this function, returns a magnet instace with the fundamental values from the *.torrent file
        :rtype: MagnetInstance
        '''
        _hash = ''
        announce = ''
        display_name = ''
        announce_list = ''

        try:
            metadata = bencodepy.decode_from_file(file)     # Read from the file
            subj = metadata[b'info']

            # Calculating hash
            try:
                hashcontents = bencodepy.encode(subj)
                digest = hashlib.sha1(hashcontents).digest()    # Calculating the magnet hash 16, based on the metadata[b'info]
                if base == '16':
                    _hash = base64.b16encode(digest).decode().lower()
                else:
                    _hash = base64.b32encode(digest).decode().lower()
            except Exception as err:
                self.logger.error(err)

            try:
                display_name = self._eval_display_name(metadata)    # Gather display_name from the file
            except MagnetBuilderTorrentKeyDisplayNameError as err:
                self.logger.warning(err.message)

            try:
                announce = self._eval_announce(metadata)            # Gather announce from the file
            except MagnetBuilderTorrentAnnounceKeyError as err:
                self.logger.warning(err.message)

            try:
                announce_list = self._eval_announce_list(metadata)  # Gather announce_list from the file
            except MagnetBuilderTorrentAnnounceListKeyError as err:
                self.logger.warning(err.message)

            if announce_list is '':
                announce_list = announce

            ch_filter = chinese_filter()
            display_name = ch_filter.sub('', str(display_name))
            self.logger.debug0('{0} Generated Uri from Torrent File: {1} with Hash [ {2} ]'.format(self.name, display_name,  _hash))
            self.logger.debug('* Announce List {0}'.format(announce_list))
            return MagnetInstance(_hash, str(display_name), announce_list, size, seed, leech)
        except Exception as err:
            return MagnetInstance

    def parse_from_magnet(self, magnet_link, size=0, seed=1, leech=1):
        '''
        This function, will parse the content present in a magnet link
        :param magnet_link: this value, represents a magnet_link
        :type magnet_link: str
        :return: this function, returns a magnet instance based on the magnet values that had been retrieved
        :rtype: MagnetInstance
        '''
        try:
            announce_list = ''
            display_name = ''
            _hash = ''

            try:
                display_name = self._get_display_name(magnet_link)
            except MagnetBuilderMagnetKeyDisplayNameError as err:
                self.logger.error(err.message)

            try:
                _hash = self._get_hash(magnet_link)
            except MagnetBuilderMagnetKeyHashError as err:
                self.logger.error(err.message)

            try:
                announce_list = self._get_announce_list(magnet_link)
            except MagnetBuilderMagnetKeyAnnounceListError as err:
                self.logger.error(err.message)

            ch_filter = chinese_filter()
            display_name = ch_filter.sub('', str(display_name))

            self.logger.debug0('{0} Generated Uri from Magnet Link: {1} with Hash [ {2} ]'.format(self.name, display_name, _hash))
            self.logger.debug('* Announce List {0}'.format(announce_list))
            return MagnetInstance(_hash, str(display_name), announce_list, size, seed, leech)
        except Exception as err:
            return MagnetInstance

    def optimize_magnet(self, magnet, announce_type='ALL'):
        tmp_magnet = magnet
        try:
            announce_list = self.get_online_announce_list(announce_type=announce_type)
            magnet = self.clean_announce_list(magnet)
            magnet.add_announce_list(announce_list)

        except MagnetBuilderNetworkAnnounceListKeyError or MagnetBuilderNetworkError:
            return tmp_magnet
        return magnet
