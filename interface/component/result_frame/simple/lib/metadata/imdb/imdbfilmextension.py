import imdb

from filemapper.utils.fileflags import FileFlags as fflags


class IMDbExtension():
    def __init__(self):
        self.name = 'IMDbExtension'
        self.imdb = imdb.IMDb()
        self.supported_fflags = [fflags.FILM_FLAG]
        self.supported_season_fflags = []
        self.supported_subtitle_fflags = []
        return

    def get_genre(self, name, index=0, debug=False):
        '''
        This function retrieves the genre of a the film
        :param name:  It represents the name of the show you're searching for
        :param index:  It represents the index of the genres, default value it's 0, you get the main genre
        :param debug: It represents the debug status of the function, default it's False
        :return: GENRE
        '''
        try:
            genres = self.imdb.search_movie(name)[0].movieID
            genre = self.imdb.get_movie(unicode(genres))['genre'][index]
        except Exception as e:
            # raise error that would be corrected in ReEngine turning exception into blank field
            genre = ''
            return genre
        else:
            if debug:
                print(
                '{extension_engine}: name:{name} :: genre:{genre}').format(
                    extension_engine=self.name,
                    name=name,
                    genre=genre)
            return genre
