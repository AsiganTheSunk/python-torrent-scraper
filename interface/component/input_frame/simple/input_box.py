from tkinter import *

class InputBox(Frame):
    def __init__(self, master, row, column, default_message='', width=34):

        Frame.__init__(self, master)
        self.grid(row=row, column=column)

        self.input_box = Entry(self, width=width)
        self.input_box.grid(row=0, column=0)
        self.input_box.configure(foreground='gray')
        self.master = master
        self.default_message = default_message
        self.input_box.insert(END, self.default_message)

        self.bind('<FocusIn>', self.on_entry_click)

    def on_entry_click(self, *args):
        """function that gets called whenever entry is clicked"""
        if self.input_box.get() == self.default_message:
            self.input_box.delete(0, "end")  # delete all the text in the entry
            self.input_box.configure(foreground='black')
            self.input_box.insert(0, '')  # Insert blank for user input

    def reset_to_default(self):
        self.input_box.delete(0, 'end')
        self.input_box.insert(END, self.default_message)

    def disable(self):
        self.input_box['state'] = 'disable'

    def enable(self):
        self.input_box['state'] = 'normal'

    def get(self):
        if self.input_box.get() == self.default_message:
            return ''
        return self.input_box.get()