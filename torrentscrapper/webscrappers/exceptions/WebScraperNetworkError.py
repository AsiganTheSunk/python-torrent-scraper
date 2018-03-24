#!/usr/bin/env python

from torrentscrapper.webscrappers.exceptions import WebScraperError

class WebScraperParseError(WebScraperError):
    """When you drive too fast"""
    def __init__(self, message):
        super(WebScraperError, self).__init__('_%s_' % (self.__class__.__name__), message)