#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk

class SimpleComboBox:
    def __init__(self, parent, column, row, values, default_value=0):
        self.parent = parent
        self.column = column
        self.row = row
        self.values = values
        self.default_value = default_value
        self.combo()

    def combo(self):
        self.box_value = tk.StringVar()
        self.box = ttk.Combobox(self.parent, state="readonly", textvariable=self.box_value)
        self.box['values'] = self.values
        self.box.current(self.default_value)
        self.box.grid(column=self.column, row=self.row)

