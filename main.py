#!/usr/bin/env python

from torrentscraper import scraper_engine as se


# def test():
#     webscraper = pbs.PirateBayScraper()
#     websearch = ws.WebSearch(title='Rick & Morty',season='02',episode='01',quality='1080p', debug=True)
#     uri_builder = UriBuilder()
#     uri_builder.build_request_url(websearch, webscraper, verbose=True)
#
#     print(webscraper.main_page)
#     webscraper.update_main_page()
#     print(webscraper.main_page)
#     webscraper.update_main_page()
#     print(webscraper.main_page)
#     webscraper.update_main_page()
#     print(webscraper.main_page)
#
#     return

def main():
    '''
    rarbg_file = open('/home/asigan/python-torrent-scrapper/examples/rarbgexample.html')
    piratebay_file = open('/home/asigan/python-torrent-scrapper/examples/thepiratebayexample.html')
    rarbg_magnet = open('/home/asigan/python-torrent-scrapper/examples/ttlkrarbg.html')
    piratebay_magnet = open('/home/asigan/python-torrent-scrapper/examples/gotTPB.html')

    '''
    print('******' * 11)
    input('Press [ENTER] To Launch WebScrapping ...')
    print('******' * 11)
    scrapper_engine = se.ScrapperEngine()
    torrents = scrapper_engine.search(title='Rick & Morty', year='', season='03', episode='01', quality='1080p', header='', search_type='SHOW')

    # for torrent in torrents:
    #     torrent.list()
    #     print('\n')

    result = scrapper_engine.unifiy_torrent_table(torrents=torrents)
    scrapper_engine.calculate_top_spot(dataframe=result)

    # content = websearch(url= 'https://www.pogdesign.co.uk/cat/')
    # dataframe = tvcs.TvCalendarScrapper().webscrapper(content=content.text)
    # dataframe.to_csv('./montly_tvcalendar.csv', sep='\t', encoding='utf-8')
    return



if __name__ == '__main__':
    #test3()
    main()
    #retrieve_cloudflare_cookie(uri='https://unblockedbay.info/s/?q=Rick++Morty++S02E01+1080p&category=205&page=0&orderby=99', debug=True)
    #test()