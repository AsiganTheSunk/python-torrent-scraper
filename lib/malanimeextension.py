from Pymoe import Anilist
import textwrap
from lib.fileflags import FileFlags as fflags
from config_parser import CustomConfigParser
import gettext


try:
    se_config = CustomConfigParser('./torrentscraper.ini')
    language_config = se_config.get_section_map('Language')
    if language_config['language'] == '0':
        _ = lambda s: s
    else:
        es = gettext.translation('imdbfilmextension', localedir='./interface/locale', languages=['es'])
        es.install()
        _ = es.gettext

    TITLE_STRING = _('Title')
    YEAR_STRING = _('Year')
    RUNTIME_STRING = _('Runtime')
    PLOT_STRING = _('Plot Summary')
    DIRECTOR_STRING = _('Director')
    ACTORS_STRING = _('Actors')

except Exception as err:
    print(err)

class MalAnimeExtension():
    def __init__(self):
        self.name = 'TVDbExtension'
        self.ani = Anilist()
        #self.supported_fflags = [fflags.SHOW_FLAG, fflags.SHOW_DIRECTORY_FLAG]
        #self.supported_season_fflags = [fflags.SEASON_DIRECTORY_FLAG]

    def get_anime_info(self, name):
        actor_str = ''
        try:
            anime_index = self.ani.search.anime(name)['data']['Page']['media'][0]['id']
            anime_data = self.ani.get.anime(anime_index)

            try:
                year = anime_data['data']['Media']['startDate']['year']
            except:
                year = '----'

            try:
                runtime = '---'
            except:
                runtime = '---'
            try:
                actors = '----'
                # actors = movie_data['actors']
                #
                # for item in actors[:15]:
                #     actor_str = actor_str + ', ' + item['name']
                #
                # dedented_text = textwrap.dedent(actor_str[2:]).strip()
                # formated_actors = textwrap.fill(dedented_text, width=80)
                # actors = formated_actors
            except:
                actors = '----'

            try:
                director = '----'
            except:
                director = '----'

            try:
                plot = anime_data['data']['Media']['description']
                dedented_text = textwrap.dedent(plot).strip()
                formated_plot = textwrap.fill(dedented_text, width=120)
            except:
                formated_plot = '----'

            info = '[{0}]: {1}\n' \
                   '[{2}]: {3}\n' \
                   '----------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n' \
                   '[{4}]: {5} Min\n' \
                   '[{6}]: {7}\n' \
                   '----------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n' \
                   '[{8}]:\n{9}\n' \
                   '----------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n' \
                   '[{10}]:\n{11}\n'.format(TITLE_STRING, name,
                                            YEAR_STRING, year,
                                            RUNTIME_STRING, runtime,
                                            DIRECTOR_STRING, director,
                                            ACTORS_STRING, actors,
                                            PLOT_STRING, formated_plot)
        except Exception as err:
            print(err)
            info = ''
            return info
        else:
            return info.replace('<br><br> ', '')


    def get_description(self, name, debug=False):
        pass

    def get_year(self, name, debug=False):
        pass

    def get_runtime(self, name, debug=False):
        pass

    def get_actors(self, name, debug=False):
        pass


    def get_genre(self, name, debug=False):
        pass

    def get_episode_name(self, name, season, episode, debug=False):
        pass

    def get_number_of_season_episodes(self, name, season, debug=False):
        pass

    def get_number_of_seasons(self, name, debug=False):
        pass

    # print('staff', instance.get.staff(5114))
    #
    # import myanimelist.session
    # session = myanimelist.session.Session()
    # # Return an anime object corresponding to an ID of 1. IDs must be natural numbers.
    # data = session.anime(5114)
    # print(data)
    # for character in data.characters:
    #     print(character.name, '---', data.characters[character]['role'])