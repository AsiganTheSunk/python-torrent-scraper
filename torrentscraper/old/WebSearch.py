class WebSearch():
    def __init__(self, title='', year='', season='', episode='', quality='', header='', search_type=''):
        self.search_type = search_type
        self.quality = quality
        self.title = title
        self.year = year
        self.season = season
        self.episode = episode
        self.header = header

    def set_search_type(self, value):
        self.search_type = value

    def set_quality(self, value):
        self.quality = value

    def set_title(self, value):
        self.title = value

    def set_year(self, value):
        self.year = value

    def set_season(self, value):
        self.season = value

    def set_episode(self, value):
        self.episode = value

    def set_header(self, value):
        self.header = value