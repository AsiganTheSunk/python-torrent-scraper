from tkinter import *
from button_box import ButtonBox
from config_parser import CustomConfigParser

class ScraperEngineConfigDataPanel(Frame):
    def __init__(self, master, row, column, width=275, height=285, background='#ADD8E6'):
        Frame.__init__(self, master, width=width, height=height, background=background)
        self.grid(row=row, column=column)
        self.display_box = None
        self.data_box = None
        self.button_box = None
        self.master = master
        self.se_config = CustomConfigParser('./scraperengine.ini')
        self.se_dict = self.se_config.get_section_map('ScraperEngine')
        self.check_bar0 = None
        self.on_create()

    def on_create(self):
        inner_border_frame3 = Frame(self, width=275, height=25, background='#ADD8E6')
        inner_border_frame3.grid(row=0, column=0)

        inner_border_frame3 = Frame(self, width=275, height=3, background='#ADD8E6')
        inner_border_frame3.grid(row=2, column=0)

        check_bar0 = Checkbar(self, self.se_dict)
        check_bar0.grid(row=3, column=0)
        self.check_bar0 = check_bar0

        inner_border_frame3 = Frame(self, width=275, height=193, background='#ADD8E6')
        inner_border_frame3.grid(row=4, column=0)

        button_box = ButtonBox(self, 5, 0, self.master, self.save_picks)
        self.button_box = button_box

        inner_border_frame0 = Frame(self, width=275, height=3, background='#ADD8E6')
        inner_border_frame0.grid(row=6, column=0)

    def save_picks(self):
        result = self.check_bar0.get_picks()
        print('post-picks: ',result)
        for index, item in enumerate(result):
            print(index, item, result[item])
            self.se_config.set_section_key('ScraperEngine', item, str(result[item]))

class Checkbar(Frame):
    def __init__(self, parent, picks):
        Frame.__init__(self, parent)
        # self.variable = tk.BooleanVar(self)
        # self.configure(variable=self.variable)
        self.picks = picks
        self.var1 = IntVar()
        self.var2 = IntVar()
        self.var3 = IntVar()

        self.var1.set(self.picks['thepiratebay'])
        check_button0 = Checkbutton(self, text='thepiratebay', variable=self.var1, background='#ADD8E6')
        check_button0.grid(row=1, column=0)

        self.var2.set(self.picks['kickass'])
        check_button1 = Checkbutton(self, text='kickass', variable=self.var2, background='#ADD8E6')
        check_button1.grid(row=1, column=1)

        self.var3.set(self.picks['torrentfunk'])
        check_button2 = Checkbutton(self, text='torrentfunk', variable=self.var3, background='#ADD8E6')
        check_button2.grid(row=1, column=2)

    def get_picks(self):
        self.picks['thepiratebay'] = self.var1.get()
        self.picks['kickass'] = self.var2.get()
        self.picks['torrentfunk'] = self.var3.get()
        print('var1:',self.var1.get(),'var2:',self.var2.get(),'var3:',self.var3.get())
        return self.picks
    #
    # def check(self):
    #     self.variable.set(True)
    #
    # def uncheck(self):
    #     self.variable.set(False)
