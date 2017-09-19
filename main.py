#!/usr/bin/env python

from torrentscrapper.webscrappers import RarbgScrapper as rs
from torrentscrapper.webscrappers import PirateBayScrapper as pbs
from torrentscrapper.webscrappers import KatScrapper as kats
from torrentscrapper.webscrappers import TvCalendarScrapper as tvcs
from torrentscrapper.utils.torcurl import TorPyCurl as tpc
from torrentscrapper import WebSearch as ws
from torrentscrapper import ScrapperEngine as se
from fake_useragent import UserAgent
import requests


def test():
    ss = ['a', 'b']
    if 'a' in ss:
        print 'TRUE'
def main():
    '''
    rarbg_file = open('/home/asigan/python-torrent-scrapper/examples/rarbgexample.html')
    piratebay_file = open('/home/asigan/python-torrent-scrapper/examples/thepiratebayexample.html')
    rarbg_magnet = open('/home/asigan/python-torrent-scrapper/examples/ttlkrarbg.html')
    piratebay_magnet = open('/home/asigan/python-torrent-scrapper/examples/gotTPB.html')

    '''

    raw_input('Press [ENTER] To Launch WebScrapping ... \n')
    scrapper_engine = se.ScrapperEngine()
    torrents = scrapper_engine.search(title='Rick and Morty', year=None, season='01', episode='06', quality='', subber=False)

    for torrent in torrents:
        torrent.list()
        print '\n'

    result = scrapper_engine.unifiy_torrent_table(torrents=torrents)
    scrapper_engine.calculate_top_spot(dataframe=result)

    # content = websearch(url= 'https://www.pogdesign.co.uk/cat/')
    # dataframe = tvcs.TvCalendarScrapper().webscrapper(content=content.text)
    # dataframe.to_csv('./montly_tvcalendar.csv', sep='\t', encoding='utf-8')
    return



if __name__ == '__main__':
    main()