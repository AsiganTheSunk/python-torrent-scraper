#!/usr/bin/env python

from torrent_scraper_interface import run_interface
from lib.cover_downloader import CoverDownloader
from torrentscraper.datastruct.websearch_instance import WebSearchInstance

def main():
    # cv = CoverDownloader()
    # ws = WebSearchInstance(title='Marvel Avengers', year='2012', quality='1080p', search_type='FILM')
    # cv.download(ws)

    run_interface()

    # ws = WebSearchInstance(title='Avengers', year='2012', quality='1080p', search_type='FILM')
    # ts = TorrentScraper()
    # ts.scrap(ws)

    # tvdb = TVDbShowExtension()
    # print(tvdb.get_year('Scrubs'))
    # print(tvdb.get_runtime('Scrubs'))
    # print(tvdb.get_description('Scrubs'))

    # from Pymoe import Anilist
    # instance = Anilist()
    # result = instance.search.anime("Fullmetal Alchemist: Brotherhood")
    # print(result['data'])
    # # print(result['data']['Page']['averageScore'])
    # id = result['data']['Page']['media'][0]['id']
    #
    # result = instance.get.anime(5114)
    # print(result)
    # year = result['data']['Media']['startDate']['year']
    # episodes = result['data']['Media']['episodes']
    # description = result['data']['Media']['description']
    # rating = result['data']['Media']['averageScore']
    # print(year)
    # print(episodes)
    # print(description)
    # print(rating)
    #
    # print('staff', instance.get.staff(5114))
    #
    # import myanimelist.session
    # session = myanimelist.session.Session()
    # # Return an anime object corresponding to an ID of 1. IDs must be natural numbers.
    # data = session.anime(5114)
    # print(data)
    # for character in data.characters:
    #     print(character.name, '---', data.characters[character]['role'])

if __name__ == '__main__':
    main()


