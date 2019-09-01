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

class ClassifyApp(ttk.Frame):
    
    def __init__(self, master=None, model_w2v=None, keys=None):
        super().__init__(master)
        self.answers = ['自己開示','質問(Yes/No)','確認','要求']
        self.Contextlength = 1
        self.texts = []
        # self.models = [classify.Classify(),classify.Classify(),classify.Classify(),classify.Classify(),classify.Classify()]
        self.create_widgets()
        
    def create_widgets(self):
        # Font
        myfont = Font('',20)

        # sizegrip
        sizegrip = ttk.Sizegrip(self)
        
        
        # _/_/_/ Left_BaseFrame
        # style
        style_frameL = ttk.Style()
        style_frameL.configure('l.TFrame',
                               foreground = 'saddle brown',
                               background = 'alice blue')
        
        # frame
        frameL = ttk.Frame(self,
                           width = 200,
                           height = 200,
                           padding = 10,
                           style = 'l.TFrame')        
        
        
        # _/_/ Left_Frame_Talk
        # style
        style_frame_talk = ttk.Style()
        style_frame_talk.configure('talk.TLabelframe',
                                   foreground = 'blue4',
                                   background = 'alice blue')
        style_label_talk = ttk.Style()
        style_label_talk.configure('talk.TLabel',
                                   foreground = 'blue4',
                                   background = 'alice blue')
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

                self.texts = list(lb_utterances.get((index-g+1,),(index,)))
                self.texts = [text.split(' : ')[1] for text in self.texts]

                print('Classify texts : ')
                print(self.texts)

                # self.models[g-1].classify(self.texts)

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
        
        # Show
        lb_utterances.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
        scrolly.grid(row=0, column=1, sticky=(tk.N,tk.S))
        scrollx.grid(row=1, column=0, sticky=(tk.W,tk.E))
        
        # _/_/ Show_Frame_talk
        # show
        frame_talk.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))

        # extend_frametalk
        frame_talk.columnconfigure(0, weight=1)
        frame_talk.columnconfigure(1, weight=0)
        frame_talk.rowconfigure(0, weight=1)
        frame_talk.rowconfigure(1, weight=0)
        
        
        # _/_/_/ Right_BaseFrame
        # style
        style_frameR = ttk.Style()
        style_frameR.configure('r.TFrame',
                               background = 'lemon chiffon')
        
        # frame
        frameR = ttk.Frame(self,
                           width = 200,
                           height = 200,
                           padding = 10,
                           style = 'r.TFrame')
        
        
        # _/_/_/ Right_Notebook
        # style
        style_nb = ttk.Style()
        style_nb.configure('nb.TNotebook',
                           foreground = 'saddle brown',
                           background = 'lemon chiffon')
        
        style_frame_nb = ttk.Style()
        style_frame_nb.configure('nb.TFrame',
                                 foreground = 'saddle brown',
                                 background = 'lemon chiffon')
        
        style_labelframe_nb = ttk.Style()
        style_labelframe_nb.configure('nb.TLabelframe',
                                      foreground = 'saddle brown',
                                      background = 'lemon chiffon')
        
        style_label_nb = ttk.Style()
        style_label_nb.configure('nb.TLabel',
                                 foreground = 'saddle brown',
                                 background = 'lemon chiffon')
        
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
                                 style = 'nb.TLabel',
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
                             style = 'nb.TLabel',
                             font = myfont)
        label_nt = ttk.Label(frame_clL,
                             text = 'RNN_Top : ',
                             style = 'nb.TLabel',
                             font = myfont)
        label_no = ttk.Label(frame_clL,
                             text = 'OvA : ',
                             style = 'nb.TLabel',
                             font = myfont)
        label_ne = ttk.Label(frame_clL,
                             text = 'ENOVA RNN : ',
                             style = 'nb.TLabel',
                             font = myfont)
        
        # frame
        frame_clR = ttk.Frame(frame_classify,
                              style = 'nb.TFrame')
        
        # Label
#        answers = ['自己開示','質問(Yes/No)','確認','要求']
        label_ab = ttk.Label(frame_clR,
                             text = self.answers[0],
                             style = 'nb.TLabel',
                             font = myfont)
        label_at = ttk.Label(frame_clR,
                             text = self.answers[1],
                             style = 'nb.TLabel',
                             font = myfont)
        label_ao = ttk.Label(frame_clR,
                             text = self.answers[2],
                             style = 'nb.TLabel',
                             font = myfont)
        label_ae = ttk.Label(frame_clR,
                             text = self.answers[3],
                             style = 'nb.TLabel',
                             font = myfont)
        
        # show
        label_length.grid(row=0, column=0, sticky=(tk.W,tk.N))
        cb_length.grid(row=0, column=1, sticky=(tk.E,tk.W,tk.N))
        
        label_nb.grid(row=0, column=0, sticky=(tk.E,tk.S,tk.N))
        label_nt.grid(row=1, column=0, sticky=(tk.E,tk.S,tk.N))
        label_no.grid(row=2, column=0, sticky=(tk.E,tk.S,tk.N))
        label_ne.grid(row=3, column=0, sticky=(tk.E,tk.S,tk.N))
        
        label_ab.grid(row=0, column=0, sticky=(tk.W,tk.S,tk.N))
        label_at.grid(row=1, column=0, sticky=(tk.W,tk.S,tk.N))
        label_ao.grid(row=2, column=0, sticky=(tk.W,tk.S,tk.N))
        label_ae.grid(row=3, column=0, sticky=(tk.W,tk.S,tk.N))
        
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
                inserttext = s+' : '+ut
                lb_utterances.insert(tk.END, inserttext)
                entry_utterance.delete(0, tk.END)
                
        # Combobox
        speaker = tk.StringVar()
        cb_speaker = ttk.Combobox(frame_send,
                                  textvariable = speaker,
                                  width = 10,
                                  font = myfont)
        cb_speaker['values'] = ('A','B')
        cb_speaker.set(cb_speaker['values'][0])
        
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
        cb_speaker.grid(row=0, column=0, sticky=(tk.W,tk.S,tk.N))
        entry_utterance.grid(row=1, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
        button_send.grid(row=1, column=1, sticky=(tk.E,tk.W,tk.S,tk.N))
        
        frame_send.grid(row=1, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
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
        
        # _/ person
        # Labelframe
        label_person = ttk.Label(frame_PEOPLE,
                                 text = 'PERSON',
                                 style = 'nb.TLabel',
                                 font = myfont)
        frame_person = ttk.LabelFrame(frame_PEOPLE,
                                      padding = 10,
                                      labelwidget = label_person,
                                      width = 100,
                                      height = 100,
                                      style = 'nb.TLabelframe')
        
        # show
        frame_select.grid(row=0, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
#        frame_classify.columnconfigure(0, weight=1)
#        frame_classify.rowconfigure(0, weight=1)
        
        frame_person.grid(row=1, column=0, sticky=(tk.E,tk.W,tk.S,tk.N))
#        frame_send.columnconfigure(0, weight=1)
#        frame_send.rowconfigure(0, weight=1)
        
        

        
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
    # wroed2vec保存しとくとこ
    # model_w2v
    # keys
    
    # def load_w2v(*args):
    #     pb.start(10)
    #     base = os.path.dirname(os.path.abspath(__file__))
    #     name_w2v = os.path.normpath(os.path.join(base, r'../../data/word2vec/wiki2.model'))
    #     # Load word2vec
    #     print('Loading Word2Vector...')
    #     global model_w2v
    #     global keys
    #     model_w2v = word2vec.Word2Vec.load(name_w2v)
    #     vocab = model_w2v.wv.vocab
    #     keys = vocab.keys()
    #     print('Done.')
    #     root.destroy()
        
    # # _/_/_/ Systems_Wait
    # # main
    # root = tk.Tk()
    # # title
    # root.title('Loading Word2Vector...')
    # # Progressbar
    # pb = ttk.Progressbar(root,
    #                 orient = tk.HORIZONTAL,
    #                 length = 200,
    #                 mode = 'indeterminate')
    # pb.configure(maximum=10, value=0)
    # pb.pack()
    # #button
    # ttk.Button(root,
    #            text = 'Load word2vec',
    #            command = load_w2v).pack()
    # # show
    # root.mainloop()



    # _/_/_/ Systems_Classify
    # main
    root = tk.Tk()
    
    # title
    root.title('Dialogue Acts Classification')
    
    # size
    root.minsize(800,400)
    
    # App
    # ClassifyApp(root, model_w2v=model_w2v, keys=keys)
    ClassifyApp(root)

    # show
    root.mainloop()


if __name__ == '__main__':
    main()



######################################## Test2 ########################################

## _/_/_/ system
#
#root = tk.Tk()
#
## タイトル
#root.title(u'ここはタイトル')
#
## ウィンドウサイズ変更 横幅x縦
#root.minsize(600,200)
#
## サイズグリップ
#sizegrip = ttk.Sizegrip(root)
#sizegrip.grid(row=2, column=2, sticky=(tk.S,tk.E))
#
#
## _/_/_/ 関数群
#def button1_clicked():
#    button1.state(['disabled'])
#    
#def cb1_clicked():
#    print(v1.get())
#
#
## _/_/_/ Frame_write
#style_frameW = ttk.Style()
#style_frameW.configure('w.TFrame',
#                       foreground = 'saddle brown',
#                       background = 'allice blue')
#
#frameW = ttk.Frame(
#        root,
#        height = 200,
#        width = 400,
#        relief = 'groove',
#        style = 'w.TFrame')
#
#frameW.grid(row=1,column=2)
#frameW.propagate(False)
#
## _/_/_/ Frame1
## Style
#style_frame1 = ttk.Style()
#style_frame1.configure('a.TFrame', 
#                       foreground = 'saddle brown', 
#                       background = 'ghost white')
#
#style_label1 = ttk.Style()
#style_label1.configure('a.TLabel', 
#                       foreground = 'saddle brown', 
#                       background = 'ghost white', 
#                       padding = (5,10))
#
#style_button1 = ttk.Style()
#style_button1.configure('a.TButton',
#                        foreground = 'saddle brown')
#
#style_cb1 = ttk.Style()
#style_cb1.configure('a.TCheckbutton',
#                    foreground = 'saddle brown',
#                    background = 'ghost white',
#                    padding = (5,10))
#
## Frame
#frame1 = ttk.Frame(
#        frameW,
#        height = 200,
#        width = 400,
#        relief = 'groove',
#        borderwidth = 10,
#        style = 'a.TFrame')
#
## Label
#label1 = ttk.Label(
#        frame1,
#        text = 'Hello',
#        background = '#0000aa',
#        foreground = '#ffffff',
#        style = 'a.TLabel')
#
#label2 = ttk.Label(
#        frame1,
#        text = 'World',
#        background = '#ffffff',
#        foreground = 'blue',
#        width = 20,
#        anchor = tk.E,
#        style = 'a.TLabel')
#
## Button
#button1 = ttk.Button(
#        frame1,
#        text = 'Quit',
#        command = button1_clicked,
#        style = 'a.TButton')
#
## Checkbutton
#v1 = tk.StringVar()
#
#cb1 = ttk.Checkbutton(
#        frame1,
#        text = 'Option 1',
#        onvalue = 'A',
#        offvalue = 'B',
#        variable = v1,
#        command = cb1_clicked,
#        style = 'a.TCheckbutton')
#
## Show
#frame1.grid(row=1, column=1)
#label1.grid(row=1, column=1)
#label2.grid(row=1, column=2)
#button1.grid(row=2, column=2)
#cb1.grid(row=2, column=1)
#
#frame1.propagate(False)
#
#
## _/_/_/ Frame2
## Style
#style_frame2 = ttk.Style()
#style_frame2.configure('b.TFrame', 
#                       foreground = 'blue4', 
#                       background = 'white')
#
#style_label2 = ttk.Style()
#style_label2.configure('b.TLabel', 
#                       foreground = 'blue4', 
#                       background = 'white', 
#                       padding = (5,10))
#
## Frame
#frame2 = ttk.Frame(
#        root,
#        height = 200,
#        width = 200,
#        relief = 'groove',
#        borderwidth = 10,
#        style = 'b.TFrame')
#
## Label
##icon = tk.PhotoImage(file = 'face2.png')
##icon = icon.subsample(6)
##
##label3 = ttk.Label(
##        frame2,
##        image = icon,
##        style = 'b.TLabel')
#
#s = tk.StringVar()
#s.set('Hello!')
#
#label4 = ttk.Label(
#        frame2,
#        textvariable = s,
#        width = 30,
#        anchor = tk.W,
#        style = 'b.TLabel')
#
## Show
#frame2.grid(row=1, column=1)
##label3.grid(row=1, column=1)
#label4.grid(row=1, column=2)
#
#frame2.propagate(False)
#
#root.mainloop()

######################################## Test1 ########################################
## _/_/_/ system
#
#root = tk.Tk()
#
## タイトル
#root.title(u'ここはタイトル')
#
## ウィンドウサイズ変更 横幅x縦
#root.minsize(600,200)
## _/_/_/ ラベル
## 出現
#Static1 = tk.Label(text=u'▼ 以下に入力 ▼', foreground='#ff0000', background='#90caf9')
#Static1.pack()
#
#Static2 = tk.Label(text=u'test', foreground='#ff0000', background='#90caf9')
#Static2.place(x=150, y=228)
#
## _/_/_/ Entry
## 出現
#Entry1 = tk.Entry(width=50)
#Entry1.insert(tk.END, u'発話をいれてね')
#Entry1.pack()
#
## 取得
#Entry1_value = Entry1.get()
#print(Entry1_value)
#
## 値削除
#Entry1.delete(0, tk.END)
#
## _/_/_/ Button
## 出現
#Button1 = tk.Button(text=u'push', width=10)
#Button1.pack()
#
#
#
#root.mainloop()