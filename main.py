#!/usr/bin/env python

import urllib.parse
from torrentscraper import scraper_engine as se
from torrentscraper.webscrapers.utils.magnet_builder import MagnetBuilder
import pandas as pd
import numpy as np
from pandas import DataFrame

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

# content = websearch(url= 'https://www.pogdesign.co.uk/cat/')
# dataframe = tvcs.TvCalendarScrapper().webscrapper(content=content.text)
# dataframe.to_csv('./montly_tvcalendar.csv', sep='\t', encoding='utf-8')

def main():
    '''
    rarbg_file = open('/home/asigan/python-torrent-scrapper/examples/rarbgexample.html')
    piratebay_file = open('/home/asigan/python-torrent-scrapper/examples/thepiratebayexample.html')
    rarbg_magnet = open('/home/asigan/python-torrent-scrapper/examples/ttlkrarbg.html')
    piratebay_magnet = open('/home/asigan/python-torrent-scrapper/examples/gotTPB.html')

    '''

    scrapper_engine = se.ScrapperEngine()
    p2p_instance_list = scrapper_engine.search(title='Rick & Morty', year='', season='03', episode='01', quality='1080p', header='', search_type='SHOW')
    p2p0 = p2p_instance_list[0].magnet_instance_list
    #p2p1 = p2p_instance_list[1].magnet_instance_list
    #p2p2 = p2p_instance_list[2].magnet_instance_list

    dataframe = DataFrame()
    for item_list in p2p_instance_list:
        for item in item_list.magnet_instance_list:
            new_row = {'name':[item['display_name']],
                       'hash':[item['hash']],
                       'size':[item['size']],
                       'seed':[item['seed']],
                       'leech':[item['leech']],
                       'ratio':[item['ratio']],
                       'magnet':[item['magnet']]}

            new_row_df = DataFrame(new_row, columns=['name', 'hash', 'size', 'seed', 'leech', 'ratio', 'magnet'])
            dataframe = dataframe.append(new_row_df, ignore_index=True)
    print(dataframe)

    mbuilder = MagnetBuilder()
    cmmn_hash = dataframe.groupby(['hash'])
    for item_hash in cmmn_hash.groups:
        if len(cmmn_hash.get_group(item_hash)) > 1:
            #TODO REPENSAR ESTO, estoy espeso. 5:04
            aux_index = cmmn_hash.get_group(item_hash).index.tolist()[0]
            tmp_magnet = dataframe.iloc[aux_index]['magnet']
            aux_magnet_instance = mbuilder.parse_from_magnet(tmp_magnet)
            aux_magnet_instance['status']
            for instance_index in cmmn_hash.get_group(item_hash).index.tolist()[1:]:
                tmp_magnet = dataframe.iloc[int(instance_index)]['magnet']
                #print(urllib.parse.unquote(tmp_magnet))
                magnet_instance = mbuilder.parse_from_magnet(tmp_magnet)
                #print(magnet_instance['display_name'])
                #TODO hacer el unquote? en caso de que el primer metodo de extraccion falle.

                #print(dataframe.iloc[int(instance_index)]['magnet'])
                print('..............................' * 3)
                aux_magnet_instance = mbuilder.merge_announce_list(magnet_instance, aux_magnet_instance)
                aux_magnet_instance['status']
        print(cmmn_hash.get_group(item_hash))
        print('___________________' * 3)


    # for item in p2p0:
    #     print(item['display_name'], 'Hash: ', item['hash'], item['activity']['seed'],  item['activity']['leech'])
    #     item['status']
    # for item in p2p1:
    #     print(item['display_name'], 'Hash: ', item['hash'], item['activity']['seed'], item['activity']['leech'])
    #     item['status']
    # for item in p2p2:
    #     print(item['display_name'], 'Hash: ', item['hash'], item['activity']['seed'], item['activity']['leech'])
    #     item['status']

    return



if __name__ == '__main__':
    #test3()
    main()
    #retrieve_cloudflare_cookie(uri='https://unblockedbay.info/s/?q=Rick++Morty++S02E01+1080p&category=205&page=0&orderby=99', debug=True)
    #test()