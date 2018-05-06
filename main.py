#!/usr/bin/env python

from tkinter import *
from tkinter import ttk
from simple_info_panel import InfoPanel

# content = websearch(url= 'https://www.pogdesign.co.uk/cat/')
# dataframe = tvcs.TvCalendarScrapper().webscrapper(content=content.text)
# dataframe.to_csv('./montly_tvcalendar.csv', sep='\t', encoding='utf-8')


def main():
    root = Tk()
    root.geometry("865x300")
    root.style = ttk.Style()
    root.style.theme_use("clam")
    root.iconbitmap('./cat-grumpy.ico')
    root.title("python-torrent-scraper-v0.3.2")

    upper_border_frame = Frame(root, width=865, height=5, background='#ADD8E6')
    upper_border_frame.grid(row=0, column=0)
    info_panel = InfoPanel(root, 1, 0)
    middle_border_frame = Frame(root, width=865, height=5, background='#ADD8E6')
    middle_border_frame.grid(row=2, column=0)

    root.mainloop()

if __name__ == '__main__':
    main()
