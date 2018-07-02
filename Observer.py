# class Event(object):
#     _observers = []
#
#     def __init__(self, webscraper, item):
#         self.webscraper = webscraper
#         self.item = item
#
#     def __repr__(self):
#         return self.__class__.__name__
#
#     @classmethod
#     def register(cls, observer):
#         if observer not in cls._observers:
#             cls._observers.append(observer)
#
#     @classmethod
#     def unregister(cls, observer):
#         if observer in cls._observers:
#             cls._observers.remove(observer)
#
#     @classmethod
#     def notify(cls, subject, item):
#         event = cls(subject, item)
#         # print(cls,'-', subject,'-', event)
#         print(cls._observers, end="\n")
#         for observer in cls._observers:
#             # print(observer, end="\n")
#             observer(event)
#
# ##### 2. Ignore method repr ###
# class MagnetRequestEvent(Event):
#     def repr(self):
#         pass
#
# # class MagnetNotifierEvent(Event):
# #     def repr(self):
# #         pass
#
# def log_add_magnet(event):
#     print('{0} magnet has been added:  {1}'.format(event.webscraper, event.item))
#
# class Announcer():
#     def __call__(self, event):
#         print('Announcer Magnet Has Been Added {0}'.format(event.item))
#
# MagnetRequestEvent.register(log_add_magnet)
# MagnetRequestEvent.register(Announcer())
# MagnetRequestEvent.notify('MejorTorrentScraper', 'magnet:aferqwejklrq12')
#
# # def log(event):
# #     print('{} was written'.format(event.subject))
# #
# # class AnotherObserver():
# #     def __call__(self, event):
# #         print('Yeah {} told me !'.format(event))
# #
# # WriteEvent.register(log)
# # WriteEvent.register(AnotherObserver())
# # WriteEvent.notify('a given file', '')
# #
# # class AnotherEvent(Event):
# #     def repr(self):
# #         pass
# # # AnotherEvent = Event(subject = 'test2')
# # AnotherEvent.register(log)
# # AnotherEvent.register(AnotherObserver())
# # AnotherEvent.notify('second file', '')
import numpy as np

webscraper_list = [1,2,3,4,5,6,7]
c = 80/len(webscraper_list)
magnet_counter = 30
f = c/30

for i in np.arange(0, c, f):
    print(int(i))

def _calculate_progress_bar(webscraper_list, counter):
    base = 80/len(webscraper_list)
    chunk = base/len(counter)
    return base, chunk

def _update_progress_bar(analized, chunk):
    return int(analized * chunk)
