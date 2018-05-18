#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from lib.fileflags import FileFlags as fflags
from lib.imdbfilmextension import IMDbExtension
from lib.tvdbshowextension import TVDbShowExtension
from lib.malanimeextension import MalAnimeExtension

class DescriptionDownloader():
    def __init__(self):
        self.name = self.__class__.__name__

    def get_info(self, fflag, title, language_index=0):
        info = ''
        if fflag == fflags.SHOW_DIRECTORY_FLAG:
            clean_title = title.replace(':', '')
            if self.check_chache(clean_title) is not True:
                show_extension = TVDbShowExtension()
                info = show_extension.get_show_info(title, language_index)
                self.save_in_cache(clean_title, info)
                return info
            else:
                return self.get_info_from_cache(clean_title)

        elif fflag == fflags.FILM_DIRECTORY_FLAG:
            clean_title = title.replace(':','')
            if self.check_chache(clean_title) is not True:
                film_extension = IMDbExtension()
                info = film_extension.get_movie_info(title, language_index)
                self.save_in_cache(clean_title, info)
                return info
            else:
                return self.get_info_from_cache(clean_title)

        elif fflag == fflags.ANIME_DIRECTORY_FLAG:
            clean_title = title.replace(':', '')
            if self.check_chache(clean_title) is not True:
                anime_extension = MalAnimeExtension()
                anime_extension.get_movie_info(title, language_index)

                self.save_in_cache(clean_title, info)
            else:
                return self.get_info_from_cache(clean_title)

    def check_chache(self, title):
        file_path = './cache/description_downloads/{0}-description.txt'.format(title)
        try:
            if os.path.isfile(file_path):
                print('Skipping This Step - DescriptionDownloader')
                return True
            else:
                return False
        except Exception as err:
            print('checkcache: ',err)

    def save_in_cache(self, title, info):
        try:
            file_path = './cache/description_downloads/{0}-description.txt'.format(title)
            with open(file_path, "w") as file:
                file.write(info)
        except Exception as err:
            print('savecache: ', err)

    def get_info_from_cache(self, title):
        info = ''
        try:
            file_path = './cache/description_downloads/{0}-description.txt'.format(title)
            with open(file_path, "r+") as file:
                info = file.read()
            return info
        except Exception as err:
            print('getcache: ', err)