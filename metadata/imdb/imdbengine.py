from filemapper.metadata.metadata import Metadata
from filemapper.metadata.imdb.imdbfilmextension import IMDbExtension
from filemapper.utils.fileflags import FileFlags as fflags


class IMDbEngine():
    def __init__(self):
        self.name = 'IMDbExtension'
        self.supported_fflags = [fflags.FILM_FLAG]
        self.category_extension = [IMDbExtension()]
        return

    def map(self, metadata, verbose=False, debug=False):
        '''
        This function maps the file or directory based on the premapping done by filemapper
        :param metadata: It represents the input Metadata object you're using to map extended values
        :param fflag: It represents the fflag of the file or directory your mapping
        :param debug: It represents the debug status of the function, default it's False
        :param verbose: It represents the verbose status of the function, default it's False
        :return: Metadata
        '''
        genre = ''
        for extension_engine in self.category_extension:
            # This will try to map the diferent values present in the file or directory basename

            if metadata.get_fflag() in extension_engine.supported_fflags:
                try:
                    genre = extension_engine.get_genre(name=metadata.get_name(),
                                                       debug=verbose)

                except AttributeError:
                    print(
                    '{extension_engine} Error: unable to parse argument ...').format(
                        extension_engine=self.name)
                    return metadata.extended_metadata(genre='')

                else:
                    if debug:
                        print(
                        '{extension_engine} :: {fflag}::{stream} ::\n name:{name}, '
                        'genre:{genre}').format(extension_engine=self.name,
                                                fflag=metadata.get_fflag(),
                                                stream=metadata,
                                                name=metadata.get_name(),
                                                genre=genre)

                    return Metadata(name=metadata.get_name(),
                                    year=metadata.get_year(),
                                    film_tag=metadata.get_film_tag(),
                                    quality=metadata.get_quality(),
                                    acodec=metadata.get_acodec(),
                                    vcodec=metadata.get_vcodec(),
                                    source=metadata.get_source(),
                                    uploader=metadata.get_uploader(),
                                    genre=genre,
                                    fflag=metadata.get_fflag(),
                                    extension=metadata.get_extension())
        return
