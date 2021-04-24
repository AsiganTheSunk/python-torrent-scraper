#!/usr/bin/env python3

class UriBuilderError(Exception):
    """
    Raise when a there is an error in the creation of the uri
    """
    def __init__(self, webscraper_name, err, trace,*args):
        self.name = self.__class__.__name__
        self.trace = trace
        self.webscraper_name = webscraper_name
        self.err = err
        self.message = '{0}, in {1} Unable to Create the Uri: [ {2} ]'.format(self.name, webscraper_name, err)
        super(UriBuilderError, self).__init__(self.message, err, webscraper_name, *args)