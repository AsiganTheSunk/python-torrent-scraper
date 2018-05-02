#!/usr/bin/env python

class ScraperEngineNetworkError(Exception):
    '''Raise when a webscraper is unable to connect to a source'''
    def __init__(self, webscraper_name, err, trace, *args):
        self.name = self.__class__.__name__
        self.trace = trace
        self.webscraper_name = webscraper_name
        self.err = err
        self.message = '{0}, in  {1} Unable to Connect to the Source: [ {2} ]'.format(self.name, webscraper_name, err)
        super(ScraperEngineNetworkError, self).__init__(self.message, err, webscraper_name, *args)