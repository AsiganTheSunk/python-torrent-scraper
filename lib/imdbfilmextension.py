import imdb
import textwrap

class IMDbExtension():
    def __init__(self):
        self.name = 'IMDbExtension'
        self.imdb = imdb.IMDb()
        # self.supported_fflags = [fflags.FILM_FLAG]
        self.supported_season_fflags = []
        self.supported_subtitle_fflags = []

    def get_movie_index(self, name):
        try:
            movie_index = self.imdb.search_movie(name)[0].movieID
        except Exception as err:
            movie_index = ''
            return movie_index
        else:
            print(self.name,  movie_index, name)
            return movie_index


    def get_poster_movie(self, movie_index):
        try:
            movie = self.imdb.get_movie(str(movie_index))
            print(self.imdb.helpers.fullSizeCoverURL(movie_index))
        except Exception as err:
            poster = ''
            return poster
        else:
            return movie

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
        actor_str = ''
        try:
            actors = self.imdb.get_movie(str(movie_index))['actors']
            for item in actors[:15]:
                # actor_list.append(item['name'])
                actor_str = actor_str + ', '  + item['name']
        except Exception as err:
            return ''
        else:
            # print(self.name, movie_index, actor_list[:15])

            dedented_text = textwrap.dedent(actor_str[2:]).strip()
            formated_actors = textwrap.fill(dedented_text, width=88)
            return formated_actors

    def get_movie_info(self, name):
        actor_str = ''
        try:
            movie_index = self.imdb.search_movie(name)[0].movieID
            movie_data = self.imdb.get_movie(str(movie_index))

            try:
                year = movie_data['year']
            except:
                year = ''

            try:
                runtime = movie_data['runtime'][0]
            except:
                runtime = '--'
            try:
                actors = movie_data['actors']

                for item in actors[:15]:
                    actor_str = actor_str + ', ' + item['name']

                dedented_text = textwrap.dedent(actor_str[2:]).strip()
                formated_actors = textwrap.fill(dedented_text, width=88)
                actors = formated_actors
            except:
                actors = ''

            try:
                director = movie_data['director'][0]['name']
            except:
                director = ''

            try:
                plot = movie_data['plot summary'][0]
                dedented_text = textwrap.dedent(plot).strip()
                formated_plot = textwrap.fill(dedented_text, width=88)
            except:
                formated_plot = ''

            info = '[Title]: {0}\n' \
                   '[Year]: {1}\n' \
                   '----------------------------------------------------------------------------------------' \
                   '[Runtime]: {2} Min\n' \
                   '[Director]: {3}\n' \
                   '----------------------------------------------------------------------------------------' \
                   '[Actors]:\n{4}\n' \
                   '----------------------------------------------------------------------------------------' \
                   '[Plot Summary]:\n{5}\n'.format(name, year, runtime, director, actors, formated_plot)
        except Exception as err:
            print(err)
            info = ''
            return info
        else:
            #print(self.name, movie_index, movie_data)
            return info


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
        dedented_text = ''
        try:
            plot_summary = self.imdb.get_movie(str(movie_index))['plot summary'][0]
            dedented_text = textwrap.dedent(plot_summary).strip()
            formated_plot = textwrap.fill(dedented_text, width=88)

        except Exception as err:
            plot_summary = ''
            return plot_summary
        else:
            # print(self.name, movie_index, plot_summary)
            return formated_plot

    def get_runtime (self, movie_index):
        try:
            runtime = self.imdb.get_movie(str(movie_index))['runtime'][0]
        except Exception as err:
            runtime = ''
            return runtime
        else:
            # print(self.name, movie_index, runtime)
            return runtime