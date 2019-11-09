import tvdb_api
import textwrap
# import gettext
# es = gettext.translation('about_config_data_panel', localedir='./interface/locale', languages=['es'])
# es.install()
# _ = es.gettext
# _ = lambda s:s

TITLE_STRING = [_('Title')]
YEAR_STRING = [_('Year')]
RUNTIME_STRING = [_('Runtime')]
PLOT_STRING = [_('Plot Summary')]
DIRECTOR_STRING = [_('Director')]
ACTORS_STRING = [_('Actors')]

class TVDbShowExtension():
    def __init__(self):
        self.name = 'TVDbExtension'
        self.tvdb = tvdb_api.Tvdb(actors = True)
        #self.supported_fflags = [fflags.SHOW_FLAG, fflags.SHOW_DIRECTORY_FLAG]
        #self.supported_season_fflags = [fflags.SEASON_DIRECTORY_FLAG]
        self.supported_subtitle_fflags = []

    def get_show_info(self, name, language_index=0):
        actor_str = ''
        try:
            show_data = self.tvdb[name]

            try:
                year = '----'
            except:
                year = '----'

            try:
                runtime = show_data['runtime']
            except:
                runtime = '---'
            try:
                actors = show_data['_actors']
                #
                # for item in actors[:15]:
                #     actor_str = actor_str + ', ' + item['name']

                # dedented_text = textwrap.dedent(actor_str[2:]).strip()
                # formated_actors = textwrap.fill(dedented_text, width=88)
                # actors = formated_actors
            except:
                actors = '----'

            try:
                director = '----'
            except:
                director = '----'

            try:
                plot = show_data['overview']
                dedented_text = textwrap.dedent(plot).strip()
                formated_plot = textwrap.fill(dedented_text, width=88)
            except:
                formated_plot = '----'

            info = '[{0}]: {1}\n' \
                   '[{2}]: {3}\n' \
                   '----------------------------------------------------------------------------------------' \
                   '[{4}]: {5} Min\n' \
                   '[{6}]: {7}\n' \
                   '----------------------------------------------------------------------------------------' \
                   '[{8}]:\n{9}\n' \
                   '----------------------------------------------------------------------------------------' \
                   '[{10}]:\n{11}\n'.format(TITLE_STRING[language_index], name,
                                            YEAR_STRING[language_index], year,
                                            RUNTIME_STRING[language_index], runtime,
                                            DIRECTOR_STRING[language_index], director,
                                            ACTORS_STRING[language_index], actors,
                                            PLOT_STRING[language_index], formated_plot)
        except Exception as err:
            print(err)
            info = ''
            return info
        else:
            return info


    def get_description(self, name, debug=False):
        '''
        This function retrieves number of episodes per season from a given show using tvdb_api
        :param name: It represents the name of the show you're searching for
        :param season: It represents the season of the show you're searching for
        :return: EPISODE_COUNT
        '''
        try:
            overview = self.tvdb[name]['overview']
        except tvdb_api.tvdb_error:
            # raise error that would be corrected in ReEngine turning exception into blank field
            overview = ''
            return overview
        else:
            if debug:
                print('{0}: name:{1}, description: {2}'.format(self.name, name, overview))
            return overview

    def get_year(self, name, debug=False):
        '''
        This function retrieves number of episodes per season from a given show using tvdb_api
        :param name: It represents the name of the show you're searching for
        :param season: It represents the season of the show you're searching for
        :return: EPISODE_COUNT
        '''
        try:
            year = self.tvdb[name]['firstAired']
        except tvdb_api.tvdb_error:
            # raise error that would be corrected in ReEngine turning exception into blank field
            year = ''
            return year
        else:
            if debug:
                print('{0}: name:{1}, year: {2}'.format(self.name, name, year[:-6]))
            return year[:-6]

    def get_runtime(self, name, debug=False):
        '''
        This function retrieves number of episodes per season from a given show using tvdb_api
        :param name: It represents the name of the show you're searching for
        :param season: It represents the season of the show you're searching for
        :return: EPISODE_COUNT
        '''
        try:
            runtime = self.tvdb[name]['runtime']
        except tvdb_api.tvdb_error:
            # raise error that would be corrected in ReEngine turning exception into blank field
            runtime = ''
            return runtime
        else:
            if debug:
                print('{0}: name:{1}, runtime: {2}'.format(self.name, name, runtime))
            return runtime

    def get_actors(self, name, debug=False):
        '''
        This function retrieves number of episodes per season from a given show using tvdb_api
        :param name: It represents the name of the show you're searching for
        :param season: It represents the season of the show you're searching for
        :return: EPISODE_COUNT
        '''
        try:
            actors = self.tvdb[name]['_actors']
        except tvdb_api.tvdb_error:
            # raise error that would be corrected in ReEngine turning exception into blank field
            actors = ''
            return actors
        else:
            if debug:
                print('{0}: name:{1}, actors: {2}'.format(self.name, name, actors))
            return actors


    def get_genre(self, name, debug=False):
        '''
         This function retrieves genre values from a given show using tvdb_api
        :param name: It represents the input string you're parsing
        :param debug: It represents the debug status of the function, default it's False
        :return: GENRE
        '''
        try:
            genres = self.tvdb[name]['genre']
            genre = genres[1:-1].split('|')[0]
        except tvdb_api.tvdb_error or tvdb_api.tvdb_episodenotfound:
            # raise error that would be corrected in ReEngine turning exception into blank field
            genre = ''
            return genre
        else:
            if debug:
                print('{0}: name:{1} :: genre:{2}'.format(self.name, name, genre))
            return genre

    def get_episode_name(self, name, season, episode, debug=False):
        '''
        This function retrieves episode name values from a given show using tvdb_api
        :param name: It represents the name of the show you're searching for
        :param season: It represents the season of the show you're searching for
        :param episode: It represents the episode of the show you're searching for
        :param debug: It represents the debug status of the function, default it's False
        :return: EPISODE_NAME
        '''
        try:
            aux_episode = self.tvdb[name][int(season)][int(episode)]
        except tvdb_api.tvdb_error or tvdb_api.tvdb_episodenotfound:
            # raise error that would be corrected in ReEngine turning exception into blank field
            episode_name = ''
            return episode_name
        else:
            episode_name = aux_episode['episodename']
            if debug:
                print('{0}: name:{1}, season:{2}, episode:{3} :: ename:{4}'.format(
                    self.name, name, season, episode, episode_name))

            return episode_name

    def get_number_of_season_episodes(self, name, season, debug=False):
        '''
        This function retrieves number of episodes per season from a given show using tvdb_api
        :param name: It represents the name of the show you're searching for
        :param season: It represents the season of the show you're searching for
        :return: EPISODE_COUNT
        '''
        try:
            episode_count = len(self.tvdb[name][int(season)])
        except tvdb_api.tvdb_error or tvdb_api.tvdb_episodenotfound:
            # raise error that would be corrected in ReEngine turning exception into blank field
            episode_count = 0
            return episode_count
        else:
            if debug:
                print('{0}: name:{1}, season:{2} :: episodes:{3}').format(self.name, name, season, episode_count)
            return episode_count

    def get_number_of_seasons(self, name, debug=False):
        '''
        This function retrieves number of seasons from a given show using tvdb_api
        :param name: It represents the name of the show you're searching for
        :return: SEASON_COUNT
        '''
        try:
            season_count = len(self.tvdb[name])
        except tvdb_api.tvdb_error or tvdb_api.tvdb_seasonnotfound:
            season_count = 0
            return season_count
        else:
            if debug:
                print('{0}: name:{1} :: seasons:{2}').format(self.name, name, season_count)
            return season_count
