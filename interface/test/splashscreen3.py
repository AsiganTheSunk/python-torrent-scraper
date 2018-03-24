#!/usr/bin/env python

try:
  import Tkinter              # Python 2
  import ttk
except ImportError:
    from tkinter import *       # Python 3
    import tkinter.ttk as ttk
    from PIL import ImageTk, Image

class DemoSplashScreen:
    def __init__(self, parent):
        self.parent = parent
        self.Splash()
        self.SplashWindow()

    def Splash(self):
        # import image menggunakan Pillow
        self.background_image = Image.open('klinikpython-splash.gif')
        self.imgSplash = ImageTk.PhotoImage(self.background_image)

    def SplashWindow(self):
        width, heigth = self.background_image.size
        middle_width = (self.parent.winfo_screenwidth() - width) // 2
        middle_height = (self.parent.winfo_screenheight() - heigth) // 2
        self.parent.geometry("%ix%i+%i+%i" % (width, heigth, middle_width, middle_height))
        Label(self.parent, image=self.imgSplash).pack()

    def ProgressBar(self):
        return


if __name__ == '__main__':
    root = Tk()
    ft = ttk.Frame()
    ft.pack(expand=True, fill=X, side=BOTTOM)
    pb_hd = ttk.Progressbar(ft, orient='horizontal', mode='indeterminate')
    pb_hd.pack(expand=True, fill=X, side=BOTTOM)
    pb_hd.start(50)
    root.overrideredirect(True)
    app = DemoSplashScreen(root)
    root.after(5000, root.destroy)
    root.mainloop()