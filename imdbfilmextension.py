import imdb


class IMDbExtension():
    def __init__(self):
        self.name = 'IMDbExtension'
        self.imdb = imdb.IMDb()
        # self.supported_fflags = [fflags.FILM_FLAG]
        self.supported_season_fflags = []
        self.supported_subtitle_fflags = []
        return

    def get_movie_index(self, name):
        try:
            movie_index = self.imdb.search_movie(name)[0].movieID
        except Exception as err:
            movie_index = ''
            return movie_index
        else:
            print(self.name,  movie_index, name)
            return movie_index

    def get_genre(self, movie_index, index=0, debug=False):
        try:
            genre = self.imdb.get_movie(str(movie_index))['genre'][index]
        except Exception as err:
            genre = ''
            return genre
        else:
            print(self.name, movie_index, genre)
            return genre


    def get_director(self, movie_index):
        director = ''
        try:
            director = self.imdb.get_movie(str(movie_index))['director'][0]['name']
        except Exception as err:
            director = ''
            return director
        else:
            print(self.name, movie_index, director)
            return director


    def get_actors(self, movie_index):
        actor_list = []
        try:
            actor_list = []
            actors = self.imdb.get_movie(str(movie_index))['actors']
            for item in actors[:15]:
                actor_list.append(item['name'])

        except Exception as err:
            actors_list = []
            return actor_list
        else:
            # print(self.name, movie_index, actor_list[:15])
            return actor_list[:15]

    def get_year(self, movie_index):
        try:
            year = self.imdb.get_movie(str(movie_index))['year']
        except Exception as err:
            year = ''
            return year
        else:
            print(self.name, movie_index, year)
            return year

    def get_plot_summary (self, movie_index):
        try:
            plot_summary = self.imdb.get_movie(str(movie_index))['plot summary'][0]
        except Exception as err:
            plot_summary = ''
            return plot_summary
        else:
            # print(self.name, movie_index, plot_summary)
            return plot_summary

    def get_runtime (self, movie_index):
        try:
            runtime = self.imdb.get_movie(str(movie_index))['runtime'][0]
        except Exception as err:
            runtime = ''
            return runtime
        else:
            # print(self.name, movie_index, runtime)
            return runtime