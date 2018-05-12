import re

from lib.sbuilder.stringbuilder import StringBuilder
from lib.sbuilder.stringutils import StringUtils
from torrentscraper.fileflags import FileFlags as fflags


def compile_pattern(patterns):
    return [re.compile(pattern) for pattern in patterns]


class RegexShowExtension():
    def __init__(self):
        self.name = 'RegexShowExtension'
        self.supported_fflags = [fflags.SHOW_DIRECTORY_FLAG, fflags.SHOW_FLAG]
        self.supported_season_fflags = [fflags.SEASON_DIRECTORY_FLAG]
        self.supported_subtitle_fflags = [fflags.SUBTITLE_DIRECTORY_SHOW_FLAG,
                                          fflags.SUBTITLE_SHOW_FLAG]
        return

    def get_name(self, stream, season_directory=False, debug=False):
        '''
        This function retrieves the name of the show from the stream using regular expresions
        :param stream: It represents the input string you're parsing
        :param season_directory: --, default value it's False
        :param debug: It represents the debug status of the function, default it's False
        :return: NAME
        '''
        _name_patterns = ['(.*)(\(|\[)?s(eason)?(\-|\s|\.)?(\d{1,2})(\)|\])?',
                          '(.*)([s]\d{1,2})']
        _tail_patterns = ['(\(|\[)?s(eason)?(\-|\s|\.)?(\d{1,2})(\)|\])?',
                          r'([s]\d{1,2})']
        try:
            if season_directory:
                tail = re.search(_tail_patterns[0], stream, re.IGNORECASE).group(0)
                name = re.search(_name_patterns[0], stream, re.IGNORECASE).group(0)[:-len(tail)]
            else:
                tail = re.search(_tail_patterns[1], stream, re.IGNORECASE).group(0)
                name = re.search(_name_patterns[1], stream, re.IGNORECASE).group(0)[:-len(tail)]
        except AttributeError:
            # raise error that would be corrected in ReEngine turning exception into blank field
            name = ''
            return name
        else:
            name = StringBuilder().prettify_stream(name)
            if debug:
                print('{0}: {1} :: name:{2}'.format(self.name, stream, name))

            return name

    def get_episode(self, stream, debug=False):
        '''
        This function retrieves the episode of the show from the stream using regular expresions
        :param stream: It represents the input string you're parsing
        :param debug: It represents the debug status of the function, default it's False
        :return: EPISODE
        '''
        _episode_pattern = ['([e])\d{2,3}']
        try:
            episode = re.search(_episode_pattern[0], stream, re.IGNORECASE).group(0)
        except AttributeError:
            # raise error that would be corrected in ReEngine turning exception into blank field
            episode = ''
            return episode
        else:
            episode = episode[1:]
            if debug:
                print('{0}: {1} :: episode:{2}'.format(self.name, stream, episode))
            return str(episode)

    def get_season(self, stream, season_directory=False, debug=False):
        '''
        This function retrieves the season of the show from the stream using regular expresions
        :param stream: It represents the input string you're parsing
        :param season_directory: --, default value it's False
        :param debug: It represents the debug status of the function, default it's False
        :return: SEASON
        '''
        _season_patterns = ['\d{1,2}', '([s]\d{2})']
        _season_directory_patterns = [
            '(\(|\[)?s(eason)?(\-|\s|\.)?(\d{1,2})(\)|\])?']
        try:
            if season_directory:
                season_directory = re.search(_season_directory_patterns[0], stream, re.IGNORECASE).group(0)
                season = re.search(_season_patterns[0], season_directory, re.IGNORECASE).group(0)
                season = str(int(season))
            else:
                season = re.search(_season_patterns[1], stream, re.IGNORECASE).group(0)
                season = season[1:]

        except AttributeError:
            season = ''
            return season
        else:

            if debug:
                print('{0}: {1} :: season:{2}'.format(self.name, stream, season))
            return str(season)

    def get_year(self, stream, debug=False):
        return ''

    def get_tags(self, stream, debug=False):
        return ''
