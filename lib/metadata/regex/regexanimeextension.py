import re

#from config import TRUSTED_UPLOADERS
from lib.sbuilder.stringbuilder import StringBuilder
from lib.fileflags import FileFlags as fflags


class RegexAnimeExtension():
    def __init__(self):
        self.name = 'RegexAnimeExtension'
        self.supported_fflags = [fflags.ANIME_DIRECTORY_FLAG, fflags.ANIME_FLAG]
        self.supported_season_fflags = []
        self.supported_subtitle_fflags = [fflags.SUBTITLE_DIRECTORY_ANIME_FLAG,
                                          fflags.SUBTITLE_ANIME_FLAG]
        return

    def get_name(self, stream, season_directory=False, debug=False):
        '''
        This function retrieves the name of the anime from the stream using regular expresions
        :param stream: It represents the input string you're parsing
        :param debug: It represents the debug status of the function, default it's False
        :return: NAME
        '''
        _uploader_patterns = []
        _core_patterns = ['E(pisode)(\-|\.|\s)?(\d{2,3})']
        _tail_patterns = ['\[(\w+.*?)\s(\-|x)',
                          '\[(\w+.*?)E(pisode)?(x|\-|\.|\s)?(\d{2,3})']
        try:
            header = len(
                re.search(_uploader_patterns[0], stream, re.IGNORECASE).group(0)) + 1
            tail = re.search(_tail_patterns[0], stream, re.IGNORECASE).group(0)

        except AttributeError:
            try:
                header = len(re.search(_uploader_patterns[0], stream, re.IGNORECASE).group(0)) + 1
                core = len(re.search(_core_patterns[0], stream, re.IGNORECASE).group(0))
                tail = re.search(_tail_patterns[1], stream, re.IGNORECASE).group(0)
            except AttributeError:
                # raise error that would be corrected in ReEngine turning exception into blank field
                name = ''
                return name
            else:
                name = StringBuilder().prettify_stream(tail[header:-core])
                if debug:
                    print(
                    '{extension_engine}: {stream} :: name:{value}').format(
                        extension_engine=self.name,
                        stream=stream,
                        value=name)

                return name
        else:
            name = tail[header:-2]
            if debug:
                print('{extension_engine}: {stream} :: name:{value}').format(
                    extension_engine=self.name,
                    stream=stream,
                    value=name)
            return StringBuilder().prettify_stream(name)

    def get_episode(self, stream, debug=False):
        '''
        This function retrieves the episode of the anime from the stream using regular expresions
        :param stream: It represents the input string you're parsing
        :param debug: It represents the debug status of the function, default it's False
        :return: EPISODE
        '''
        _episode_patterns = ['\-.?\d{1,3}', 'Episode(\-|\s|\.)?(\d{1,3})',
                             '(x|E)(\d{1,3})']
        try:
            episode = re.search(_episode_patterns[0], stream, re.IGNORECASE).group(0)
        except AttributeError:
            try:
                episode = re.search(_episode_patterns[1], stream, re.IGNORECASE).group(0)
            except AttributeError:
                try:
                    episode = re.search(_episode_patterns[2], stream, re.IGNORECASE).group(0)
                except AttributeError:
                    # raise error that would be corrected in ReEngine turning exception into blank field
                    episode = ''
                    return episode
                else:
                    episode = episode[1:]
                    if debug:
                        print(
                        '{extension_engine}: {stream} :: episode:{value}').format(
                            extension_engine=self.name,
                            stream=stream,
                            value=episode)
                    return episode
            else:
                episode = episode[8:]
                if debug:
                    print(
                    '{extension_engine}: {stream} :: episode:{value}').format(
                        extension_engine=self.name,
                        stream=stream,
                        value=episode)
                return episode
        else:
            episode = episode[2:]
            if debug:
                print('{extension_engine}: {stream} :: episode:{value}').format(
                    extension_engine=self.name,
                    stream=stream,
                    value=episode)
            return str(episode)

    def get_season(self, stream, season_directory=False, debug=False):
        return ''

    def get_year(self, stream, debug=False):
        return ''

    def get_tags(self, stream, debug=False):
        return ''
