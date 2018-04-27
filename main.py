#!/usr/bin/env python

from torrentscraper import scraper_engine as se
import logging
# content = websearch(url= 'https://www.pogdesign.co.uk/cat/')
# dataframe = tvcs.TvCalendarScrapper().webscrapper(content=content.text)
# dataframe.to_csv('./montly_tvcalendar.csv', sep='\t', encoding='utf-8')

# rarbg_file = open('/home/asigan/python-torrent-scrapper/examples/rarbgexample.html')
# piratebay_file = open('/home/asigan/python-torrent-scrapper/examples/thepiratebayexample.html')
# rarbg_magnet = open('/home/asigan/python-torrent-scrapper/examples/ttlkrarbg.html')
# piratebay_magnet = open('/home/asigan/python-torrent-scrapper/examples/gotTPB.html')

def main():


    scraper_engine = se.ScrapperEngine()
    p2p_instance_list = scraper_engine.search(title='Rick & Morty', year='', season='03', episode='01', quality='1080p', header='', search_type='SHOW')
    dataframe = scraper_engine.create_magnet_dataframe(p2p_instance_list)
    dataframe = scraper_engine.unique_magnet_dataframe(dataframe)
    dataframe = scraper_engine.get_dataframe(dataframe, 5, True)

if __name__ == '__main__':
    main()
