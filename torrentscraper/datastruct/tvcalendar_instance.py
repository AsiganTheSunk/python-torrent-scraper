#!/usr/bin/env python

class TVCalendarInstance():
    def __init__(self, main_month_uri):
        self.main_month_uri = main_month_uri
        self.next_month_uri = ''
        self.previous_month_uri = ''
        self.main_calendar = {}
