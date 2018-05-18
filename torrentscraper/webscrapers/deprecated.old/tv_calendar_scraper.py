#!/usr/bin/env python3

from bs4 import BeautifulSoup
from pandas import DataFrame

class TvCalendarScrapper():
    def __init__(self):
        self.name = 'TvCalendarScraper'

        self.main_landing_page = 'https://www.pogdesign.co.uk/cat/'
        return

    def webscrapper(self, content):

        title_list = []
        season_list = []
        episode_list = []
        month_list = []
        day_month_list = []
        day_week_list = []
        chapter_list = []

        soup = BeautifulSoup(content, 'html.parser')
        ttable = soup.findAll('div', {'class':'month_box'})
        month = soup.findAll('h1')[1].find('a')['href']

        if ttable != []:
            print ('%s retrieving individual values from the table\n' % self.name)

            for items in ttable:
                week = items.findAll('div', {'class':'week'})

                for days in week:
                    day = days.findAll('div', {'class':'day'})

                    for shows in day:
                        day_month = shows.findAll('span', {'class': 'sp1'})[0].text
                        day_week = shows.findAll('span', {'class': 'sp3'})[0].text
                        show = shows.findAll('div', {'class':'ep info'})
                        for show_info in show:
                            a = show_info.findAll('a')

                            season = str(a[1].text)[3:]
                            episode = str(a[1].text).split('e')[0]

                            month_list.append(str(month))
                            day_month_list.append(str(day_month))
                            day_week_list.append(str(day_week))
                            title_list.append(str(a[0].text).strip())
                            season_list.append(season[1:])
                            episode_list.append(episode[1:])
                            chapter_list.append(str(a[1].text))


            dict = {'name': title_list,
                    'chapter': chapter_list,
                    'episode': episode_list,
                    'season': season_list,
                    'month' : month_list,
                    'day_month': day_month_list,
                    'day_week': day_week_list}

            dataframe = DataFrame(dict, columns=['name', 'episode', 'season', 'chapter', 'month', 'day_month', 'day_week'])
            dataframe.to_csv('./montly_tvcalendar.csv', sep='\t', encoding='utf-8')

        else:
            print ('%s seems to not be working at the moment, please try again later ...\n' % self.name)
        return dataframe


        # Create a calendar like structure or something like this to make a search
        # Episodes Aired on X-Day-Week, Next Episode Day - X-Day-Week