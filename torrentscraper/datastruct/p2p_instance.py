#!/usr/bin/env python3

class P2PInstance():
    def __init__(self, name, search_type, lower_size_limit, upper_size_limit, ratio_limit, magnet_instance_list):
        self.scrapper_name = name
        self.search_type = search_type
        self.lower_size_limit = lower_size_limit
        self.upper_size_limit = upper_size_limit
        self.ratio_limit = ratio_limit
        self.magnet_instance_list = magnet_instance_list
        self.magnet_instance_batch_list = []


