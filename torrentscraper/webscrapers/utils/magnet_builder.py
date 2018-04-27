#!/usr/bin/env python

# Import System Libraries
from collections.abc import Mapping
import urllib.parse
import traceback
import hashlib
import base64
import re

# Import External Libraries
import torrent_parser as tp
import bencodepy
import requests

# Import Custom Exceptions
from torrentscraper.webscrapers.utils.exceptions.magnet_builder_error import MagnetBuilderMagnetKeyError
from torrentscraper.webscrapers.utils.exceptions.magnet_builder_error import MagnetBuilderTorrentKeyError

# Constants
HTTPS_ANNOUNCE_LIST = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_https.txt'
HTTP_ANNOUNCE_LIST = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_http.txt'
UDP_ANNOUNCE_LIST = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_udp.txt'
IP_ANNOUNCE_LIST = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_ip.txt'
ALL_ANNOUNCE_LIST = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt'
BLACKLIST_ANNOUNCE_LIST = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/blacklist.txt'


class MagnetBuilder(object):
    def __init__(self):
        self.name = self.__class__.__name__

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
            raise MagnetBuilderTorrentKeyError(self.name, str(err))
            #print('[WARNING]: {0} Unable to Retrieve Announce List Value: {1}'.format(self.name, str(e)))
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
            raise MagnetBuilderTorrentKeyError(self.name, str(err))
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
            raise MagnetBuilderTorrentKeyError(self.name, str(err))
        return _result


    def _select_announce_type(self, announce_type='ALL'):
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

    def _get_online_announce_list(self, announce_type, debug=False):
        '''
        This function, will retrieve all the announce_list items from the bytearray
        :param announce_type: this value, represents the announce_type, that you're going to try to retrieve
        from internet resources
        :type announce_type: bytearray
        :param debug: this value, sets the function in debug mode, printing some additional info about the operations
        :type debug: bool
        :return: this function, returns a clean announce_list
        :rtype: list
        '''
        _announce_list = []
        try:
            for line in self._select_announce_type(announce_type=announce_type).iter_lines():
                if line:
                    if announce_type == 'BLACKLIST':
                        line = (line.decode('utf-8').split('#')[0]).rstrip()    # Remove the comments from the line
                    else:
                        line = line.decode('utf-8')
                    _announce_list.append(line)
                    if debug:
                        print('{0} Announce Fetched: [ {1} ]'.format(self.name, line))
        except Exception as e:
            print('{0} ErrorMagnetDisplayName Unable to Retrieve the Value: {1}'.format(self.name, str(e)))
        return _announce_list

    def _get_hash(self, magnet_link, debug=True):
        '''
        This function, uses re lib, to retrieve the value of a magnet hash, from a magnet_link
        :param magnet_link: this value, represents a magnet_link
        :type magnet_link: str
        :param debug: this value, sets the function in debug mode, printing some additional info about the operations
        :type debug: bool
        :return: this function, returns the hash of a magnet_link
        :rtype: str
        '''
        _hash = ''
        try:
            _hash = re.search('(?<=(magnet:\?xt=urn:btih:)).*?(?=(&dn=))', magnet_link, re.IGNORECASE).group(0)
            if debug:
                print('{0} Hash [ {1} ]'.format(self.name , _hash))
        except Exception as e:
            print('{0} ErrorMagnetHash Unable to Retrieve the Value: {1}'.format(self.name, str(e)))
        return _hash

    def _get_display_name(self, magnet_link, debug=False):
        '''
        This function, uses re lib, to retrieve the value of display name, from a magnet_link
        :param magnet_link: this value, represents a magnet_link
        :type magnet_link: str
        :param debug: this value, sets the function in debug mode, printing some additional info about the operations
        :type debug: bool
        :return: this, function, returns the display name of a magnet_link
        :rtype: str
        '''
        display_name = ''
        try:
            display_name = re.search('(?<=(&dn=)).*?(?=(&tr))', magnet_link, re.IGNORECASE).group(0)
            if debug:
                print('{0} Display Name: [ {1} ]'.format(self.name, display_name))
        except Exception as e:
            print('{0} ErrorMagnetDisplayName Unable to Retrieve the Value {1}'.format(self.name, str(e)))
        return display_name

    def _get_announce_list(self, magnet_link, debug=False):
        '''
        This function, uses re lib, to retrieve the value of announce_list, from a magnet
        :param magnet_link: this value, represents a magnet_link
        :type magnet_link: str
        :param debug: this value, sets the function in debug mode, printing some additional info about the operations
        :type debug: bool
        :return: this function, returns the announce_list of a magnet_link
        :rtype: list
        '''
        announce_list = []
        try:
            chunks = magnet_link.split('tr=')
            for chunk in chunks[1:]:
                announce_list.append(urllib.parse.unquote(chunk.rstrip('\&')))
                if debug:
                    print('{0} Announce List: [ {1} ]'.format(self.name, urllib.parse.unquote(chunk.rstrip('\&'))))
        except Exception as e:
            print('{0} ErrorMagnetAnnounce Unable to Retrieve the Value {1}'.format(self.name, str(e)))
        return announce_list

    def clean_announce_list(self, magnet, debug=False):
        '''
        This function, uses internal functions to retrieve a blacklist announce_list and clean the actual
        annouce_list, removing invalid announcers
        :param magnet: this value, represents a magnet instance
        :type magnet: MagnetInstance
        :param debug: this value, sets the function in debug mode, printing some additional info about the operations
        :type debug: bool
        :return: this function, returns a magnet with the announce_list cleaned from invalid announcers
        :rtype: MagnetsIntance
        '''
        blacklist = self._get_online_announce_list('BLACKLIST', debug)

        # Unpack the sorted list[ of list ] of announce
        announce_list = magnet.announce_list[0] + \
                        magnet.announce_list[1] + \
                        magnet.announce_list[2]
        clean_announce_list = list(set(announce_list).difference(set(blacklist)))   # Apply Logic difference
        magnet.set_announce_list(clean_announce_list)
        return magnet

    def merge_announce_list(self, magnet0, magnet1=None, debug=False):
        '''
        This function, merge one magnet instance into another removing duplicated results
        :param magnet0: this value, represents a magnet instance
        :type magnet0: MagnetInstance
        :param magnet1: this value, represents a magnet instance
        :type magnet1: MagnetInstance
        :param debug: this value, sets the function in debug mode, printing some additional info about the operations
        :type debug: bool
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
                if debug:
                    print('%s: Common\n\t\t- %s\n%s: Diference\n\t\t- %s' % (self.name, cmmn, self.name, diff))
                if diff is []:
                    updated_announce_list =  announce_list0
                else:
                    updated_announce_list = announce_list0 + diff
                if debug:
                    print('%s: Result\n\t\t- %s' % (self.name, updated_announce_list))

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
                print('{0} ErrorMergeMagnet Unable to Retrieve the Value {1}'.format(self.name, str(e)))
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
        except Exception as e:
            print(e)
        return data

    def parse_from_file(self, file, base='16', size=0, seed=1, leech=1, debug=False):
        '''
        This function, will parse the content of a *.torrent file, retrieving the fundamental values
        :param file: this value, represents the path to the *.torrent file
        :param base: this value, represents the base of hash you're gonna use to encode, by default 16
        :param debug: this value, sets the function in debug mode, printing some additional info about the operations
        :type debug: bool
        :return: this function, returns a magnet instace with the fundamental values from the *.torrent file
        :rtype: MagnetInstance
        '''
        _hash = ''
        announce = ''
        display_name = ''
        announce_list = ''

        metadata = bencodepy.decode_from_file(file)     # Read from the file
        subj = metadata[b'info']

        # Calculating hash
        hashcontents = bencodepy.encode(subj)
        digest = hashlib.sha1(hashcontents).digest()    # Calculating the magnet hash 16, based on the metadata[b'info]
        if base == '16':
            _hash = base64.b16encode(digest).decode().lower()
        else:
            _hash = base64.b32encode(digest).decode().lower()

        try:
            display_name = self._eval_display_name(metadata)    # Gather display_name from the file
        except MagnetBuilderTorrentKeyError as err:
            print(err.message)
        try:
            announce = self._eval_announce(metadata)            # Gather announce from the file
        except MagnetBuilderTorrentKeyError as err:
            print(err.message)
        try:
            announce_list = self._eval_announce_list(metadata)  # Gather announce_list from the file
        except MagnetBuilderTorrentKeyError as err:
            print(err.message)

        if announce_list is '':
            announce_list = announce

        if debug:
            print('%s: Generated Uri\n\t\t- Hash [ %s ]: %s\n\t\t- DisplayName: %s\n\t\t- Trackers: %s' % (self.name, base, _hash, display_name, announce_list))
        return MagnetInstance(_hash, display_name, announce_list, size, seed, leech)

    def parse_from_magnet(self, magnet_link, size=0, seed=1, leech=1, debug=False):
        '''
        This function, will parse the content present in a magnet link
        :param magnet_link: this value, represents a magnet_link
        :type magnet_link: str
        :param debug: this value, sets the function in debug mode, printing some additional info about the operations
        :type debug: bool
        :return: this function, returns a magnet instance based on the magnet values that had been retrieved
        :rtype: MagnetInstance
        '''
        return MagnetInstance(self._get_hash(magnet_link, debug),
                              self._get_display_name(magnet_link, debug),
                              self._get_announce_list(magnet_link, debug), size, seed, leech)

    def parse_magnet_list(self, magnet_link_list):
        l = []
        for magnet_link in magnet_link_list:
            l.append(magnet_link)
        return l

class MagnetInstance(Mapping):
    def __init__(self, _hash, display_name, announce_list, size=0, seed=1, leech=1):
        self.name = self.__class__.__name__
        self.hash = _hash
        self.display_name = display_name
        self.size = size
        self.seed = int(seed)
        self.leech = int(leech)
        self.announce_list = self._get_announce_list(announce_list)
        self.activity = {'seed': self.seed, 'leech': self.leech}
        self._storage = {'hash': self.hash,
                 'display_name': self.display_name,
                         'size': self.size,
                         'seed': self.seed,
                         'leech': self.leech,
                         'ratio': self.seed/self.leech,
                         'announce_list':{'https':self.announce_list[0],
                                          'http':self.announce_list[1],
                                          'udp':self.announce_list[2]}}

    def __getitem__(self, key):
        if key == 'magnet':
            return self._get_magnet()
        if key == 'status':
            return self._get_status()
        if key == 'activity':
            return self.activity
        return self._storage[key]

    def __iter__(self):
        return iter(self._storage)    # ``ghost`` is invisible

    def __len__(self):
        return len(self._storage)

    def __repr__(self):
        '''
        This function, overrides the default function method.
        :return: this function, returns every component in the magnet instance
        :rtype:
        '''
        return

    def set_announce_list(self, announce_list):
        '''
        This function, sets the announce_list to the magnet instance
        :param announce_list:
        :return: None
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

    def _get_status(self):
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
        :return: this function, returns a string, with the magnet_link
        :rtype: str
        '''
        # [['&tr='+ str(announce) for announce in announce_subtype] for announce_subtype in self.announce_list]
        magnet_uri = ''
        announce_list = ''
        try:
            for announce_subtype in self.announce_list:
                for announce in announce_subtype:
                    announce_list += '&tr=' + urllib.parse.quote(announce)

            magnet_uri += 'magnet:?xt=urn:btih:' + self.hash \
                          + '&dn=' + self.display_name\
                          + announce_list
        except Exception as e:
            print('%s: ErrorGeneratingMagnetUri %s' % (self.name, e))
        return magnet_uri


def main():
    torrent_file = 'C:/Users/Asigan/Documents/GitHub/python-torrent-scraper/torrentscraper/Rick.and.Morty.S03E08.2017.HDTV.x264.-.SPARKS.torrent'
    torrent_file1 = 'C:/Users/Asigan/Documents/GitHub/python-torrent-scraper/torrentscraper/The.Hurricane.Heist.2018.1080p.KORSUB.HDRip.x264.AAC2.0-STUTTERSHIT-[rarbg.to].torrent'
    torrent_file2 = 'C:/Users/Asigan/Documents/GitHub/python-torrent-scraper/torrentscraper/[HorribleSubs].Overlord.II.-.13.[720p].torrent'
    Magnet2 = 'magnet:?xt=urn:btih:b105818432fcef1628a1024bd761206eb0f66f9a&dn=Lady.Bird.2017.1080p.BluRay.H264.AAC&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Fzer0day.ch%3A1337&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969'
    Magnet1 = 'magnet:?xt=urn:btih:224472e05e3b1087348ea1be58febb73b5456cfc&dn=Future.Man.S01E01.Pilot.1080p.AMZN.WEBRip.DDP5.1.x264-NTb%5Brartv%5D&tr=http%3A%2F%2Ftracker.trackerfix.com%3A80%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2710&tr=udp%3A%2F%2F9.rarbg.to%3A2710'
    test=True
    if test:
        mbuilder = MagnetBuilder()
        minstance0 = mbuilder.parse_from_file(torrent_file1)
        minstance1 = mbuilder.parse_from_magnet(Magnet1)

        print(minstance0['hash'])
        print(minstance0['display_name'])
        print(minstance0['announce_list'])

        print(minstance1['hash'])
        print(minstance1['display_name'])
        print(minstance1['announce_list'])

        minstance1.add_announce_list(mbuilder._get_online_announce_list(announce_type='HTTPS'))
        minstance1.add_announce_list(['http://henbt.com:2710/announce'])

        print(minstance1['announce_list'])
        print(minstance1['magnet'])

        mbuilder.clean_announce_list(minstance1)

        print(minstance1['announce_list'])
        print(minstance1['magnet'])

        minstance1['stats']

if __name__ == '__main__':
    main()