from python_magnet_builder.exceptions.magnet_builder_error import MagnetBuilderNetworkError, MagnetBuilderMagnetKeyAnnounceListError, MagnetBuilderNetworkAnnounceListKeyError
from requests import get, Response
from python_magnet_builder.data_struct.magnet_instance import MagnetInstance

from python_magnet_builder.constants.magnet_announce_type import MagnetAnnounceType
from python_magnet_builder.constants.magnet_announce_list import ANNOUNCE_LIST


class MagnetAnnounceBuilder:
    def retrieve_announce_list_from_endpoint(self, announce_type: MagnetAnnounceType = MagnetAnnounceType.ALL) -> Response:
        """
        This function, will connect to a internet endpoint and retrieve a bytearray, containing
        the announce_list. The returned announce_list will be based on the AnnounceType that has
        been provided. The default value is AnnounceType.ALL.

        :param announce_type: this value, sets the type of announce_list you're going to get from
         the internet endpoint.
        :type announce_type: MagnetAnnounceType
        :return: this function, returns the bytearray with the announce_list.
        :rtype: Response
        """
        try:
            response = get(ANNOUNCE_LIST[announce_type], stream=True)
            assert response, 200
            return response
        except AssertionError as error:
            raise MagnetBuilderNetworkError(self.__class__.__name__, error)

    def get_announce_list_from_endpoint(self, announce_type: MagnetAnnounceType = MagnetAnnounceType.ALL):
        """
        This function, will retrieve all the announce_list items from the bytearray
        :param announce_type: this value, represents the announce_type, that you're going to try to retrieve
        from internet resources
        :type announce_type: str
        :return: this function, returns a clean announce_list
        :rtype: list
        """
        _announce_list = []
        try:
            response: Response = self.retrieve_announce_list_from_endpoint(announce_type)
            for response_line in response.iter_lines():
                if response_line:
                    if announce_type is MagnetAnnounceType.BLACKLIST:
                        # Remove the comments from the line
                        response_line = (response_line.decode('utf-8').split('#')[0]).rstrip()
                    else:
                        response_line = response_line.decode('utf-8')

                    _announce_list.append(response_line)
                    # self.logger.debug('{0} Announce List Item Fetched: [ {1} ]'.format(self.name, line))
        except Exception as err:
            raise MagnetBuilderNetworkAnnounceListKeyError(self.__class__.__name__, err)
        return _announce_list

    def clean(self, magnet: MagnetInstance) -> MagnetInstance:
        """
        This function, uses internal functions to retrieve a blacklist announce_list and clean the actual
        annouce_list, removing invalid announcers
        :param magnet: this value, represents a magnet instance
        :type magnet: MagnetInstance
        :return: this function, returns a magnet with the announce_list cleaned from invalid announcers
        :rtype: MagnetsInstance
        """
        try:
            announce_blacklist = self.retrieve_announce_list_from_endpoint(MagnetAnnounceType.BLACKLIST)
            # Cast List to Set, to Delete repeated values, then apply Logic Difference to subtract blacklisted elements
            clean_announce_list = list(set(magnet.unpack_announce_list()).difference(set(announce_blacklist)))
            magnet.set_announce_list(clean_announce_list)
        except MagnetBuilderNetworkError as err:
            raise MagnetBuilderNetworkError(err.class_name, err.message)
        except MagnetBuilderNetworkAnnounceListKeyError as err:
            raise MagnetBuilderMagnetKeyAnnounceListError(err.class_name, err.message)
        return magnet

    def merge(self, magnet0: MagnetInstance, magnet1: MagnetInstance = None) -> MagnetInstance:
        """
        This function, merge one magnet instance into another removing duplicated results
        :param magnet0: this value, represents a magnet instance
        :type magnet0: MagnetInstance
        :param magnet1: this value, represents a magnet instance
        :type magnet1: MagnetInstance
        :return: this function, returns a new magnet instance, with updated announce_list
        :rtype: MagnetInstance
        """
        updated_announce_list = []
        seed = ''
        leech = ''
        size = ''
        if magnet1 is not None:

            try:
                magnet0_announce_list = magnet0.unpack_announce_list()
                magnet1_announce_list = magnet1.unpack_announce_list()

                common_announcers = list(set(magnet1_announce_list).intersection(set(magnet0_announce_list)))
                different_announcers = list(set(magnet1_announce_list).difference(set(common_announcers)))

                # self.logger.debug('%s: Common\n\t\t- %s\n%s: Diference\n\t\t- %s' % (self.name, cmmn, self.name, diff))
                # self.logger.debug('%s: Result\n\t\t- %s' % (self.name, updated_announce_list))

                size = (magnet0['size'], magnet1['size'])[magnet0['size'] >= magnet1['size']]
                seed = (magnet0['seed'], magnet1['seed'])[magnet0['seed'] > magnet1['seed']]
                leech = (magnet0['leech'], magnet1['leech'])[magnet0['leech'] > magnet1['leech']]
                magnet0.set_announce_list(magnet0_announce_list + different_announcers)

            except Exception as e:
                pass
                # self.logger.error('{0} ErrorMergeMagnet Unable to Retrieve the Value {1}'.format(self.name, str(e)))
            return MagnetInstance(magnet0.hash, magnet0.display_name, updated_announce_list, size, seed, leech)

        else:
            return magnet0



