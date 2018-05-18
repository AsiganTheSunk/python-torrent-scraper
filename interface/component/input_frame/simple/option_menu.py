from tkinter import OptionMenu, StringVar

class SimpleOptionMenu(OptionMenu):
    def __init__(self, master, status, *options):
        self.var = StringVar(master)
        self.var.set(status)
        self.selection = ''
        self.var.trace('w', self.get)
        OptionMenu.__init__(self, master, self.var, *options)
        self.config(font=('calibri', (10)), width=12, relief='groove')
        self['menu'].config(font=('calibri', (10)), bg='white')

    def get(self, *args):
        self.selection = self.var.get()
        print(self.selection)