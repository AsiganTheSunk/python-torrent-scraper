#!/usr/bin/env python

from torrentscraper import scraper_engine as se
from torrentscraper.datastruct.websearch_instance import WebSearchInstance

# content = websearch(url= 'https://www.pogdesign.co.uk/cat/')
# dataframe = tvcs.TvCalendarScrapper().webscrapper(content=content.text)
# dataframe.to_csv('./montly_tvcalendar.csv', sep='\t', encoding='utf-8')

def main():
    websearch = WebSearchInstance(title='Rick & Morty', year='', season='03', episode='08', quality='HDTV', header='', search_type='SHOW')
    scraper_engine = se.ScraperEngine()
    p2p_instance_list = scraper_engine.search(websearch)
    dataframe = scraper_engine.create_magnet_dataframe(p2p_instance_list)
    dataframe = scraper_engine.unique_magnet_dataframe(dataframe)
    dataframe = scraper_engine.get_dataframe(dataframe, 5)

if __name__ == '__main__':
    main()
