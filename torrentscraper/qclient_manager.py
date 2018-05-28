#!/usr/bin/env python3

# TODO path to qClient config C:\Users\Asigan\AppData\Roaming\qBittorrent.ini

# Import External Libraries
from qbittorrent import Client


class QClientManager(object):
    def __init__(self, url='http://127.0.0.1:8080/', user='', passwd=''):
        self.name = self.__class__.__name__

        # Default Parameters for QClient Session
        self.defautl_url = url
        self.user = user
        self.passwd = passwd

        # Launching Session in QClient
        self.session = Client(self.defautl_url)
        if self.user != '' and self.passwd != '':
            self.session.login(self.user, self.passwd)

    def session_shutdown(self):
        try:
            self.session.shutdown()
        except Exception as e:
            print(e)
        return True

    def get_torrent_info(self):
        torrents = self.session.torrents()
        for torrent_item in torrents:
            print('%s: [%s] \n\t\t- %s' % (self.name, torrent_item['hash'], torrent_item['name']))


    def load_magnet(self, magnet_uri):
        try:
            self.session.download_from_link(magnet_uri)
        except Exception as e:
            print (e)
        return True

# qclient = QClientManager()
# qclient.session.set_category(torrents[0]['hash'], category='Anime')
# qclient.get_torrent_info()
