# using Tkinter's Optionmenu() as a combobox
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk


def select():
    sf = "value is %s" % var.get()
    root.title(sf)
    # optional
    color = var.get()
    root['bg'] = color


root = tk.Tk()
# use width x height + x_offset + y_offset (no spaces!)
root.geometry("%dx%d+%d+%d" % (330, 80, 200, 150))
root.title("tk.Optionmenu as combobox")
var = tk.StringVar(root)
# initial value
var.set('red')
choices = ['red', 'green', 'blue', 'yellow', 'white', 'magenta']
option = tk.OptionMenu(root, var, *choices)
option.pack(side='left', padx=10, pady=10)
button = tk.Button(root, text="check value slected", command=select)
button.pack(side='left', padx=20, pady=10)
root.mainloop()