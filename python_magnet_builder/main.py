from magnet_regex_parser import MagnetRegexAttributeParser
from magnet_byte_reader import MagnetByteAttributeReader
from magnet_reader import MagnetReader
from magnet_builder import MagnetBuilder

if __name__ == '__main__':
    magnet_link = 'magnet:?xt=urn:btih:d0b2494cece9920a7d4974d051d4fa3caea66a71&dn=The.Marksman.2021.1080p.WEB-DL.DD5.1.H264-FGT&tr=http%3A%2F%2Ftracker.trackerfix.com%3A80%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2820&tr=udp%3A%2F%2F9.rarbg.to%3A2870&tr=udp%3A%2F%2Ftracker.thinelephant.org%3A12720&tr=udp%3A%2F%2Ftracker.slowcheetah.org%3A14760'

    # magnet_regex_attribute_parser = MagnetRegexAttributeParser()
    # print(magnet_regex_attribute_parser.parse_hash(magnet_link))
    # print(magnet_regex_attribute_parser.parse_display_name(magnet_link))
    # print(magnet_regex_attribute_parser.parse_announce_list(magnet_link))

    torrent_file = './The.Marksman.2021.1080p.WEB-DL.DD5.1.H264-FGT-[rarbg.to].torrent'
    # magnet_reader = MagnetReader()
    # magnet_instance = magnet_reader.read_byte_from_file(magnet_file)
    # print(magnet_instance.display_name, magnet_instance.hash, magnet_instance.announce_list)

    # magnet_byte_attribute_reader = MagnetByteAttributeReader()
    # magnet_byte_attribute_reader.read_display_name(magnet_byte_content)

    magnet_builder = MagnetBuilder()
    magnet_instance = magnet_builder.build(magnet_link)
    print(magnet_instance)
    # print(magnet_instance.display_name, magnet_instance.hash, magnet_instance.announce_list)
