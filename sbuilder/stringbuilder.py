from metadata.metadata import Metadata
from sbuilder.stringanimeextension import StringAnimeExtension
from sbuilder.stringfilmextension import StringFilmExtension
from sbuilder.stringshowextension import StringShowExtension
from torrentscraper.fileflags import FileFlags as fflags

EMPTY_WRAP = -1
BRACKET_WRAP = 0
PARENTHESIS_WRAP = 1
DASH_PARENTHESIS_WRAP = 2
EXTENSION_WRAP = 3


def eval_wrapped_key(value, wrap_type):
    '''
    This function peform auxiliary help to the build name functions validating the content of the string
    :param value: It represents the key you'regex testing
    :param wrap_type: It represents the type of wrapping the string it's going to get, numbers 0 to 2, being
                    0 for [value], 1 for (value), 2 for -(value) 3 value
    :return: modified value
    '''
    if value is None:
        return ''
    else:
        if wrap_type is 0:
            return ('[' + value + ']')
        elif wrap_type is 1:
            return ('(' + value + ')')
        elif wrap_type is 2:
            return (' - (' + value + ')')
        elif wrap_type is 3:
            return ('.' + value)
        else:
            return value


class StringBuilder():
    def __init__(self):
        self.extension_engines = [StringAnimeExtension(), StringShowExtension(),
                                  StringFilmExtension()]
        return

    # ADD DUMMY FLAGS FUNCTIONS! to try to remap properly
    def prettify_stream(self, stream, title=True):
        '''
        This function makes a stream look pretty, removing dots, dashes and spaces
        :param stream: It represents the input string of the function
        :return: PRETTY_STREAM
        '''
        try:
            if title:
                new_stream = stream.replace('-', ' ').replace('.', ' ').replace('_', ' ').rstrip().title()
            else:
                new_stream = stream.replace('-', ' ').replace('.', ' ').replace('_', ' ').rstrip()
        except Exception as e:
            return stream
        else:
            return new_stream

    '''
        GENERAL FUNCTIONS:
            This section of the code contains the following functions

            build_name:
    '''

    def rebuild_name(self, metadata=Metadata(), debug=False):
        '''
        This function rebuilds the name of a show|movie|anime from a given class Metadata Object
        :param metadata: It represents the metadata gathered from the MetadataEngine
        :param debug: It represents the debug status of the function, default it's False
        :return: NEW_NAME
        '''
        name, year, season, episode, \
        ename, quality, subtitle, language, \
        film_tag, fflag, extension = metadata.unpack_metadata(debug=debug)

        try:
            if metadata.get_fflag() is (
                    fflags.LIBRARY_FLAG or fflags.MAIN_SHOW_DIRECTORY_FLAG or fflags.IGNORE_FLAG):
                return name
            else:
                for extension_engine in self.extension_engines:
                    if metadata.get_fflag() in extension_engine.supported_fflags:
                        return extension_engine.build_name(name=name, year=year,
                                                           season=season,
                                                           episode=episode,
                                                           ename=ename,
                                                           quality=quality,
                                                           extension=extension,
                                                           film_tag=film_tag,
                                                           debug=debug)
                    elif metadata.get_fflag() in extension_engine.supported_subtitle_fflags:
                        return extension_engine.build_subtitle_name(name=name,
                                                                    year=year,
                                                                    season=season,
                                                                    episode=episode,
                                                                    subtitle=subtitle,
                                                                    language=language,
                                                                    extension=extension,
                                                                    debug=debug)
                    elif metadata.get_fflag() in extension_engine.supported_season_fflags:
                        return extension_engine.build_season_name(name=name,
                                                                  season=season,
                                                                  debug=debug)

        except Exception as e:
            print(e)
