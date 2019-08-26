import tkinter as tk
from tkinter import ttk
from . import functions

def create_note_classify(self):
    # _/_/ Classify Frame
    # Labelframe
    self.label_classify = ttk.Label(self.frame_CLASSIFY,
                                    text = 'Classify',
                                    style = 'nb.TLabel',
                                    font = self.myfont)
    self.frame_classify = ttk.LabelFrame(self.frame_CLASSIFY,
                                         padding = 10,
                                         labelwidget = self.label_classify,
                                         width = 100,
                                         height = 100,
                                         style = 'nb.TLabelframe')

    # _/_/ Send Frame
    # Labelframe
    self.label_send = ttk.Label(self.frame_CLASSIFY,
                                text = 'Send a message',
                                style = 'nb.TLabel',
                                font = self.myfont)
    self.frame_send = ttk.LabelFrame(self.frame_CLASSIFY,
                                     padding = 10,
                                     labelwidget = self.label_send,
                                     width = 100,
                                     height = 100,
                                     style = 'nb.TLabelframe')
    
    # Show
    self.frame_classify.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
    self.frame_send.grid(row=1, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
    
    self.frame_CLASSIFY.columnconfigure(0, weight=1)
    self.frame_CLASSIFY.rowconfigure(0, weight=1)
    self.frame_CLASSIFY.rowconfigure(1, weight=1)

def create_note_people(self):
    pass

def create_rightparts(self):
    # Create Notebook
    self.nb = ttk.Notebook(self.frameR,
                           style = 'nb.TNotebook')
    
    # Create frames on Notebook
    self.frame_CLASSIFY = ttk.Frame(self.nb,
                                    padding = 10,
                                    style = 'nb.TFrame')
    
    create_note_classify(self)

    self.frame_PEOPLE = ttk.Frame(self.nb,
                                  padding = 10,
                                  style = 'nb.TFrame')

    create_note_people(self)
    
    # Add tabs and Show Right_Notebook
    self.nb.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
    self.nb.add(self.frame_CLASSIFY, text='CLASSIFY')
    self.nb.add(self.frame_PEOPLE, text='PEOPLE')
    
    self.nb.columnconfigure(0, weight=1)
    self.nb.rowconfigure(0, weight=1)

    # extend_frameR
    self.frameR.columnconfigure(0, weight=1)
    self.frameR.rowconfigure(0, weight=1)