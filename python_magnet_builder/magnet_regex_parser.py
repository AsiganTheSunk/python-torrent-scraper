from python_magnet_builder.exceptions.magnet_builder_error import MagnetBuilderMagnetKeyHashError
from re import search, IGNORECASE
from urllib.parse import unquote


class MagnetRegexAttributeParser:
    def parse_hash(self, magnet_link: str):
        """
        This function, uses re lib, to retrieve the value of a magnet hash, from a magnet_link
        :param magnet_link: this value, represents a magnet_link
        :type magnet_link: str
        :return: this function, returns the hash of a magnet_link
        :rtype: str
        """
        _hash = ''
        try:
            _hash = search(r'(?<=(magnet:\?xt=urn:btih:)).*?(?=(&dn=))', magnet_link, IGNORECASE).group(0)
            # self.logger.debug('{0} Hash [ {1} ]'.format(self.name, _hash))
        except Exception as err:
            raise MagnetBuilderMagnetKeyHashError(self.__class__.__name__, err)
        return _hash

    def parse_display_name(self, magnet_link: str):
        """
        This function, uses re lib, to retrieve the value of display name, from a magnet_link
        :param magnet_link: this value, represents a magnet_link
        :type magnet_link: str
        :return: this, function, returns the display name of a magnet_link
        :rtype: str
        """
        display_name = ''
        try:
            display_name = search('(?<=(&dn=)).*?(?=(&tr))', magnet_link, IGNORECASE).group(0)
            display_name = unquote(display_name)
            # self.logger.debug('{0} Display Name: [ {1} ]'.format(self.name, display_name))
        except AttributeError as err:
            try:
                display_name = search(r'(?<=(&dn=)).*', magnet_link, IGNORECASE).group(0)
                # self.logger.debug('{0} Display Name: [ {1} ]'.format(self.name, display_name))
            except Exception as err:
                # self.logger.error('[MagnetLink Error Source]: {0}'.format(magnet_link))
                raise MagnetBuilderMagnetKeyHashError(self.__class__.__name__, err)
        return display_name

    def parse_announce_list(self, magnet_link: str):
        """
        This function, uses re lib, to retrieve the value of announce_list, from a magnet
        :param magnet_link: this value, represents a magnet_link
        :type magnet_link: str
        :return: this function, returns the announce_list of a magnet_link
        :rtype: list
        """
        announce_list = []
        try:
            announcer_chunks = magnet_link.split('tr=')
            for announce in announcer_chunks[1:]:
                announce_list.append(unquote(announce.rstrip('\&')))
                # self.logger.debug(
                #     '{0} Announce List Item: [ {1} ]'.format(self.name, unquote(chunk.rstrip('\&'))))
        except Exception as e:
            pass
            # self.logger.error('ErrorMagnetAnnounce Unable to Retrieve the Value {1}'.format(self.name, str(e)))
        return announce_list
