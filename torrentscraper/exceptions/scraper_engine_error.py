#!/usr/bin/env python3

class ScraperEngineNetworkError(Exception):
    '''Raise when a webscraper is unable to connect to a source'''
    def __init__(self, webscraper_name, err, trace, *args):
        self.name = self.__class__.__name__
        self.trace = trace
        self.webscraper_name = webscraper_name
        self.err = err
        self.message = '{0}, in  {1} Unable to Connect to the Source: [ {2} ]'.format(self.name, webscraper_name, err)
        super(ScraperEngineNetworkError, self).__init__(self.message, err, webscraper_name, *args)

class ScraperEngineUnknowError(Exception):
    '''Raise when a webscraper is unable to connect to a source'''
    def __init__(self, webscraper_name, err, trace, *args):
        self.name = self.__class__.__name__
        self.trace = trace
        self.webscraper_name = webscraper_name
        self.err = err
        self.message = '{0}, Something Went Wrong in {1} Unable to Perform the Task: [ {2} ] [ {3} ]'.format(self.name, webscraper_name, err, trace)
        super(ScraperEngineUnknowError, self).__init__(self.message, err, webscraper_name, *args)

class ScraperEngineCookieError(Exception):
    '''Raise when a webscraper is unable to connect to a source'''
    def __init__(self, webscraper_name, err, trace, *args):
        self.name = self.__class__.__name__
        self.trace = trace
        self.webscraper_name = webscraper_name
        self.err = err
        self.message = '{0}, in  {1} Unable to Retrieve Cloudflare Cookie: [ {2} ]'.format(self.name, webscraper_name, err)
        super(ScraperEngineCookieError, self).__init__(self.message, err, webscraper_name, *args)