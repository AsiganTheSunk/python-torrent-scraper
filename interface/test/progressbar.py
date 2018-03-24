#!/usr/bin/env python

try:
  import Tkinter as tkinter   # Python 2
  import ttk
except ImportError:
  import tkinter   # Python 3
  import tkinter.ttk as ttk


def main():

  root = tkinter.Tk()

  ft = ttk.Frame()
  fb = ttk.Frame()

  ft.pack(expand=True, fill=tkinter.BOTH, side=tkinter.TOP)
  fb.pack(expand=True, fill=tkinter.BOTH, side=tkinter.TOP)

  pb_hd = ttk.Progressbar(ft, orient='horizontal', mode='determinate')
  pb_hD = ttk.Progressbar(ft, orient='horizontal', mode='indeterminate')
  pb_vd = ttk.Progressbar(fb, orient='vertical', mode='determinate')
  pb_vD = ttk.Progressbar(fb, orient='vertical', mode='indeterminate')

  pb_hd.pack(expand=True, fill=tkinter.BOTH, side=Tkinter.TOP)
  pb_hD.pack(expand=True, fill=tkinter.BOTH, side=Tkinter.TOP)
  pb_vd.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.LEFT)
  pb_vD.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.LEFT)

  pb_hd.start(50)
  pb_hD.start(50)
  pb_vd.start(50)
  pb_vD.start(50)

  root.mainloop()


if __name__ == '__main__':
    main()