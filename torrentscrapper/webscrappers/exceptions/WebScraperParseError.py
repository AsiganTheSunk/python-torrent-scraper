#!/usr/bin/env python

from torrentscrapper.webscrappers.exceptions import WebScraperError

class WebScraperParseError(WebScraperError):
    """When you drive too fast"""
    def __init__(self, webscraper_name, original_exception):
        super(WebScraperError, self).__init__('%s _%s_' % (webscraper_name, self.__class__.__name__), original_exception)