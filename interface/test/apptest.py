from tkinter import *
from .HoverInfo import HoverInfo

class MyApp(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.grid()
        self.lbl = Label(self, text='testing')
        self.lbl.grid()

        self.hover = HoverInfo(self, 'while hovering press return \n for an exciting msg', self.HelloWorld)

    def HelloWorld(self):
        print
        'Hello World'


app = MyApp()
app.master.title('test')
app.mainloop()