from tkinter import *
master = Tk()

def getThrottle(event):
    print (Throttle.get())

Throttle = Scale(master, from_=0, to=100, orient=HORIZONTAL, command=getThrottle)
Throttle.set(0)
Throttle.pack()

mainloop()