from enum import Enum


class MagnetAnnounceType(Enum):
    HTTPS = 'HTTPS'
    HTTP = 'HTTP'
    UDP = 'UDP'
    IP = 'IP'
    BLACKLIST = 'BLACKLIST'
    ALL = 'ALL'

