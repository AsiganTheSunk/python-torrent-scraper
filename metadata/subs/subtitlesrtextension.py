import chardet
import pysrt
from langdetect import DetectorFactory
from langdetect import detect

from filemapper.utils.fileflags import FileFlags as fflags


class SubtitleSrtExtension():
    def __init__(self):
        self.name = 'SubtitleSrtExtension'
        self.supported_fflags = []
        self.supported_season_fflags = []
        self.supported_subtitle_fflags = [fflags.SUBTITLE_ANIME_FLAG,
                                          fflags.SUBTITLE_FILM_FLAG,
                                          fflags.SUBTITLE_SHOW_FLAG]
        self.supported_formats = ['srt']
        return

    def _get_subtitle_chunk(self, path, chunk_size=15):
        '''
        Function _get_subtitle_chunk
        This function opens the subs file and extract a chunk using pysrt

        :param path: It represents the path of the subs file
        :param chunk_size: It represents the number of lines you'regex gonna metadata in the chunk
        :return: SUBTITLE_CHUNK, None otherwise
        '''
        subtitle_chunk = ''
        try:
            with open(str(path), 'r') as subtitle:
                subtitle_data = subtitle.read()
                encoding = chardet.detect(subtitle_data)
                content = pysrt.open(path, encoding=encoding['encoding'])

                for i in range(0, chunk_size, 1):
                    subtitle_chunk += ' ' + content[i].text

            return subtitle_chunk
        except Exception:
            return None

    def get_language(self, stream, debug=False):

        '''
        This function retrieves language from a given path using regex | langdetect, firts it will try to get the
        language from the name file, if the fuction it's unable to metadata this way it will try reading a chunk of
        the subs content and detect the language using langdetect
        :param stream: It represents the input string you're parsing
        :param debug: It represents the debug status of the function, default it's False
        :return: LANGUAGE
        '''

        language = ''
        DetectorFactory.seed = 0
        stream = unicode(stream, "utf-8")
        try:
            if stream[-3:] in self.supported_formats:
                language = detect(self._get_subtitle_chunk(path=stream))
        except Exception:
            # raise error that would be corrected in ReEngine turning exception into blank field
            language = ''
            return language
        else:
            if debug:
                print(
                '{extension_engine}: {stream} :: language:{value}').format(
                    extension_engine=self.name,
                    stream=stream,
                    value=language)
            return language
