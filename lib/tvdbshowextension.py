import tvdb_api

class TVDbShowExtension():
    def __init__(self):
        self.name = 'TVDbExtension'
        self.tvdb = tvdb_api.Tvdb(actors = True)
        #self.supported_fflags = [fflags.SHOW_FLAG, fflags.SHOW_DIRECTORY_FLAG]
        #self.supported_season_fflags = [fflags.SEASON_DIRECTORY_FLAG]
        self.supported_subtitle_fflags = []

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
