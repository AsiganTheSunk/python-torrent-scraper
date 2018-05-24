from tkinter import OptionMenu, StringVar

class SimpleOptionMenu(OptionMenu):
    def __init__(self, master, status, *options):
        self.var = StringVar(master)
        self.var.set(status)
        OptionMenu.__init__(self, master, self.var, *options)
        self.selection = ''
        self.var.trace('w', self.get)
        self.config(font=('calibri', (10)), width=12, relief='groove')
        self['menu'].config(font=('calibri', (10)), bg='#F0F8FF')

    def get(self, *args):
        self.selection = self.var.get()
        print(self.selection)
