import tkinter as tk
from tkinter import ttk
from . import functions

def create_innerparts(self):
    # _/_/ Create inner parts
    # Listbox
    self.utterances = []
    self.v_utterances = tk.StringVar(value=self.utterances)
    self.lb_utterances = tk.Listbox(self.frame_talk,
                                    listvariable=self.v_utterances,
                                    height=3,
                                    font = self.myfont)
    self.lb_utterances.bind('<<ListboxSelect>>', functions.listbox_selected)
    
    # Scrollbar
    self.scrollbar = ttk.Scrollbar(self.frame_talk,
                                   orient=tk.VERTICAL,
                                   command=self.lb_utterances.yview)
    self.lb_utterances['yscrollcommand'] = self.scrollbar.set

    # _/_/ Show inner parts
    self.lb_utterances.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
    self.scrollbar.grid(row=0, column=1, sticky=(tk.N,tk.S))

    # extend_frametalk
    self.frame_talk.columnconfigure(0, weight=1)
    self.frame_talk.columnconfigure(1, weight=0)
    self.frame_talk.rowconfigure(0, weight=1)


def create_leftparts(self):
    # Create Label and Frame
    self.label_talk = ttk.Label(self.frameL,
                                text = 'Talk',
                                style = 'talk.TLabel',
                                font = self.myfont)
    self.frame_talk = ttk.LabelFrame(self.frameL,
                                     padding = 10,
                                     labelwidget = self.label_talk,
                                     style = 'talk.TLabelframe')

    # inner parts
    create_innerparts(self)

    # Show Frame
    self.frame_talk.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))

    # extend_frameL
    self.frameL.columnconfigure(0, weight=1)
    self.frameL.rowconfigure(0, weight=1)