#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import listdir, remove, makedirs
from os.path import isfile, join, isdir, exists
from shutil import rmtree

from lib.fileflags import FileFlags as fflags
from lib.imdbfilmextension import IMDbExtension
from lib.tvdbshowextension import TVDbShowExtension
from lib.malanimeextension import MalAnimeExtension

class DescriptionDownloader():
    def __init__(self):
        self.name = self.__class__.__name__
        self.location = './cache/description_downloads/'
        if not exists(self.location):
            makedirs(self.location)

    def get_info(self, fflag, title):
        try:
            info = ''
            if fflag == fflags.SHOW_DIRECTORY_FLAG:
                clean_title = title.replace(':', '')
                if self.check_chache(clean_title) is not True:
                    show_extension = TVDbShowExtension()
                    info = show_extension.get_show_info(title)
                    self.save_in_cache(clean_title, info)
                    return info
                else:
                    return self.get_info_from_cache(clean_title)

            elif fflag == fflags.FILM_DIRECTORY_FLAG:
                clean_title = title.replace(':','')
                if self.check_chache(clean_title) is not True:
                    film_extension = IMDbExtension()
                    info = film_extension.get_movie_info(title)
                    self.save_in_cache(clean_title, info)
                    return info
                else:
                    return self.get_info_from_cache(clean_title)

            elif fflag == fflags.ANIME_DIRECTORY_FLAG:
                clean_title = title.replace(':', '')
                if self.check_chache(clean_title) is not True:
                    anime_extension = MalAnimeExtension()
                    info = anime_extension.get_anime_info(title)
                    self.save_in_cache(clean_title, info)
                    return info
                else:
                    return self.get_info_from_cache(clean_title)
        except Exception as err:
            print('Description Downloader: Error - ', err)

    def check_chache(self, title):
        file_path = self.location + '{0}-description.txt'.format(title)
        try:
            if isfile(file_path):
                print(self.name, 'Skipping This Step: File Already in Cache')
                return True
            else:
                return False
        except Exception as err:
            print('checkcache: ',err)

    def save_in_cache(self, title, info):
        try:
            file_path = self.location + '{0}-description.txt'.format(title)
            with open(file_path, "w") as file:
                file.write(info)
        except Exception as err:
            print(self.name, 'Save Cache Error: ', err)

    def get_info_from_cache(self, title):
        info = ''
        try:
            file_path = self.location + '{0}-description.txt'.format(title)
            with open(file_path, "r+") as file:
                info = file.read()
            return info
        except Exception as err:
            print(self.name, 'Get Cache Error: ', err)

    def clear_cache(self):
        try:
            if isdir(self.location):
                rmtree(self.location)
        except Exception as err:
            print(self.name, 'Clear Cache Error: ', err)