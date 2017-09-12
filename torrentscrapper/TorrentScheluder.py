#!/usr/bin/env python

import sched
import time
import schedule

scheduler = sched.scheduler(time.time, time.sleep)

def print_event(name):
    print 'EVENT:', time.time(), name

print 'START:', time.time()
scheduler.enter(2, 1, print_event, ('first',))
scheduler.enter(5, 1, print_event, ('second',))

scheduler.run()

def job():
    print("I'm working...")

schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
