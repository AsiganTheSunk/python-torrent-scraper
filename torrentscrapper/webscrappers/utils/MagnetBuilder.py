
import re

import urllib.parse
from bencode import bdecode
from bencodepy import decode

Magnet = 'magnet:?xt=urn:btih:224472e05e3b1087348ea1be58febb73b5456cfc&dn=Future.Man.S01E01.Pilot.1080p.AMZN.WEBRip.DDP5.1.x264-NTb%5Brartv%5D&tr=http%3A%2F%2Ftracker.trackerfix.com%3A80%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2710&tr=udp%3A%2F%2F9.rarbg.to%3A2710'

class MagnetBuilder():
    def __init__(self):
        self.all_trackers_http =  "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_http.txt"
        self.best_trackers_ip = "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best_ip.txt"
        return

    def complement_trackers(self):
        trackers = []
        # for line in requests.get(TRACKERS_URL, stream=True).iter_lines():
        #     if line: trackers.append(urllib.quote(line))
        # for line in requests.get(TRACKERS_URL2, stream=True).iter_lines():
        #     if line: trackers.append(urllib.quote(line))
        # tracker_addition = "&tr=".join(trackers)


    def retrieve_hash(self, stream):
        magnet = re.search('(?<=(magnet:\?xt\=urn:btih:)).*?(?=(&dn=))', stream, re.IGNORECASE).group(0)
        print('MagnetBuilder: Hash [ ', magnet,' ]')
        return


    def retrieve_trackers(self, stream, debug=True):
        tracker_list = []
        chunks = stream.split('tr=')
        for chunk in chunks[1:]:
            tracker_list.append(urllib.parse.unquote(chunk.rstrip('\&')))
            if debug:
                print('MagnetBuilder: Tracker [',urllib.parse.unquote(chunk.rstrip('\&')),' ]')
        return tracker_list

    def magnet_filter(self):
        return

    def magnet_merge(self):
        return

    def eval_wrapped_key(self, value, wrap_type):
        '''
        This function peform auxiliary help to the build name functions validating the content of the string
        :param value: It represents the key you're testing
        :param wrap_type: It represents the type of wrapping the string it's going to get, numbers 0 to 2, being
                        0 for [value], 1 for (value), 2 for -(value) 3 value
        :return: modified value
        '''
        if value is None:
            return ''
        else:
            if wrap_type is -1:
                if value is '':
                    return ''
                value = value.replace('&', 'and')
                return value.replace(' ', '+')
            elif wrap_type is 0:
                if value is '':
                    return value
                return ('+S' + value)
            elif wrap_type is 1:
                if value is '':
                    return value
                return ('E' + value)
            elif wrap_type is 2:
                if value is '':
                    return value
                return ('+' + value)
            elif wrap_type is 3:
                if value is '':
                    return value
                return (value + '+')
            else:
                return value


def main():
    magnet_builder = MagnetBuilder()
    magnet_builder.retrieve_hash(stream=Magnet)

    l = magnet_builder.retrieve_trackers(stream=Magnet)

    print(l)
if __name__ == '__main__':
    main()
