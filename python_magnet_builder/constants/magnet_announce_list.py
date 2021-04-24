from python_magnet_builder.constants.magnet_announce_type import MagnetAnnounceType

ANNOUNCE_LIST = {
    MagnetAnnounceType.HTTPS: 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_https.txt',
    MagnetAnnounceType.HTTP: 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_http.txt',
    MagnetAnnounceType.UDP: 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_udp.txt',
    MagnetAnnounceType.IP: 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_ip.txt',
    MagnetAnnounceType.ALL: 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt',
    MagnetAnnounceType.BLACKLIST: 'https://raw.githubusercontent.com/ngosang/trackerslist/master/blacklist.txt'
}