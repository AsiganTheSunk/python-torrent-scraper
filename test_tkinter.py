from Tkinter import *
import time


class myapp(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.weeds()

    def weeds(self):
        self.button = Button(self, text='Button', command=self.onclick).grid()
        self.var = StringVar()

        self.msg = Label(self, textvar=self.var)
        self.msg.grid()

    def onclick(self):
        self.var.set("Running command..")
        self.msg.update_idletasks()  # remember to update "idle tasks"-**
        time.sleep(1.5)  # otherwise your message waits until
        self.nest1()  # mainloop

    def nest1(self):
        self.var.set("Still Running.")
        self.msg.update_idletasks()  # **
        time.sleep(2)
        self.nest2()

    def nest2(self):
        self.var.set("Not yet.")
        self.msg.update_idletasks()  # **
        time.sleep(1.5)
        self.nest3()

    def nest3(self):
        self.var.set("Finished")
        self.msg.update_idletasks()  # **


root = Tk()
APP = myapp(master=root)
APP.mainloop()