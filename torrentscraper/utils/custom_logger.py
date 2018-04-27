
# Import System Libraries
from logging import getLoggerClass, addLevelName, NOTSET

VERBOSE = 5
DEBUG0 = 15

class CustomLogger(getLoggerClass()):
    def __init__(self, name, level=NOTSET):
        super().__init__(name, level)
        addLevelName(VERBOSE, 'VERBOSE')
        addLevelName(DEBUG0, 'DEBUG0')

    def verbose(self, msg, *args, **kwargs):
        if self.isEnabledFor(VERBOSE):
            self._log(VERBOSE, msg, args, **kwargs)

    def debug0(self, msg, *args, **kwargs):
        if self.isEnabledFor(DEBUG0):
            self._log(DEBUG0, msg, args, **kwargs)