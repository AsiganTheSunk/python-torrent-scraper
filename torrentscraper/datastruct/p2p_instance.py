#!/usr/bin/env python3

class P2PInstance():
    def __init__(self, scraper_name, websearch, magnet_instance_list):
        self.scrapper_name = scraper_name
        self.search_type = websearch['search_type']
        self.surrogated_id = websearch['surrogated_id']
        self.ratio_limit = websearch['ratio_limit']
        self.lower_size_limit = websearch['lower_size_limit']
        self.upper_size_limit = websearch['upper_size_limit']
        self.magnet_instance_list = magnet_instance_list

