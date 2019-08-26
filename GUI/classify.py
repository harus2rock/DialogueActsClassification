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
from chainer import serializers
import os
import MeCab

"""
好きな発話から推定する．
"""

xp = np

# classにしちゃってw2vを保持する
# 文脈長を保持するようにして文脈長毎にClassifyクラスを作るようにする
class Classify:
    def __init__(self, context):
        self.w2v = functions.load_w2v(consts.W2V_PATH)
        self.context = int(context)

    def classify(self, texts):
        print('Classify')
        print(texts)

    
if __name__ == '__main__':
    functions.reset_seed()

    # word2vec読み込み
    w2v = functions.load_w2v(consts.W2V_PATH)
    # vocab = w2v.wv.vocab
    # keys = vocab.keys()
    # print(w2v['おはよう'])

    # 試しにRNN_Bottomでclassify
    model_bottom = models.RNN_SINGLE()
    model_top = models.RNN_FINETUNING()

    base = os.path.dirname(os.path.abspath(__file__))
    path_bottom = os.path.normpath(os.path.join(base, '../data/models/bottom/nsteplstm0best.model'))
    path_top = os.path.normpath(os.path.join(base, '../data/models/context3/top/nsteplstm0best.model'))
    serializers.load_npz(path_bottom, model_bottom)
    serializers.load_npz(path_top, model_top)

    texts = ['おはようございます','よろしくね','お元気ですか','へえー。']
    variables = functions.to_variable(texts, w2v)
    # print(type(variables[0]))
    ys = model_bottom(variables).data

    print(consts.ACTS[np.argmax(ys[0])])
    print(consts.ACTS[np.argmax(ys[1])])
    print(consts.ACTS[np.argmax(ys[2])])
    print(consts.ACTS[np.argmax(ys[3])])

    bottoms, tops = functions.load_models(3)
    ys_bottom = [bottom(variables).data for bottom in bottoms]
    print(ys_bottom)
