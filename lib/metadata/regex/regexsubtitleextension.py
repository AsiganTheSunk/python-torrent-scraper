import re

from torrentscraper.fileflags import FileFlags as fflags


class RegexSubtitleExtension():
    def __init__(self):
        self.name = 'RegexSubtitleExtension'
        self.supported_fflags = []
        self.supported_season_fflags = []
        self.supported_subtitle_fflags = [fflags.SUBTITLE_DIRECTORY_FILM_FLAG,
                                          fflags.SUBTITLE_FILM_FLAG,
                                          fflags.SUBTITLE_DIRECTORY_SHOW_FLAG,
                                          fflags.SUBTITLE_SHOW_FLAG,
                                          fflags.SUBTITLE_DIRECTORY_ANIME_FLAG,
                                          fflags.SUBTITLE_ANIME_FLAG]
        return

    def get_subtitles_directory(self, stream, debug=False):
        '''
        This function retrieves the subtitle_directory of the file or directory from the stream using regular expresions
        :param stream: It represents the input string you're parsing
        :param debug: It represents the debug status of the function, default it's False
        :return: SUBTITLE_DIRECTORY
        '''
        _subtitle_directory_patterns = ['(sub\w{0,6}(?!=\!))']
        try:
            subtitle_directory = re.search(_subtitle_directory_patterns[0], stream, re.IGNORECASE).group(0)
        except AttributeError:
            # raise error that would be corrected in ReEngine turning exception into blank field
            subtitle_directory = ''
            return subtitle_directory
        else:
            subtitle_directory = 'subs'
            if debug:
                print('{extension_engine}: {stream} :: {value}').format(
                    extension_engine=self.name,
                    stream=stream,
                    value=subtitle_directory)
            return subtitle_directory
