# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 17:19:23 2019

@author: izumi
"""

#import sys
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from gensim.models import word2vec
import os
import classify
import styles
import functions
import consts

class ClassifyApp(ttk.Frame):
    
    def __init__(self, master=None, model_w2v=None, keys=None):
        super().__init__(master)
        self.answers = ['自己開示','質問(Yes/No)','確認','要求']
        self.Contextlength = 1
        self.texts = []
        self.w2v = functions.load_w2v(consts.W2V_PATH)
        print('Classify class initialization...')
        self.models = [classify.Classify(1, self.w2v),classify.Classify(2, self.w2v),classify.Classify(3, self.w2v),classify.Classify(4, self.w2v),classify.Classify(5, self.w2v)]
        print('Done.')
        styles.create_styles(self)
        self.create_widgets()
        
    def create_widgets(self):
        # Font
        myfont = Font(self,family=u'游ゴシック',size=20)

        # sizegrip
        sizegrip = ttk.Sizegrip(self)
        
        
        # _/_/_/ Left_BaseFrame        
        # frame
        frameL = ttk.Frame(self,
                           width = 200,
                           height = 200,
                           padding = 10,
                           style = 'l.TFrame')        
        
        
        # _/_/ Left_Frame_Talk
        # Labelframe
        label_talk = ttk.Label(frameL,
                               text = 'Talk',
                               style = 'talk.TLabel',
                               font=myfont)
        frame_talk = ttk.LabelFrame(frameL,
                                    padding = 10,
                                    labelwidget = label_talk,
                                    style = 'talk.TLabelframe')
        
        # _/ Wigets_Frame_talk
        def listbox_selected(*args):
            try:
                g = int(length.get())
                if 5 < g:
                    length.set(5)
                    self.Contextlength = 5
                    g = 5
                    
                (index,) = lb_utterances.curselection()

                if g < 1 or index+1 is 1:                  
                    length.set(1)
                    self.Contextlength = 1
                    
                elif index+1 <= g:
                    length.set(index+1)
                    self.Contextlength = index+1
                
                g = int(length.get())

                texts = list(lb_utterances.get((index-g+1,),(index,)))
                self.texts = []
                for text in texts:
                    if ' : ' in text:
                        self.texts.append(text.split(' : ')[1])
                    else:
                        self.texts.append(text)
 
                print('Classify texts : ')
                print(self.texts)

                self.answers = self.models[g-1].classify(self.texts)
                answer_bottom.set(self.answers[0])
                answer_top.set(self.answers[1])
                answer_ova.set(self.answers[2])
                answer_enova.set(self.answers[3])

            except ValueError:
                pass

            
        # Listbox
        lb_utterances = tk.Listbox(frame_talk,
                                   height=3,
                                   font = myfont)
        lb_utterances.bind('<<ListboxSelect>>', listbox_selected)
        
        # Scrollbar
        scrolly = ttk.Scrollbar(frame_talk,
                                  orient=tk.VERTICAL,
                                  command=lb_utterances.yview)
        lb_utterances['yscrollcommand'] = scrolly.set

        scrollx = ttk.Scrollbar(frame_talk,
                                  orient=tk.HORIZONTAL,
                                  command=lb_utterances.xview)
        lb_utterances['xscrollcommand'] = scrollx.set

        def Delete(*args):
            try:
                index = lb_utterances.curselection()
                lb_utterances.delete(index)
            except:
                pass

        def Delete_All(*args):
            try:
                lb_utterances.delete(0,tk.END)
            except:
                pass

        # Frame
        frame_delete = ttk.Frame(frame_talk,
                                 style = 'l.TFrame')

        frame_emp = ttk.Frame(frame_delete,
                              style = 'l.TFrame',
                              width=20)
        # Button
        button_delete = ttk.Button(frame_delete,
                                   text = 'Delete',
                                   command = Delete,
                                   width = 15)
        
        button_deleteall = ttk.Button(frame_delete,
                                      text = 'Delete All',
                                      command = Delete_All,
                                      width = 15)
                
        # Show
        button_delete.grid(row=0, column=0, sticky=(tk.W))
        frame_emp.grid(row=0, column=1)
        button_deleteall.grid(row=0, column=2, sticky=(tk.E))
        lb_utterances.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
        scrolly.grid(row=0, column=1, sticky=(tk.N,tk.S))
        scrollx.grid(row=1, column=0, sticky=(tk.W,tk.E))
        frame_delete.grid(row=2, column=0)
        
        # _/_/ Show_Frame_talk
        # show
        frame_talk.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))

        # extend_frametalk
        frame_talk.columnconfigure(0, weight=1)
        frame_talk.columnconfigure(1, weight=0)
        frame_talk.rowconfigure(0, weight=1)
        frame_talk.rowconfigure(1, weight=0)
        frame_talk.rowconfigure(2, weight=0)
        
        
        # _/_/_/ Right_BaseFrame
        # frame
        frameR = ttk.Frame(self,
                           width = 200,
                           height = 200,
                           padding = 10,
                           style = 'r.TFrame')
        
        
        # _/_/_/ Right_Notebook
        # Notebook
        nb = ttk.Notebook(frameR,
                          style = 'nb.TNotebook')
        
        # frames
        frame_CLASSIFY = ttk.Frame(nb,
                             padding = 10,
                             style = 'nb.TFrame')
        
        frame_PEOPLE = ttk.Frame(nb,
                                 padding = 10,
                                 style = 'nb.TFrame')
        
        # _/_/ CLASSIFY
        # _/ classify        
        # Labelframe
        label_classify = ttk.Label(frame_CLASSIFY,
                                   text = 'Classify',
                                   style = 'nb.TLabel',
                                   font = myfont)
        frame_classify = ttk.LabelFrame(frame_CLASSIFY,
                                        padding = 10,
                                        labelwidget = label_classify,
                                        width = 100,
                                        height = 100,
                                        style = 'nb.TLabelframe')
        
        # _/ Wigets_classify
        def length_changed(*args):
            g = length.get()
            
            if g.isnumeric():
                length.set(int(g))
                self.Contextlength = int(g)

            else:
                length.set(1)
                self.Contextlength = 1

            print('Contextlength = '+str(self.Contextlength))
                
            
        # Label
        label_length = ttk.Label(frame_classify,
                                 text = 'Context Length : ',
                                 style = 'nbinner.TLabel',
                                 font = myfont)
        # Spinbox
        length = tk.StringVar()
        length.trace('w', length_changed)
        cb_length = tk.Spinbox(frame_classify,
                               textvariable = length,
                               width = 5,
                               from_ = 1,
                               to = 5,
                               font = myfont)
        cb_length.bind('<Return>', listbox_selected)
        
        # frame
        frame_empty = ttk.Frame(frame_classify,
                                height = 10,
                                style = 'nb.TFrame')
        
        # frame
        frame_clL = ttk.Frame(frame_classify,
                              style = 'nb.TFrame')
        # Label
        label_nb = ttk.Label(frame_clL,
                             text = 'RNN_Bottom : ',
                             style = 'nbinner.TLabel',
                             font = myfont)
        label_nt = ttk.Label(frame_clL,
                             text = 'RNN_Top : ',
                             style = 'nbinner.TLabel',
                             font = myfont)
        label_no = ttk.Label(frame_clL,
                             text = 'OvA : ',
                             style = 'nbinner.TLabel',
                             font = myfont)
        label_ne = ttk.Label(frame_clL,
                             text = 'ENOVA RNN : ',
                             style = 'nbinner.TLabel',
                             font = myfont)
        
        # frame
        frame_clR = ttk.Frame(frame_classify,
                              style = 'nb.TFrame')
        
        # StringVar
        answer_bottom = tk.StringVar(master=frame_classify, value=self.answers[0])
        answer_top = tk.StringVar(master=frame_classify, value=self.answers[1])
        answer_ova = tk.StringVar(master=frame_classify, value=self.answers[2])
        answer_enova = tk.StringVar(master=frame_classify, value=self.answers[3])

        # Label
        label_ab = ttk.Label(frame_clR,
                             textvariable = answer_bottom,
                             width = 13,
                             style = 'nbinner.TLabel',
                             font = myfont)
        label_at = ttk.Label(frame_clR,
                             textvariable = answer_top,
                             width = 13,
                             style = 'nbinner.TLabel',
                             font = myfont)
        label_ao = ttk.Label(frame_clR,
                             textvariable = answer_ova,
                             width = 13,
                             style = 'nbinner.TLabel',
                             font = myfont)
        label_ae = ttk.Label(frame_clR,
                             textvariable = answer_enova,
                             width = 13,
                             style = 'nbinner.TLabel',
                             font = myfont)
        
        # show
        label_length.grid(row=0, column=0, sticky=(tk.W,tk.N))
        cb_length.grid(row=0, column=1, sticky=(tk.E,tk.W,tk.N))
        
        label_nb.grid(row=0, column=0, sticky=(tk.E,tk.S,tk.N))
        label_nt.grid(row=1, column=0, sticky=(tk.E,tk.S,tk.N))
        label_no.grid(row=2, column=0, sticky=(tk.E,tk.S,tk.N))
        label_ne.grid(row=3, column=0, sticky=(tk.E,tk.S,tk.N))
        
        label_at.grid(row=1, column=0, sticky=(tk.W,tk.S,tk.N))
        label_ao.grid(row=2, column=0, sticky=(tk.W,tk.S,tk.N))
        label_ae.grid(row=3, column=0, sticky=(tk.W,tk.S,tk.N))
        label_ab.grid(row=0, column=0, sticky=(tk.W,tk.S,tk.N))
        
        frame_empty.grid(row=1, column= 0)
        
        frame_clL.grid(row=2, column=0, sticky=(tk.E,tk.S,tk.N))
        frame_clR.grid(row=2, column=1, sticky=(tk.W,tk.S,tk.N))
        
        frame_classify.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
        frame_classify.columnconfigure(0, weight=0)
        frame_classify.columnconfigure(1, weight=1)
        frame_classify.rowconfigure(0, weight=0)
        frame_classify.rowconfigure(1, weight=1)
        frame_classify.rowconfigure(2, weight=1)

        # _/ send
        # Labelframe
        label_send = ttk.Label(frame_CLASSIFY,
                               text = 'Send a message',
                               style = 'nb.TLabel',
                               font = myfont)
        frame_send = ttk.LabelFrame(frame_CLASSIFY,
                                    padding = 10,
                                    labelwidget = label_send,
                                    width = 100,
                                    height = 100,
                                    style = 'nb.TLabelframe')
        
        # _/ Wigets_send
        def Send(*args):
            ut = utterance.get()
            print(ut)
            if ut is not '':
                s = speaker.get()
                if s not in cb_speaker['values']:
                    speaker.set(cb_speaker['values'][0])
                    s = speaker.get()
                if s == '(None)':
                    inserttext = ut
                else:
                    inserttext = s+' : '+ut
                lb_utterances.insert(tk.END, inserttext)
                entry_utterance.delete(0, tk.END)
        # _/ User Combobox
        # Frame
        frame_user = ttk.Frame(frame_send,
                               style = 'nb.TFrame')

        # Label
        label_user = ttk.Label(frame_user,
                               text = 'User : ',
                               style = 'nbinner.TLabel',
                               font = myfont)
        # Combobox
        speaker = tk.StringVar()
        cb_speaker = ttk.Combobox(frame_user,
                                  textvariable = speaker,
                                  width = 7,
                                  font = myfont)
        cb_speaker['values'] = ('(None)','A','B')
        cb_speaker.set(cb_speaker['values'][0])

        # Show
        label_user.grid(row=0, column=0)
        cb_speaker.grid(row=0, column=1)
        frame_user.columnconfigure(0, weight=0)
        frame_user.columnconfigure(1, weight=1)
        
        # _/ Insert Message
        # Entry
        utterance = tk.StringVar()
        entry_utterance = ttk.Entry(frame_send,
                                    textvariable = utterance,
                                    width = 10,
                                    font = myfont)
        entry_utterance.bind('<Return>', Send)
        
        # Button
        button_send = ttk.Button(frame_send,
                                 text = 'Send',
                                 width = 5,
                                 command = Send)        

        # show
        frame_user.grid(row=0, column=0, sticky=(tk.W))
        entry_utterance.grid(row=1, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
        button_send.grid(row=1, column=1, sticky=(tk.E,tk.W,tk.S,tk.N))
        
        frame_send.grid(row=1, column=0, sticky=(tk.E,tk.W))
        frame_send.columnconfigure(0, weight=1)
        frame_send.rowconfigure(0, weight=0)
        frame_send.rowconfigure(1, weight=0)

        
        # _/_/ PEOPLE
        # _/ select       
        # Labelframe
        label_select = ttk.Label(frame_PEOPLE,
                                 text = 'Select',
                                 style = 'nb.TLabel',
                                 font = myfont)
        frame_select = ttk.LabelFrame(frame_PEOPLE,
                                      padding = 10,
                                      labelwidget = label_select,
                                      width = 100,
                                      height = 100,
                                      style = 'nb.TLabelframe')

        label_tbd = ttk.Label(frame_select,
                              text = 'TBD.',
                              style = 'nbinner.TLabel',
                              font = myfont)
        
        # _/ person
        # Labelframe
        label_person = ttk.Label(frame_PEOPLE,
                                 text = 'Person',
                                 style = 'nb.TLabel',
                                 font = myfont)
        frame_person = ttk.LabelFrame(frame_PEOPLE,
                                      padding = 10,
                                      labelwidget = label_person,
                                      width = 100,
                                      height = 100,
                                      style = 'nb.TLabelframe')

        label_tbd2 = ttk.Label(frame_person,
                              text = 'TBD.',
                              style = 'nbinner.TLabel',
                              font = myfont)

        # show
        frame_select.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
        frame_person.grid(row=1, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
        label_tbd.grid(row=0, column=0)
        label_tbd2.grid(row=0, column=0)

        # _/_/_/ Add & Show Right_Notebook
        nb.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
        nb.add(frame_CLASSIFY, text='CLASSIFY')
        nb.add(frame_PEOPLE, text='PEOPLE')
        
        nb.columnconfigure(0, weight=1)
        nb.rowconfigure(0, weight=1)
        
        frame_CLASSIFY.columnconfigure(0, weight=1)
        frame_CLASSIFY.rowconfigure(0, weight=1)
        frame_CLASSIFY.rowconfigure(1, weight=1)
        
        frame_PEOPLE.columnconfigure(0, weight=1)
        frame_PEOPLE.rowconfigure(0, weight=1)
        frame_PEOPLE.rowconfigure(1, weight=1)
        
        
        # _/_/_/ Show
        #grid
        frameL.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
        frameR.grid(row=0, column=1, sticky=(tk.E,tk.W,tk.S,tk.N))
        
        sizegrip.grid(row=1, column=1, sticky=(tk.S, tk.E))

        self.grid(column=0, row=0, sticky=(tk.E,tk.W,tk.S,tk.N))
        
        # extend_frameL
        frameL.columnconfigure(0, weight=1)
        frameL.columnconfigure(1, weight=0)
        frameL.rowconfigure(0, weight=1)
        
        # extend_frameR
        frameR.columnconfigure(0, weight=1)
        frameR.rowconfigure(0, weight=1)
        
        # extend_column
        self.columnconfigure(0, weight=1, uniform='group1')
        self.columnconfigure(1, weight=1, uniform='group1')
        
        # extend_row
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        
        # extend_master
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)


def main():
    # _/_/_/ Systems_Classify
    # main
    root = tk.Tk()
    
    # title
    root.title('Dialogue Acts Classification')
    
    # size
    root.minsize(800,400)
    
    # App
    ClassifyApp(root)

    # show
    root.mainloop()


if __name__ == '__main__':
    main()
