#!/usr/bin/env python

# path to qClient config C:\Users\Asigan\AppData\Roaming\qBittorrent.ini
# search values, to change and auto configurate. nº of conexions etc etc

from qbittorrent import Client
from time import sleep

class QClientManager(object):
    def __init__(self, url='http://127.0.0.1:8080/', user='admin', paswd='test'):
        self.name = self.__class__.__name__
        self.url = url
        self.user = user
        self.paswd = paswd

        # Launching Session to QClient
        self.session = Client(self.url)
        self.session.login(self.user, self.paswd)

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


    def load_magnet(self, magnet_uri, savepath, category):
        try:
            self.session.download_from_link(link=magnet_uri)#, savepath=savepath, category=category)
        except Exception as e:
            print (e)
        return True


def main():
    qclient = QClientManager()
    #qclient.session.set_category(torrents[0]['hash'], category='Anime')
    qclient.get_torrent_info()

if __name__ == '__main__':
    main()
