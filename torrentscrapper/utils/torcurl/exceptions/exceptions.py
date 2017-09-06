#!/usr/bin/env python
# Base Exceptions

class Error(Exception):
    """Base class for other exceptions

    Attributes:
        msg  -- explanation of the error
    """
    def __init__(self, arg=None):
        if arg is None:
            arg = 'An error ocurred with coco'
        self.msg = arg
        super(Error, self).__init__(arg)

    pass

# Custom Exceptions

class UrlValueError(Error):
    """Exception raised for errors in the input.

    Attributes:
        msg  -- explanation of the error
    """
    def __init__(self):
        super(UrlValueError, self).__init__(arg="URL ERROR")
