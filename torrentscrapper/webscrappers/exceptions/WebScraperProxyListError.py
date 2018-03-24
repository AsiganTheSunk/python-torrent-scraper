#!/usr/bin/env python

from torrentscrapper.webscrappers.exceptions import WebScraperError

class WebScraperProxyListError(IndexError):
    """When you drive too fast"""
    def __init__(self, webscraper_name, error):
        self.message = (('%s\n _%s_: %s' % (webscraper_name, self.__class__.__name__), error))