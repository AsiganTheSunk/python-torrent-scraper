#!/usr/bin/env python

class WebScraperError(Exception):
    # """Basic exception for errors raised by webscrapers"""
    # def __init__(self, message):
    #     self.message = message
    #     super(WebScraperError, self).__init__(message)
    pass

class WebScraperCategoryError(WebScraperError):
    """When you drive too fast"""
    def __init__(self, message):
        super(WebScraperError, self).__init__(('_%s_: \n %s' % (self.__class__.__name__, message)))

class WebScraperNetworkError(WebScraperError):
    """When you drive too fast"""
    def __init__(self, message):
        super(WebScraperError, self).__init__('_%s_' % (self.__class__.__name__), message)

class WebScraperParseError(WebScraperError):
    """When you drive too fast"""
    def __init__(self, webscraper_name, message):
        super(WebScraperError, self).__init__('%s _%s_' % (webscraper_name, self.__class__.__name__), message)

class WebScraperProxyListError(WebScraperError):
    """When you drive too fast"""
    def __init__(self, webscraper_name, message):
        super(WebScraperError, self).__init__('_%s_' % (self.__class__.__name__), message)