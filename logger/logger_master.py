#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logger.custom_logger import CustomLogger

# Import Logging Libraries
from logging import Formatter, FileHandler, StreamHandler
from logger.constants.logger_level_type import LoggingLevelType
from logger.constants.logger_messages import message_separator


class LoggerMaster:
    def __init__(self, name, level=LoggingLevelType.INFO.value, file_streamer=True, console_streamer=False, mode='w'):
        self.name = name
        self.logger = CustomLogger(name=name, level=level)

        # Logger Master Format Definition: Console, File
        console_formatter = Formatter(fmt='[%(levelname)s]: %(message)s')
        file_formatter = Formatter(fmt='%(asctime)s - [%(levelname)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

        if file_streamer:
            # Custom Logger File Configuration: File Init Configuration
            file_handler = FileHandler(f'logs/{name}.log', mode)
            file_handler.setFormatter(file_formatter)
            file_handler.setLevel(level=level)
            self.logger.addHandler(file_handler)

        if console_streamer:
            # Custom Logger Console Configuration; Console Init Configuration
            console_handler = StreamHandler()
            console_handler.setFormatter(console_formatter)
            console_handler.setLevel(level=level)
            self.logger.addHandler(console_handler)

    def log_info_header(self, message):
        self.log_info_message()
        self.log_info_separator()
        self.log_info_message(message)
        self.log_info_separator()

    def log_info_message(self, message=''):
        self.logger.info(message)

    def log_info_separator(self):
        self.logger.info(message_separator)

    def log_debug_header(self, message):
        self.log_debug_message()
        self.log_debug_separator()
        self.log_debug_message(message)
        self.log_debug_separator()

    def log_debug_message(self, message=''):
        self.logger.debug(message)

    def log_debug_separator(self):
        self.logger.debug(message_separator)


tracker_scraper_logger = LoggerMaster('tracker_scraper', console_streamer=True)
