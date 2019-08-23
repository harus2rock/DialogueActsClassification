# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 14:12:55 2019

@author: izumi
"""
import numpy as np
import consts
import models
import functions
from gensim.models import word2vec

"""
好きな発話から推定する．
"""

xp = np

# classにしちゃってw2vを保持する
class Classify:
    def __init__(self):
        self.w2v = functions.load_w2v(consts.W2V_PATH)

    def classify(self, texts):
        print('Classify')
    
if __name__ == '__main__':
    functions.reset_seed()

    # word2vec読み込み
    w2v = functions.load_w2v(consts.W2V_PATH)
    vocab = w2v.wv.vocab
    keys = vocab.keys()
    print(w2v['おはよう'])

