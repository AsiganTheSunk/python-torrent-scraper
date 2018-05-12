from filemapper.metadata.metadata import Metadata
from filemapper.metadata.tvdb.tvdbshowextension import TVDbShowExtension
from filemapper.utils.fileflags import FileFlags as fflags


class TVDbEngine():
    def __init__(self):
        self.name = 'TVDbEngine'
        self.supported_fflags = [fflags.SHOW_FLAG, fflags.SHOW_DIRECTORY_FLAG,
                                 fflags.SEASON_DIRECTORY_FLAG]
        self.category_extension = [TVDbShowExtension()]
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
        ename = n_season = e_season = genre = ''

        for extension_engine in self.category_extension:
            # This will try to map the diferent values present in the file or directory basename

            if metadata.get_fflag() in extension_engine.supported_fflags:
                try:
                    genre = extension_engine.get_genre(name=metadata.get_name(),
                                                       debug=verbose)
                    ename = extension_engine.get_episode_name(
                        name=metadata.get_name(),
                        season=metadata.get_season(),
                        episode=metadata.get_episode(),
                        debug=verbose)
                except AttributeError:
                    return Metadata(name=metadata.get_name(),
                                    episode=metadata.get_episode(),
                                    ename='',
                                    season=metadata.get_season(),
                                    year=metadata.get_year(),
                                    film_tag=metadata.get_film_tag(),
                                    quality=metadata.get_quality(),
                                    acodec=metadata.get_acodec(),
                                    vcodec=metadata.get_vcodec(),
                                    source=metadata.get_source(),
                                    uploader=metadata.get_uploader(),
                                    genre='',
                                    fflag=metadata.get_fflag(),
                                    extension=metadata.get_extension())

                else:
                    if debug:
                        print(
                            '{extension_engine} :: {fflag}::{stream} ::\n name:{name}, season:{season}, episode:{episode}, ename:{ename}, '
                            'genre:{genre}').format(extension_engine=self.name,
                                                    fflag=metadata.get_fflag(),
                                                    stream=metadata,
                                                    name=metadata.get_name(),
                                                    episode=metadata.get_episode(),
                                                    season=metadata.get_season(),
                                                    ename=ename,
                                                    genre=genre)

                    return Metadata(name=metadata.get_name(),
                                    episode=metadata.get_episode(),
                                    ename=ename,
                                    season=metadata.get_season(),
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

            elif metadata.get_fflag() in extension_engine.supported_season_fflags:
                try:
                    n_season = extension_engine.get_number_of_seasons(
                        name=metadata.get_name(), debug=verbose)
                    e_season = extension_engine.get_number_of_season_episodes(
                        name=metadata.get_name(),
                        season=metadata.get_season(),
                        debug=verbose)
                except AttributeError:
                    print 'PARSING FAILED'
                    return Metadata(name=metadata.get_name(),
                                    episode=metadata.get_episode(),
                                    e_season='',
                                    season=metadata.get_season(),
                                    year=metadata.get_year(),
                                    film_tag=metadata.get_film_tag(),
                                    quality=metadata.get_quality(),
                                    acodec=metadata.get_acodec(),
                                    vcodec=metadata.get_vcodec(),
                                    source=metadata.get_source(),
                                    uploader=metadata.get_uploader(),
                                    n_season='',
                                    fflag=metadata.get_fflag(),
                                    extension=metadata.get_extension())


                else:
                    if debug:
                        print(
                        '{extension_engine} :: {fflag}::{stream} ::\n name:{name} season:{season}, '
                        'e_season:{e_season}, n_season:{n_season}').format(
                            extension_engine=self.name,
                            fflag=metadata.get_fflag(),
                            stream=metadata,
                            name=metadata.get_name(),
                            season=metadata.get_season(),
                            e_season=e_season,
                            n_season=n_season
                        )

                    return Metadata(name=metadata.get_name(),
                                    episode=metadata.get_episode(),
                                    e_season=e_season,
                                    season=metadata.get_season(),
                                    year=metadata.get_year(),
                                    film_tag=metadata.get_film_tag(),
                                    quality=metadata.get_quality(),
                                    acodec=metadata.get_acodec(),
                                    vcodec=metadata.get_vcodec(),
                                    source=metadata.get_source(),
                                    uploader=metadata.get_uploader(),
                                    n_season=n_season,
                                    fflag=metadata.get_fflag(),
                                    extension=metadata.get_extension())

        return
