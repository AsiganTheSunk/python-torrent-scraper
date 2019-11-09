from lib.sbuilder.stringutils import StringUtils
from lib.fileflags import FileFlags as fflags


EMPTY_WRAP = -1
BRACKET_WRAP = 0
PARENTHESIS_WRAP = 1
DASH_PARENTHESIS_WRAP = 2
EXTENSION_WRAP = 3
DASH_EMPTY_WRAP = 4
NONE_WRAP = 5


class StringShowExtension():
    def __init__(self):
        self.name = 'ShowExtension'
        self.supported_fflags = [fflags.SHOW_DIRECTORY_FLAG, fflags.SHOW_FLAG]
        self.supported_season_fflags = [fflags.SEASON_DIRECTORY_FLAG]
        self.supported_subtitle_fflags = [fflags.SUBTITLE_DIRECTORY_SHOW_FLAG,
                                          fflags.SUBTITLE_SHOW_FLAG]
        self.string_utils = StringUtils()
        return

    '''
        ShowExtension:
            This section of the code contains the following functions

            build_show_name:
            build_show_subtitle_name:
            build_show_season_name:
    '''

    def build_name(self, name, year, season, episode, ename, quality, extension, film_tag, debug=False):
        '''
        This function builds a show name directory
        :param name: It represents the title of the show you'regex rebuilding to proper match the standard
        :param season: It represents the season of the show you'regex rebuilding to proper match the standard
        :param episode: It represents the episode of the show you'regex rebuilding to proper match the standard
        :param ename: It represents the name of the episode of the show you'regex rebuilding to proper match the standard
        :param quality: It represents the resolution of the show you'regex rebuilding to proper match the standard
        :param extension: It represents the webscrapers of the file containing the show
        :param debug: It represents the debug status of the function, default it's False
        :return: SHOW_NAME
        '''
        try:
            SHOW_NAME = (
            '{name}{season}{episode}{ename}{quality}{webscrapers}').format(
                name=self.string_utils.eval_wrapped_key(value=name, wrap_type=NONE_WRAP),
                season=self.string_utils.eval_wrapped_key(value=('S' + season), wrap_type=EMPTY_WRAP),
                episode=self.string_utils.eval_wrapped_key(value=('E' + episode), wrap_type=NONE_WRAP),
                ename=self.string_utils.eval_wrapped_key(value=ename, wrap_type=DASH_EMPTY_WRAP),
                quality=self.string_utils.eval_wrapped_key(value=quality, wrap_type=BRACKET_WRAP),
                extension=self.string_utils.eval_wrapped_key(value=extension, wrap_type=EXTENSION_WRAP))

            if debug:
                print ('{engine}: {name}').format(engine=self.name, name=SHOW_NAME)

            return SHOW_NAME

        except Exception as e:
            print(e)

    def build_subtitle_name(self, name, year, season, episode, subtitle, language, extension, debug=False):
        '''
        This function builds a subs name for file or directory
        :param name: It represents the title of the show you'regex rebuilding to proper match the standard
        :param season: It represents the season of the show you'regex rebuilding to proper match the standard
        :param episode: It represents the episode of the show you'regex rebuilding to proper match the standard
        :param subtitle: It represents the subs tag
        :param language: It represents the language of the show
        :param extension: It represents the webscrapers of the file containing the show
        :param debug: It represents the debug status of the function, default it's False
        :return: SUBTITLE_NAME
        '''
        try:
            SUBTITLE_NAME = (
            '{name}{season}{episode}{subtitle}{language}{webscrapers}').format(
                name=self.string_utils.eval_wrapped_key(value=name, wrap_type=NONE_WRAP),
                season=self.string_utils.eval_wrapped_key(value=('S' + season), wrap_type=EMPTY_WRAP),
                episode=self.string_utils.eval_wrapped_key(value=('E' + episode), wrap_type=NONE_WRAP),
                subtitle=self.string_utils.eval_wrapped_key(value=subtitle, wrap_type=PARENTHESIS_WRAP),
                language=self.string_utils.eval_wrapped_key(value=language, wrap_type=DASH_PARENTHESIS_WRAP),
                extension=self.string_utils.eval_wrapped_key(value=extension, wrap_type=EXTENSION_WRAP))

            if debug:
                print ('{engine}: {name}').format(engine=self.name,
                                                  name=SUBTITLE_NAME)

            return SUBTITLE_NAME

        except Exception as e:
            print(e)

    def build_season_name(self, name, season, debug=False):
        '''
        This function builds a season name for directory
        :param name: It represents the title of the show you'regex rebuilding to proper match the standard
        :param season: It represents the season of the show you'regex rebuilding to proper match the standard
        :param debug: It represents the debug status of the function, default it's False
        :return: SEASON_NAME
        '''
        try:
            SEASON_NAME = ('{name}{season}').format(
                name=self.string_utils.eval_wrapped_key(value=name, wrap_type=NONE_WRAP),
                season=self.string_utils.eval_wrapped_key(value=('Season ' + str(int(season))), wrap_type=BRACKET_WRAP)
            )

            if debug:
                print ('{engine}: {name}').format(engine=self.name, name=SEASON_NAME)

            return SEASON_NAME
        except Exception as e:
            print(e)
