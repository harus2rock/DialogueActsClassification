import tkinter as tk
from tkinter import ttk
from forGUI import styles,left,right

class ClassifyApp(ttk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.answers = ['自己開示','質問(Yes/No)','確認','要求']
        self.Contextlength = 1
        styles.create_styles(self)
        self.create_widgets()

    def create_widgets(self):
        # _/_/_/ Create Parts
        # sizegrip
        self.sizegrip = ttk.Sizegrip(self)

        # frameL
        self.frameL = ttk.Frame(self,
                                padding = 10,
                                style = 'l.TFrame')
        
        left.create_leftparts(self)
        
        # frameR
        self.frameR = ttk.Frame(self,
                                padding = 10,
                                style = 'r.TFrame')

        right.create_rightparts(self)
        
        # _/_/_/ Show
        self.frameL.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
        self.frameR.grid(row=0, column=1, sticky=(tk.E,tk.W,tk.S,tk.N))
        
        self.sizegrip.grid(row=1, column=1, sticky=(tk.S, tk.E))

        self.grid(column=0, row=0, sticky=(tk.E,tk.W,tk.S,tk.N))

        # extend_column
        self.columnconfigure(0, weight=1, uniform='group1')
        self.columnconfigure(1, weight=1, uniform='group1')
        
        # extend_row
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        
        # extend_master
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)