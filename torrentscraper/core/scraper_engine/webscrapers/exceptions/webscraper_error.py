#!/usr/bin/env python3


class WebScraperProxyListError(IndexError):
    '''Raise when a there is no more proxy entries in the proxy_list of a webscrapers'''
    def __init__(self, webscraper_name, err, trace,*args):
        self.name = self.__class__.__name__
        self.trace = trace
        self.webscraper_name = webscraper_name
        self.err = err
        self.message = '{0}, in {1} Proxy List is Empty: [ {2} ]'.format(self.name, webscraper_name, err)
        super(WebScraperProxyListError, self).__init__(self.message, err, webscraper_name, *args)


class WebScraperParseError(Exception):
    '''Raise when a webscrapers is unable to parse raw values from current search'''
    def __init__(self, webscraper_name, err, trace='', *args):
        self.name = self.__class__.__name__
        self.trace = trace
        self.webscraper_name = webscraper_name
        self.err = err
        self.message = '{0}, in {1} Unable to Parse Raw Values from Search Result Response: [ {2} ]'.format(self.name, webscraper_name, err)
        super(WebScraperParseError, self).__init__(self.message, err, webscraper_name, *args)


class WebScraperContentError(Exception):
    '''Raise when a webscrapers is unable to parse raw values from current search'''
    def __init__(self, webscraper_name, err, trace='', *args):
        self.name = self.__class__.__name__
        self.trace = trace
        self.webscraper_name = webscraper_name
        self.err = err
        self.message = '{0}, in {1} Content Error in Search Result Response: [ {2} ]'.format(self.name, webscraper_name, err)
        super(WebScraperContentError, self).__init__(self.message, err, webscraper_name, *args)


