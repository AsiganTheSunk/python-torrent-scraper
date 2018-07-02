from subject import Subject


class StatusData(Subject):
    def __init__(self, webscraper_name=''):
        super(StatusData, self).__init__()
        self.webscraper_name = webscraper_name
        self._analized_data = 0
        self._counter = 0

    @property
    def analized_data(self):
        return self._analized_data

    @property
    def counter(self):
        return self._counter

    @analized_data.setter
    def analized_data(self, value):
        self._analized_data = value
        self.notify()

    @counter.setter
    def counter(self, value):
        self._counter = value
        self.notify()

class MagnetAnalizedViewer(object):
    def update(self, subject):
        print('{}'.format(subject.analized_data))

class MagnetCounterViewer(object):
    def update(self, subject):
        print('{}'.format(subject.counter))
        return subject.counter