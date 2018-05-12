# from filemapper.metadata.regex.RegexEngine import compile_pattern
import re

from lib.sbuilder.stringutils import StringUtils
from torrentscraper.fileflags import FileFlags as fflags


def compile_pattern(patterns):
    return [re.compile(pattern) for pattern in patterns]


class RegexFilmExtension():
    def __init__(self):
        self.name = 'RegexFilmExtension'
        self.supported_fflags = [fflags.FILM_DIRECTORY_FLAG, fflags.FILM_FLAG]
        self.supported_season_fflags = []
        self.supported_subtitle_fflags = [fflags.SUBTITLE_DIRECTORY_FILM_FLAG,
                                          fflags.SUBTITLE_FILM_FLAG]
        return

    def get_name(self, stream, season_directory=False, debug=False):
        '''
        This function retrieves the name of the film from the stream using regular expresions
        :param stream: It represents the input string you're parsing
        :param debug: It represents the debug status of the function, default it's False
        :return: NAME
        '''
        _tail_patterns = ['((\(?)([1-2])([890])(\d{2})(\))?)(?!p)']
        _name_patterns = ['(.*)(([1-2])([890])(\d{2})(\))?)(?!p)']
        try:
            tail = re.search(_tail_patterns[0], stream).group(0)
            name = re.search(_name_patterns[0], stream).group(0)[:-(len(tail))]
        except AttributeError:
            # raise error that would be corrected in ReEngine turning exception into blank field
            name = ''
            return name
        else:
            name = StringBuilder().prettify_stream(name)
            if debug:
                print('{extension_engine}: {stream} :: name:{value}').format(
                    extension_engine=self.name,
                    stream=stream,
                    value=name)
            return name

    def get_episode(self, stream, debug=False):
        return ''

    def get_season(self, stream, season_directory=False, debug=False):
        return ''

    def get_year(self, stream, debug=False):
        '''
        This function retrieves the tags of the film from the stream using regular expresions
        :param stream: It represents the input string you're parsing
        :param debug: It represents the debug status of the function, default it's False
        :return: YEAR
        '''
        _year_patterns = ['(([1-2])([890])(\d{2}))(?!p)']
        try:
            year = re.search(_year_patterns[0], stream).group(0)
        except AttributeError:
            # raise error that would be corrected in ReEngine turning exception into blank field
            year = ''
            return year
        else:
            if debug:
                print('{extension_engine}: {stream} :: year:{value}').format(
                    extension_engine=self.name,
                    stream=stream,
                    value=year)
            return str(year)

    def get_tags(self, stream, debug=False):
        '''
        This function retrieves the tags of the film from the stream using regular expresions
        :param stream: It represents the input string you're parsing
        :param debug: It represents the debug status of the function, default it's False
        :return: TAGS
        '''
        _film_tag_patterns = ['EXTENDED(.*)?CUT|REMASTERED']
        try:
            film_tag = re.search(_film_tag_patterns[0], stream, re.IGNORECASE).group(0)
        except AttributeError:
            # raise error that would be corrected in ReEngine turning exception into blank field
            film_tag = ''
            return film_tag
        else:
            film_tag = StringBuilder().prettify_stream(film_tag, title=False)
            if debug:
                print('{extension_engine}: {stream} :: tags:{tag}').format(
                    extension_engine=self.name,
                    stream=stream,
                    tag=film_tag)
            return film_tag
