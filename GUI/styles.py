import tkinter as tk
import tkinter.font as font
from tkinter import ttk

def create_styles(self):

    self.myfont = font.Font("", size=20)

    self.style_frameL = ttk.Style()
    self.style_frameL.configure('l.TFrame',
                                # foreground = 'saddle brown',
                                # background = 'alice blue')
                            # foreground = 'saddle brown',
                            # background = 'lemon chiffon')
                            foreground = 'white',
                            background = 'RosyBrown4')

    self.style_frame_talk = ttk.Style()
    self.style_frame_talk.configure('talk.TLabelframe',
                                    # foreground = 'blue4',
                                    # background = 'alice blue')
                            # foreground = 'saddle brown',
                            # background = 'lemon chiffon')
                            foreground = 'navajo white',
                            background = 'RosyBrown4')

    self.style_label_talk = ttk.Style()
    self.style_label_talk.configure('talk.TLabel',
                                    # foreground = 'blue4',
                                    # background = 'alice blue')
                            # foreground = 'saddle brown',
                            # background = 'lemon chiffon')
                            foreground = 'navajo white',
                            background = 'RosyBrown4')

    self.style_frameR = ttk.Style()
    self.style_frameR.configure('r.TFrame',
                                # background = 'lemon chiffon')
                                    # foreground = 'blue4',
                                    # background = 'alice blue')
                            foreground = 'navajo white',
                            background = 'RosyBrown4')

    self.style_nb = ttk.Style()
    self.style_nb.configure('nb.TNotebook',
                            # foreground = 'saddle brown',
                            # background = 'lemon chiffon')
                                    # foreground = 'blue4',
                                    # background = 'alice blue')
                            foreground = 'navajo white',
                            background = 'RosyBrown4')

    self.style_frame_nb = ttk.Style()
    self.style_frame_nb.configure('nb.TFrame',
                                #   foreground = 'saddle brown',
                                #   background = 'lemon chiffon')
                                    # foreground = 'blue4',
                                    # background = 'alice blue')
                            foreground = 'navajo white',
                            background = 'RosyBrown4')

    self.style_labelframe_nb = ttk.Style()
    self.style_labelframe_nb.configure('nb.TLabelframe',
                                    #    foreground = 'saddle brown',
                                    #    background = 'lemon chiffon')
                                    # foreground = 'blue4',
                                    # background = 'alice blue')
                            foreground = 'navajo white',
                            background = 'RosyBrown4')

    self.style_label_nb = ttk.Style()
    self.style_label_nb.configure('nb.TLabel',
                                #   foreground = 'saddle brown',
                                #   background = 'lemon chiffon')
                                    # foreground = 'blue4',
                                    # background = 'alice blue')
                            foreground = 'navajo white',
                            background = 'RosyBrown4')

    self.style_label_nbinner = ttk.Style()
    self.style_label_nbinner.configure('nbinner.TLabel',
                                #   foreground = 'saddle brown',
                                #   background = 'lemon chiffon')
                                    # foreground = 'blue4',
                                    # background = 'alice blue')
                            foreground = 'white',
                            background = 'RosyBrown4')