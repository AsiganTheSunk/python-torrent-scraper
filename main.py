#!/usr/bin/env python

# content = websearch(url= 'https://www.pogdesign.co.uk/cat/')
# dataframe = tvcs.TvCalendarScrapper().webscrapper(content=content.text)
# dataframe.to_csv('./montly_tvcalendar.csv', sep='\t', encoding='utf-8')

from interface.torrent_scraper_interface import run_interface

def main():
    run_interface()

if __name__ == '__main__':
    main()


