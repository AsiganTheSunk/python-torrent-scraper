#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import Logging Libraries
from logging import getLoggerClass, addLevelName
from logger.constants.logger_level_type import LoggingLevelType


class CustomLogger(getLoggerClass()):
    def __init__(self, name, level=LoggingLevelType.NOTSET):
        super().__init__(name, level)
        addLevelName(LoggingLevelType.VERBOSE.value, 'VERBOSE')

    def verbose(self, msg, *args, **kwargs):
        if self.isEnabledFor(LoggingLevelType.VERBOSE.value):
            self._log(LoggingLevelType.VERBOSE.value, msg, args, **kwargs)
