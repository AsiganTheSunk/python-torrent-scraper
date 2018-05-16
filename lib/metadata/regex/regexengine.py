import re

from lib.metadata.metadata import Metadata
from lib.metadata.regex.regexanimeextension import RegexAnimeExtension
from lib.metadata.regex.regexcommonextension import RegexCommonExtension
from lib.metadata.regex.regexfilmextension import RegexFilmExtension
from lib.metadata.regex.regexshowextension import RegexShowExtension
from lib.metadata.regex.regexsubtitleextension import RegexSubtitleExtension
from lib.fileflags import FileFlags as fflags


def compile_pattern(patterns):
    return [re.compile(pattern) for pattern in patterns]


class RegexEngine():
    def __init__(self):
        self.name = 'RegexEngine'
        self.supported_fflags = [fflags.FILM_FLAG, fflags.SHOW_FLAG,
                                 fflags.ANIME_FLAG,
                                 fflags.FILM_DIRECTORY_FLAG,
                                 fflags.SEASON_DIRECTORY_FLAG,
                                 fflags.ANIME_DIRECTORY_FLAG,
                                 fflags.SHOW_DIRECTORY_FLAG,
                                 fflags.SUBTITLE_DIRECTORY_FILM_FLAG,
                                 fflags.SUBTITLE_FILM_FLAG,
                                 fflags.SUBTITLE_DIRECTORY_SHOW_FLAG,
                                 fflags.SUBTITLE_SHOW_FLAG,
                                 fflags.SUBTITLE_DIRECTORY_ANIME_FLAG,
                                 fflags.SUBTITLE_ANIME_FLAG
                                 ]
        self.category_extension = [RegexFilmExtension(), RegexAnimeExtension(),
                                   RegexShowExtension()]
        self.common_extension = RegexCommonExtension()
        self.subtitle_extension = RegexSubtitleExtension()
        return

    def map(self, stream, fflag, verbose=False, debug=False):
        '''
        This function maps the file or directory based on the premapping done by filemapper
        :param stream: It represents the input string you're mapping
        :param fflag: It represents the fflag of the file or directory your mapping
        :param debug: It represents the debug status of the function, default it's False
        :param verbose: It represents the verbose status of the function, default it's False
        :return: Metadata
        '''
        name = season = episode = tags = year = quality = subs = \
            acodec = vcodec = uploader = source = ''

        print('STREAM: ', stream)
        for extension_engine in self.category_extension:
            # This will try to map the diferent values present in the file or directory basename

            if fflag in extension_engine.supported_fflags:
                try:
                    name = extension_engine.get_name(stream=stream, season_directory=False, debug=verbose)
                    episode = extension_engine.get_episode(stream=stream, debug=verbose)
                    season = extension_engine.get_season(stream=stream, debug=verbose)
                    year = extension_engine.get_year(stream=stream, debug=verbose)
                    tags = extension_engine.get_tags(stream=stream, debug=verbose)

                except AttributeError or Exception:
                    print('{0} Error: unable to parse argument ...'.format(self.name))
                    return
                else:
                    try:

                        quality = self.common_extension.get_quality(stream=stream, debug=verbose)
                        acodec = self.common_extension.get_acodec(stream=stream, debug=verbose)
                        vcodec = self.common_extension.get_vcodec(stream=stream, debug=verbose)
                        bit = self.common_extension.get_bit(stream, verbose)
                        channels = self.common_extension.get_channels(stream, verbose)
                        uploader = self.common_extension.get_uploader(stream=stream, debug=verbose)
                        source = self.common_extension.get_source(stream=stream, debug=verbose)
                        extension = self.common_extension.get_extension(stream=stream, debug=verbose)
                    except AttributeError or Exception:
                        # caputure errors!!!
                        print('Error Show Regex Engine')
                        return
                    else:
                        if debug:
                            print('{0} :: {1}::{2} ::\n name:{3} episode:{4}, season:{5}, year:{6}, tags:{7}, '
                                  'quality:{8}\n acodec:{9}, vcodec:{10}, uploader:{11} source:{12}, extension:{13}, channels:{14}, bit:{15}'.format(
                                self.name, fflag, stream, name, episode, season, year,
                                tags, quality, acodec, vcodec, source, uploader, extension, channels, bit))

                        return Metadata(name=name, episode=episode,
                                        season=season, year=year, film_tag=tags,
                                        quality=quality, acodec=acodec,
                                        vcodec=vcodec, source=source,
                                        uploader=uploader, fflag=fflag,
                                        extension=extension, channels=channels, bit=bit)

            elif fflag in extension_engine.supported_season_fflags:
                try:
                    name = extension_engine.get_name(stream=stream, season_directory=True, debug=verbose)
                    season = extension_engine.get_season(stream=stream, season_directory=True, debug=verbose)
                except AttributeError:
                    print(
                    '{extension_engine} Error: unable to parse argument ...'.format(
                        extension_engine=self.name))
                    return
                else:
                    try:
                        quality = self.common_extension.get_quality(
                            stream=stream, debug=verbose)
                    except AttributeError:
                        print('Error Subtitles Regex Engine')
                        return
                    else:
                        if debug:
                            print('{0} :: {1}::{2} :: name:{3} season:{4}, quality:{5}'.format(
                                self.name, fflag, stream, name, season, quality))

                        return Metadata(name=name, season=season,
                                        quality=quality, fflag=fflag)

            elif fflag in extension_engine.supported_subtitle_fflags:
                try:
                    name = extension_engine.get_name(stream=stream, season_directory=False, debug=verbose)
                    episode = extension_engine.get_episode(stream=stream, debug=verbose)
                    season = extension_engine.get_season(stream=stream, debug=verbose)
                    year = extension_engine.get_year(stream=stream, debug=verbose)
                    tags = extension_engine.get_tags(stream=stream, debug=verbose)

                except AttributeError:
                    print('{0} Error: unable to parse argument ...'.format(self.name))
                    return
                else:
                    try:
                        subs = self.subtitle_extension.get_subtitles_directory(stream=stream, debug=verbose)
                        language = self.common_extension.get_language(stream=stream, debug=verbose)
                        extension = self.common_extension.get_extension(stream=stream, debug=verbose)
                    except AttributeError:
                        # caputure errors!!!
                        return
                    else:
                        if debug:
                            print('{0} :: {1}::{2} ::\n name:{3} episode:{4}, season:{5},'
                                  ' year:{6} tags:{7}, language:{8}, subs:{9}, extension:{10}'.format(
                                self.name, fflag, stream, name, episode, season, year, tags, subs, language, extension))

                        return Metadata(name=name, episode=episode,
                                        season=season, year=year, film_tag=tags,
                                        subtitle=subs, fflag=fflag,
                                        language=language, extension=extension)
