#!/usr/bin/env python

class MagnetBuilderMagnetKeyError(Exception):
    '''Raise when a there is no more proxy entries in the proxy_list of a webscraper'''
    def __init__(self, class_name, err, *args):
        self.name = self.__class__.__name__
        # self.trace = trace
        self.class_name = class_name
        self.err = err
        self.message = '[ERROR]: {0}, in {1} Unable to Retrieve Value from Magnet: [ {2} ]'.format(self.name, class_name, err)
        super( MagnetBuilderMagnetKeyError, self).__init__(self.message, err, class_name, *args)

class MagnetBuilderTorrentKeyError(Exception):
    '''Raise when a there is no more proxy entries in the proxy_list of a webscraper'''
    def __init__(self, class_name, err, *args):
        self.name = self.__class__.__name__
        # self.trace = trace
        self.class_name = class_name
        self.err = err
        self.message = '{0}, in {1} Unable to Retrieve Value from Torrent: [ {2} ]'.format(self.name, class_name, err)
        super(MagnetBuilderTorrentKeyError, self).__init__(self.message, err, class_name, *args)