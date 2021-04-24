# Import Custom Exceptions
from core.web.scraper.exceptions.webscraper_error import WebScraperProxyListError

# Import System Libraries
import traceback

# Import Custom Data Structure
from core.web.scraper.data_struct.rawdata_instance import RAWDataInstance

# Todo: Change to ScraperSession + ScraperHelper for the clean up of the malformed shit


class ScraperInstance:
    def __init__(self, proxy_list, supported_searches):
        self.proxy_index = 0
        self.proxy_list = proxy_list
        self._proxy_list_length = len(self.proxy_list)
        self.main_page = self.proxy_list[self.proxy_index]
        self.supported_searches = supported_searches

    def get_proxy_endpoint(self):
        return self.main_page

    def update_proxy_index(self) -> None:
        """
        This function will try to update the current proxy index for the scraper, during a failed search
        :return:
        """
        tmp_proxy_index = self.proxy_index
        if self._proxy_list_length > self.proxy_index:
            tmp_proxy_index += 1
        self.proxy_index = tmp_proxy_index

    def update_proxy_target(self) -> None:
        """
        This Function will try to update the current proxy target used in the search
        :return:
        """
        try:
            self.update_proxy_index()
            self.main_page = self.proxy_list[self.proxy_index]
        except IndexError as err:
            raise WebScraperProxyListError(self.__class__.__name__, err, traceback.format_exc())

    @staticmethod
    def validate_peer_value(peer: str) -> int:
        """
        This Function will validate the peer value been retrieved from the target proxy during the search
        :param peer:
        :return:
        """
        if peer.strip() == '0':
            return int('1')
        return int(peer)

    @staticmethod
    def validate_size_value(size: str) -> int:
        """
        This Function will validate the size value
        :param size:
        :return:
        """
        try:
            if 'MB' in size:
                return int(float(size[:-3]))
            elif 'MiB' in size:
                return int(float(size[:-4]))
            elif 'GB' in size:
                return int(float(size[:-3]) * 1000)
            elif 'GiB' in size:
                return int(float(size[:-4]) * 1000)
        except ValueError:
            if 'MB' in size:
                return int(float(size[:-6]))
            if 'MiB' in size:
                return int(float(size[:-7]))
            elif 'GB' in size:
                return int(float(size[:-6] * 1000))
            elif 'GiB' in size:
                return int(float(size[:-7] * 1000))
        except Exception as error:
            print(f'validate_size_value: {error}')
            return 0

    def get_raw_data(self, content) -> RAWDataInstance:
        pass

    def get_magnet_link(self, content) -> str:
        pass
