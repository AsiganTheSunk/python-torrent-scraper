from python_magnet_builder.exceptions.magnet_builder_error import MagnetBuilderTorrentAnnounceListKeyError, \
    MagnetBuilderTorrentKeyDisplayNameError, MagnetBuilderTorrentAnnounceKeyError


class MagnetByteAttributeReader:

    def read_info(self, magnet_byte_metadata):
        _result = ''
        try:
            if magnet_byte_metadata[b'info'] != b'info':
                _result = magnet_byte_metadata[b'info']
        except Exception as err:
            raise MagnetBuilderTorrentKeyDisplayNameError(self.__class__.__name__, str(err))
        return _result

    def read_display_name(self, magnet_byte_metadata):
        """
        This function, will eval a dictionary entry, and search for a value, in this case, display_name
        :param magnet_byte_metadata: this value, represents the sub-sample of an OrderedDict
        :type magnet_byte_metadata: OrderedDict
        :return: this function, returns the str with the display_name
        :rtype: str
        """
        _result = ''
        try:
            if magnet_byte_metadata[b'info'][b'name'] != b'name':
                _result = magnet_byte_metadata[b'info'][b'name'].decode('utf-8')
        except Exception as err:
            raise MagnetBuilderTorrentKeyDisplayNameError(self.__class__.__name__, str(err))
        return _result

    def read_announce(self, magnet_byte_metadata):
        """
        This function, will eval a dictionary entry, and search for a value, in this case, announce
        :param magnet_byte_metadata: this value, represents the sub-sample of a OrderedDict
        :type magnet_byte_metadata: OrderedDict
        :return: this function, returns the str with the announce
        :rtype: str
        """
        _result = ''
        try:
            if magnet_byte_metadata[b'announce'] != b'announce':
                _result = magnet_byte_metadata[b'announce'].decode()
            # _result += '&'
        except Exception as err:
            raise MagnetBuilderTorrentAnnounceKeyError(self.__class__.__name__, str(err))
        return _result

    def read_announce_list(self, magnet_byte_metadata) -> list[str]:
        """
        This function, will eval a dictionary entry, and search for a value, in this case, announce_list
        :param magnet_byte_metadata: this value, represents the sub-sample of a OrderedDict
        :type magnet_byte_metadata: OrderedDict
        :return: this function, returns the str with the announce_list
        :rtype: list
        """
        _result = []
        try:
            if magnet_byte_metadata[b'announce-list'] != b'announce-list':
                for announce in magnet_byte_metadata[b'announce-list']:
                    _result.append(str(announce[0].decode('utf-8')))
        except Exception as err:
            raise MagnetBuilderTorrentAnnounceListKeyError(self.__class__.__name__, str(err))
        return _result
