import tkinter as tk


def on_entry_click(*args, argument1=None, argument2=None):
    """function that gets called whenever entry is clicked"""
    if entry.get() == 'Enter your user name...':
       entry.delete(0, "end") # delete all the text in the entry
       entry.insert(0, '') #Insert blank for user input


root = tk.Tk()

label = tk.Label(root, text="User: ")
label.pack(side="left")

entry = tk.Entry(root, bd=1)
entry.insert(0, 'Enter your user name...')
entry.bind('<FocusIn>', on_entry_click)
entry.pack(side="left")

root.mainloop()