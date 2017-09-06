#!/usr/bin/env python

class Response(str):
    def __new__(cls, code, type, data):
        return str.__new__(cls, data)

    def __init__(self, code, type, data):
        self.code = code
        self.type = type
        self.data = data
        str.__init__(self)


