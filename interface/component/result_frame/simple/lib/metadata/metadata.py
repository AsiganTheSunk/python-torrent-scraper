# TODO: update default values to N/A to match the index namespace
class Metadata:
    def __init__(self, name='', year='', ename='', season='', episode='',
                 quality='', film_tag='', language='', subtitle='', uploader='',
                 source='', extension='', fflag='', acodec='', vcodec='',
                 director='', actors='', genre='', duration='', chapters='',
                 n_season='', e_season='', channels='', bit=''):

        self.name = name
        self.ename = ename
        self.season = season
        self.episode = episode
        self.quality = quality
        self.extension = extension
        self.uploader = uploader
        self.source = source
        self.year = year
        self.film_tag = film_tag
        self.language = language
        self.subtitle = subtitle
        self.acodec = acodec
        self.vcodec = vcodec
        self.channels = channels
        self.bit = bit
        self.fflag = fflag
        self.director = director
        self.actors = actors
        self.genre = genre
        self.duration = duration
        self.chapters = chapters
        self.n_season = n_season
        self.e_season = e_season

    def eval_value(self, value):
        if value is '':
            return value

    def get_name(self):
        return self.name

    def get_ename(self):
        return self.ename

    def get_season(self):
        return self.season

    def get_episode(self):
        return self.episode

    def get_quality(self):
        return self.quality

    def get_extension(self):
        return self.extension

    def get_source(self):
        return self.source

    def get_year(self):
        return self.year

    def get_film_tag(self):
        return self.film_tag

    def get_language(self):
        return self.language

    def get_subtitle(self):
        return self.subtitle

    def get_uploader(self):
        return self.uploader

    def get_fflag(self):
        return self.fflag

    def get_acodec(self):
        return self.acodec

    def get_vcodec(self):
        return self.vcodec

    def get_director(self):
        return self.director

    def get_actors(self):
        return self.actors

    def get_genre(self):
        return self.genre

    def get_duration(self):
        return self.duration

    def get_chapters(self):
        return self.chapters

    def get_n_season(self):
        return self.n_season

    def get_e_season(self):
        return self.e_season

    def set_name(self, name):
        self.name = name

    def set_ename(self, ename):
        self.ename = ename

    def set_episode(self, episode):
        self.episode = episode

    def set_season(self, season):
        self.season = season

    def set_quality(self, quality):
        self.quality = quality

    def set_extension(self, extension):
        self.extension = extension

    def set_source(self, source):
        self.source = source

    def set_year(self, year):
        self.year = year

    def set_film_tag(self, film_tag):
        self.film_tag = film_tag

    def set_language(self, language):
        self.language = language

    def set_subtitle(self, subtitle):
        self.subtitle = subtitle

    def set_uploader(self, uploader):
        self.uploader = uploader

    def set_acodec(self, audio):
        self.acodec = audio

    def set_vcodec(self, codec):
        self.vcodec = codec

    def set_fflag(self, fflag):
        self.fflag = fflag

    def set_director(self, director):
        self.director = director

    def set_actors(self, actors):
        self.actors = actors

    def set_genre(self, genre):
        self.genre = genre

    def set_duration(self, duration):
        self.duration = duration

    def set_chapters(self, chapters):
        self.chapters = chapters

    def set_n_season(self, n):
        self.n_season = n

    def set_e_season(self, e):
        self.e_season = e

    def unpack_metadata(self, debug=False):
        '''
        This function unpacks the Metada Object
        :param metadata: It represents the metadata a class Metadata Object
        :return: name, year, season, episode, ename, quality, subs, language,
                    film_tag, fflag, webscrapers
        '''
        try:
            name = self.get_name()
            year = self.get_year()
            season = self.get_season()
            episode = self.get_episode()
            ename = self.get_ename()
            quality = self.get_quality()
            subtitle = self.get_subtitle()
            language = self.get_language()
            film_tag = self.get_film_tag()
            fflag = self.get_fflag()
            extension = self.get_extension()
            source = self.get_source()
            uploader = self.get_uploader()
            n_season = self.get_n_season()
            e_season = self.get_e_season()

            if debug:
                print(name, year, season, episode, ename,
                      quality, subtitle, language,
                      film_tag, fflag, extension)

            return(name, year, season, episode, ename,
                   quality, subtitle, language,
                   film_tag, fflag, extension)

        except Exception as e:
            print(e)
