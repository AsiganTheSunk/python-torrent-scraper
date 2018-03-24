from tkinter import *

class FunFrame(Frame):
    def __init__(self, master, lbl,  **kwargs):
        Frame.__init__(self, master)
        if 'inside outer frame (self)':
            innerFrame = Frame(self, width=280, height=200, bg="red", **kwargs)
            innerFrame.grid(row=0, column=0, pady=3)
            if 'inside inner frame':
                self.l = Label(innerFrame, text=lbl)
                self.l.grid(row=0, column=0)
            separator = Frame(self, height=2, bd=1, width=280, relief=SUNKEN)
            separator.grid(row=1, column=0)

if __name__ == "__main__":
    root = Tk()
    Frame1 = FunFrame(root, "hello")
    Frame2 = FunFrame(root, "world")
    Frame1.grid(row=0, column=0)
    Frame2.grid(row=1, column=0)
    root.mainloop()