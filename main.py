#!/usr/bin/env python

from torrentscrapper.webscrappers import RarbgScrapper as rs
from torrentscrapper.webscrappers import PirateBayScrapper as pbs
from torrentscrapper.utils.torcurl import TorPyCurl as tpc
from torrentscrapper import ScrapperEngine as se

import requests
from fake_useragent import UserAgent

def main():
    '''


    rarbg_file = open('/home/asigan/python-torrent-scrapper/examples/rarbgexample.html')
    piratebay_file = open('/home/asigan/python-torrent-scrapper/examples/thepiratebayexample.html')
    rarbg_magnet = open('/home/asigan/python-torrent-scrapper/examples/ttlkrarbg.html')
    piratebay_magnet = open('/home/asigan/python-torrent-scrapper/examples/gotTPB.html')

    '''

    raw_input('Press [ENTER] To Launch WebScrapping... \n')
    scrapper_engine = se.ScrapperEngine()
    print '[Film ]'
    torrents = scrapper_engine.search(quality='1080p', title='Baywatch', year='2017', season=None, episode=None, subber=False)
    for torrent in torrents:
        torrent.list()
        print '\n'
        scrapper_engine.create_data_frame(torrent=torrent)



    scrapper_engine.unify_torrent_table(torrents[0],torrents[1])

    return

def websearch (url):
    headers = {'UserAgent':str(UserAgent().random)}
    try:
        r = requests.get (url, verify=True, headers=headers)
        return r
    except Exception as e:
        print 'Unable to stablish connection'
    finally:
        if r.status_code == 200:
            print '200 OK'


if __name__ == '__main__':
    main()