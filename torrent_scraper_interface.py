import tkinter
from interface.main_threaded_interface import ThreadedClient

def run_interface():
    root = tkinter.Tk()
    client = ThreadedClient(root)
    root.mainloop()
