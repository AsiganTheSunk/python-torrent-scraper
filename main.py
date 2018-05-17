#!/usr/bin/env python

from torrent_scraper_interface import run_interface
from lib.cover_downloader import CoverDownloader
from torrentscraper.datastruct.websearch_instance import WebSearchInstance
from tkinter import *
from vertical_list_box import SimpleVerticalListBox

from configparser import ConfigParser

def ConfigSectionMap(section):
    Config = ConfigParser()
    Config.read('./scraperengine.ini')
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None

    return dict1

def main():
    run_interface()

    # cv = CoverDownloader()
    # ws = WebSearchInstance(title='Marvel Avengers', year='2012', quality='1080p', search_type='FILM')
    # cv.download(ws)

    # root = Tk()
    # vlb = SimpleVerticalListBox(root, [' [ ScraperEngine ]', ' [ Qbittorrent ]',  ' [ About ]'])
    # vlb.configure(borderwidth=1, highlightbackground='white', bg='#DCDCDC', relief='groove')
    # vlb.grid(row=0, column=0)
    #
    # root.mainloop()


if __name__ == '__main__':
    main()

# TODO
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