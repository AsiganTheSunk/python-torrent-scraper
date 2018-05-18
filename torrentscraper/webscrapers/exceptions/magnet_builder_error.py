#!/usr/bin/env python3

class MagnetBuilderMagnetKeyHashError(Exception):
    '''Raise when a there is no more proxy entries in the proxy_list of a webscraper'''
    def __init__(self, class_name, err, *args):
        self.name = self.__class__.__name__
        # self.trace = trace
        self.class_name = class_name
        self.err = err
        self.message = '[ERROR]: {0}, in {1} Unable to Retrieve KeyHash Value from Magnet: [ {2} ]'.format(self.name, class_name, err)
        super(MagnetBuilderMagnetKeyHashError, self).__init__(self.message, err, class_name, *args)

class MagnetBuilderMagnetKeyDisplayNameError(Exception):
    '''Raise when a there is no more proxy entries in the proxy_list of a webscraper'''
    def __init__(self, class_name, err, *args):
        self.name = self.__class__.__name__
        # self.trace = trace
        self.class_name = class_name
        self.err = err
        self.message = '[ERROR]: {0}, in {1} Unable to Retrieve KeyDisplayName Value from Magnet: [ {2} ]'.format(self.name, class_name, err)
        super(MagnetBuilderMagnetKeyDisplayNameError, self).__init__(self.message, err, class_name, *args)

class MagnetBuilderMagnetKeyAnnounceListError(Exception):
    '''Raise when a there is no more proxy entries in the proxy_list of a webscraper'''
    def __init__(self, class_name, err, *args):
        self.name = self.__class__.__name__
        # self.trace = trace
        self.class_name = class_name
        self.err = err
        self.message = '[ERROR]: {0}, in {1} Unable to Retrieve KeyAnnounce Value from Magnet: [ {2} ]'.format(self.name, class_name, err)
        super(MagnetBuilderMagnetKeyAnnounceListError, self).__init__(self.message, err, class_name, *args)

class MagnetBuilderNetworkError(Exception):
    '''Raise when a there is no more proxy entries in the proxy_list of a webscraper'''
    def __init__(self, class_name, err, *args):
        self.name = self.__class__.__name__
        # self.trace = trace
        self.class_name = class_name
        self.err = err
        self.message = '[ERROR]: {0}, in {1}: [ {2} ]'.format(self.name, class_name, err)
        super(MagnetBuilderNetworkError, self).__init__(self.message, err, class_name, *args)


class MagnetBuilderNetworkAnnounceListKeyError(Exception):
    '''Raise when a there is no more proxy entries in the proxy_list of a webscraper'''
    def __init__(self, class_name, err, *args):
        self.name = self.__class__.__name__
        # self.trace = trace
        self.class_name = class_name
        self.err = err
        self.message = '{0}, in {1} Unable to Retrieve AnnounceListKey Value from Source: [ {2} ]'.format(self.name, class_name, err)
        super(MagnetBuilderNetworkAnnounceListKeyError, self).__init__(self.message, err, class_name, *args)

class MagnetBuilderTorrentKeyDisplayNameError(Exception):
    '''Raise when a there is no more proxy entries in the proxy_list of a webscraper'''
    def __init__(self, class_name, err, *args):
        self.name = self.__class__.__name__
        # self.trace = trace
        self.class_name = class_name
        self.err = err
        self.message = '{0}, in {1} Unable to Retrieve Value from Torrent: [ {2} ]'.format(self.name, class_name, err)
        super(MagnetBuilderTorrentKeyDisplayNameError, self).__init__(self.message, err, class_name, *args)

class MagnetBuilderTorrentKeyHashError(Exception):
    '''Raise when a there is no more proxy entries in the proxy_list of a webscraper'''
    def __init__(self, class_name, err, *args):
        self.name = self.__class__.__name__
        # self.trace = trace
        self.class_name = class_name
        self.err = err
        self.message = '{0}, in {1} Unable to Retrieve KeyHash Value from Torrent: [ {2} ]'.format(self.name, class_name, err)
        super(MagnetBuilderTorrentKeyHashError, self).__init__(self.message, err, class_name, *args)

class MagnetBuilderTorrentAnnounceKeyError(Exception):
    '''Raise when a there is no more proxy entries in the proxy_list of a webscraper'''
    def __init__(self, class_name, err, *args):
        self.name = self.__class__.__name__
        # self.trace = trace
        self.class_name = class_name
        self.err = err
        self.message = '{0}, in {1} Unable to Retrieve AnnounceKey Value from Torrent: [ {2} ]'.format(self.name, class_name, err)
        super(MagnetBuilderTorrentAnnounceKeyError, self).__init__(self.message, err, class_name, *args)

class MagnetBuilderTorrentAnnounceListKeyError(Exception):
    '''Raise when a there is no more proxy entries in the proxy_list of a webscraper'''
    def __init__(self, class_name, err, *args):
        self.name = self.__class__.__name__
        # self.trace = trace
        self.class_name = class_name
        self.err = err
        self.message = '{0}, in {1} Unable to Retrieve AnnounceListKey Value from Torrent: [ {2} ]'.format(self.name, class_name, err)
        super(MagnetBuilderTorrentAnnounceListKeyError, self).__init__(self.message, err, class_name, *args)