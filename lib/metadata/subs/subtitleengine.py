from filemapper.metadata.metadata import Metadata
from filemapper.metadata.subs.subtitlesrtextension import SubtitleSrtExtension
from filemapper.utils.fileflags import FileFlags as fflags


class SubtitleEngine():
    def __init__(self):
        self.name = 'SubtitleEngine'
        self.supported_fflags = [fflags.SUBTITLE_ANIME_FLAG,
                                 fflags.SUBTITLE_FILM_FLAG,
                                 fflags.SUBTITLE_SHOW_FLAG]
        self.supported_formats = ['srt', 'ass']
        self.category_extension = [SubtitleSrtExtension()]
        return

    def map(self, stream, metadata, verbose=False, debug=False):
        '''
        This function maps the file or directory based on the premapping done by filemapper
        :param stream: It represents the input string you're mapping
        :param fflag: It represents the fflag of the file or directory your mapping
        :param debug: It represents the debug status of the function, default it's False
        :param verbose: It represents the verbose status of the function, default it's False
        :return: language
        '''
        language = ''

        for extension_engine in self.category_extension:
            # This will try to map the diferent values present in the file or directory basename
            if metadata.get_fflag() in extension_engine.supported_subtitle_fflags:
                try:
                    language = extension_engine.get_language(stream=stream,
                                                             debug=verbose)

                except Exception:
                    print(
                    '{extension_engine} Error: unable to parse argument ...').format(
                        extension_engine=self.name)
                    return Metadata(name=metadata.get_name(),
                                    episode=metadata.get_episode(),
                                    season=metadata.get_season(),
                                    year=metadata.get_year(),
                                    film_tag=metadata.get_film_tag(),
                                    subtitle=metadata.get_subtitle(),
                                    fflag=metadata.get_fflag(),
                                    language='',
                                    extension=metadata.get_extension())

                else:
                    if debug:
                        print(
                        '{extension_engine} :: {fflag}::{stream} ::\n language:{language}').format(
                            extension_engine=self.name,
                            fflag=metadata.get_fflag(),
                            stream=stream,
                            language=language)

                    return Metadata(name=metadata.get_name(),
                                    episode=metadata.get_episode(),
                                    season=metadata.get_season(),
                                    year=metadata.get_year(),
                                    film_tag=metadata.get_film_tag(),
                                    subtitle=metadata.get_subtitle(),
                                    fflag=metadata.get_fflag(),
                                    language=language,
                                    extension=metadata.get_extension())
