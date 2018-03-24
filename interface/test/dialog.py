import tkinter
from tkinter import *

root = Tk()
root.title('Random')
Label(text='How many squares? (ex: 4x4, 5x3)').pack(side=TOP,padx=10,pady=10)

entry = Entry(root, width=10)
entry.pack(side=TOP,padx=10,pady=10)

def onok():
    x, y = entry.get().split('x')
    for row in range(int(y)):
        for col in range(int(x)):
            print((col, row))

Button(root, text='OK', command=onok).pack(side=LEFT)
Button(root, text='CLOSE').pack(side= RIGHT)

root.mainloop()