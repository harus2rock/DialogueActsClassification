# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 14:12:55 2019

@author: izumi
"""

from __future__ import unicode_literals
import re
import unicodedata
import os
import chainer
from chainer.cuda import cuda
from chainer import Variable
import pickle
from gensim.models import word2vec
import MeCab
import numpy as np
import random
from tqdm import tqdm
import copy

import sys
import chainer.functions as F
import chainer.links as L
from chainer import optimizers,Chain,serializers
from chainer.cuda import to_cpu

from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import pandas as pd
import csv

"""
好きな発話から推定する．
"""

# 定数
GPU = -1       # 使用:0 不使用:-1
EPOCH = 400
BATCH_SIZE = 400
CONTEXT = 2    # 考慮する文脈の数
LAYERS = 1     # nsteplstmの層の数
IN = 200       # 入力次元数
UNITS = 200    # nsteplstmの出力次元数
DROPOUT = 0.5  # ドロップアウト率
L1_REGULARIZATION = -1 # L1正則化を使うかどうか
L2_REGULARIZATION = -1 # L2正則化を使うかどうか
UNDERSAMPLING = 100000  # ある対話行為の上限サンプル数
CLEAN = 0 # 使用:0 不使用:-1
CHANGE = -1   # 話者交代の情報を使う:0 使わない:-1
CHANGE_MODE = -1 # 話者交代のタイミングで1:-1 話者によって変更:0
MECAB = -1 # MeCab使用:0 Sentence Piece使用:-1
EARLY = 40 # early stopping
TYPE = 1 # 0:9次元のみ 1:9+200次元 2:9+800次元
BEST = 0 # 今までのベストモデル使用:0 不使用:-1

VERSION = '0/' # 下段RNNのうちどれを使うか
FILENAME = '0' # 上段RNNのうちどれを使うか
FILE = '0' # FILENAME内の2値分類器
CONNECT = '1' # 何番目のファイルか

xp = np

def reset_seed(seed=0):
    random.seed(seed)
    np.random.seed(seed)
    if cuda.available:
        cuda.cupy.random.seed(seed)


# 文書を正規化する関数群
def unicode_normalize(cls, s):
    pt = re.compile('([{}]+)'.format(cls))

    def norm(c):
        return unicodedata.normalize('NFKC', c) if pt.match(c) else c

    s = ''.join(norm(x) for x in re.split(pt, s))
    s = re.sub('－', '-', s)
    return s

def remove_extra_spaces(s):
    s = re.sub('[ 　]+', ' ', s)
    blocks = ''.join(('\u4E00-\u9FFF',  # CJK UNIFIED IDEOGRAPHS
                      '\u3040-\u309F',  # HIRAGANA
                      '\u30A0-\u30FF',  # KATAKANA
                      '\u3000-\u303F',  # CJK SYMBOLS AND PUNCTUATION
                      '\uFF00-\uFFEF'   # HALFWIDTH AND FULLWIDTH FORMS
                      ))
    basic_latin = '\u0000-\u007F'

    def remove_space_between(cls1, cls2, s):
        p = re.compile('([{}]) ([{}])'.format(cls1, cls2))
        while p.search(s):
            s = p.sub(r'\1\2', s)
        return s

    s = remove_space_between(blocks, blocks, s)
    s = remove_space_between(blocks, basic_latin, s)
    s = remove_space_between(basic_latin, blocks, s)
    return s

# 文章正規化
def normalize_neologd(s):
    s = s.strip()
    s = unicode_normalize('０-９Ａ-Ｚａ-ｚ｡-ﾟ', s)

    def maketrans(f, t):
        return {ord(x): ord(y) for x, y in zip(f, t)}

    s = re.sub('[˗֊‐‑‒–⁃⁻₋−]+', '-', s)  # normalize hyphens
    s = re.sub('[﹣－ｰ—―─━ー]+', 'ー', s)  # normalize choonpus
    s = re.sub('[~∼∾〜〰～]', '', s)  # remove tildes
    s = s.translate(
        maketrans('!"#$%&\'()*+,-./:;<=>?@[¥]^_`{|}~｡､･｢｣',
              '！”＃＄％＆’（）＊＋，－．／：；＜＝＞？＠［￥］＾＿｀｛｜｝〜。、・「」'))

    s = remove_extra_spaces(s)
    s = unicode_normalize('！”＃＄％＆’（）＊＋，－．／：；＜＞？＠［￥］＾＿｀｛｜｝〜', s)  # keep ＝,・,「,」
    s = re.sub('[’]', '\'', s)
    s = re.sub('[”]', '"', s)
    return s



# RNN_Bottom用
class RNN_SINGLE(Chain):
    def __init__(self, n_layers=LAYERS, n_w2vlen=IN, n_units=UNITS, n_tag=9, dropout=DROPOUT):
        """
        n_tag    : ラベルの次元
        """
        super(RNN_SINGLE, self).__init__()
        
        # パラメータを持つ層の登録
        with self.init_scope():
            self.xh = L.NStepBiLSTM(n_layers, n_w2vlen, n_units, dropout)
            self.hh = L.Linear(n_units*2, 100*2)
            self.hy = L.Linear(100*2, n_tag)
        
    def __call__(self, xs):
        """
        x       : list(Variable)
        x.shape : [(文書の単語数, 200)] * batchsize
        y       : Variable
        y.shape : batchsize * 9
        """
        #  FILENAME=0
        hy, _, _ = self.xh(None, None, xs)
        h = F.concat(F.concat(F.split_axis(hy, 2, axis=0),axis=2),axis=0)
        h = F.dropout(F.relu(self.hh(h)))
        y = self.hy(h)
        return y

# RNN_Top用
class RNN_FINETUNING(Chain):
    def __init__(self, n_layers=LAYERS, n_in=IN*2, n_units=UNITS*2, n_tag=9, dropout=DROPOUT):
        super(RNN_FINETUNING, self).__init__()
        
        # パラメータを持つ層の登録
        with self.init_scope():
            self.xh = L.NStepBiLSTM(n_layers, n_in, n_units, dropout)
            self.hy1 = L.Linear(n_units*2, 100*2)
            self.hy2 = L.Linear(100*2, n_tag)
            
    def __call__(self, xs):
        """
        xs : list(Variable)
        y  : xp.array
        """
        hy, _, _ = self.xh(None, None, xs)
        h = F.relu(F.concat(F.concat(F.split_axis(hy, 2, axis=0),axis=2),axis=0))
        h = F.dropout(F.relu(self.hy1(h)))
        y = self.hy2(h)
        return y
    
# 2値分類層
class RNN_TOP(Chain):
    def __init__(self, n_layers=LAYERS, n_in=IN*2, n_units=UNITS*2, n_tag=9, dropout=DROPOUT):
        super(RNN_TOP, self).__init__()
        
        # パラメータを持つ層の登録
        with self.init_scope():
            self.xh = L.NStepBiLSTM(n_layers, n_in, n_units, dropout)
            self.h_100_self = L.Linear(n_units*2, 100*2)
            self.h_1_self = L.Linear(100*2,1)
            self.h_100_qyn = L.Linear(n_units*2, 100*2)
            self.h_1_qyn = L.Linear(100*2,1)
            self.h_100_qw = L.Linear(n_units*2, 100*2)
            self.h_1_qw = L.Linear(100*2,1)
            self.h_100_ayn = L.Linear(n_units*2, 100*2)
            self.h_1_ayn = L.Linear(100*2,1)
            self.h_100_aw = L.Linear(n_units*2, 100*2)
            self.h_1_aw = L.Linear(100*2,1)
            self.h_100_res = L.Linear(n_units*2, 100*2)
            self.h_1_res = L.Linear(100*2,1)
            self.h_100_fil = L.Linear(n_units*2, 100*2)
            self.h_1_fil = L.Linear(100*2,1)
            self.h_100_con = L.Linear(n_units*2, 100*2)
            self.h_1_con = L.Linear(100*2,1)
            self.h_100_req = L.Linear(n_units*2, 100*2)
            self.h_1_req = L.Linear(100*2,1)
            
    def __call__(self, xs, act):
        """
        xs : list(Variable)
        y  : xp.array
        """
        hy, _, _ = self.xh(None, None, xs)
        h = F.relu(F.concat(F.concat(F.split_axis(hy, 2, axis=0),axis=2),axis=0))

        if act == 0:
            h = F.dropout(F.relu(self.h_100_self(h)))
            y = self.h_1_self(h)
        elif act == 1:
            h = F.dropout(F.relu(self.h_100_qyn(h)))
            y = self.h_1_qyn(h)
        elif act == 2:
            h = F.dropout(F.relu(self.h_100_qw(h)))
            y = self.h_1_qw(h)
        elif act == 3:
            h = F.dropout(F.relu(self.h_100_ayn(h)))
            y = self.h_1_ayn(h)
        elif act == 4:
            h = F.dropout(F.relu(self.h_100_aw(h)))
            y = self.h_1_aw(h)
        elif act == 5:
            h = F.dropout(F.relu(self.h_100_res(h)))
            y = self.h_1_res(h)
        elif act == 6:
            h = F.dropout(F.relu(self.h_100_fil(h)))
            y = self.h_1_fil(h)
        elif act == 7:
            h = F.dropout(F.relu(self.h_100_con(h)))
            y = self.h_1_con(h)
        elif act == 8:
            h = F.dropout(F.relu(self.h_100_req(h)))
            y = self.h_1_req(h)
        return y

class RNN_CONNECT_AT(Chain):
    def __init__(self, n_layers=LAYERS, n_in=IN*2, n_units=UNITS*2, dropout=DROPOUT):
        super(RNN_CONNECT_AT,self).__init__()
        
        with self.init_scope():
            self.xh = L.NStepBiLSTM(n_layers, n_in, n_units, dropout)
            self.hy1 = L.Linear(n_units*2, 100*2)
            
            self.h_100_self = L.Linear(n_units*2, 100*2)
            self.h_100_qyn = L.Linear(n_units*2, 100*2)
            self.h_100_qw = L.Linear(n_units*2, 100*2)
            self.h_100_ayn = L.Linear(n_units*2, 100*2)
            self.h_100_aw = L.Linear(n_units*2, 100*2)
            self.h_100_res = L.Linear(n_units*2, 100*2)
            self.h_100_fil = L.Linear(n_units*2, 100*2)
            self.h_100_con = L.Linear(n_units*2, 100*2)
            self.h_100_req = L.Linear(n_units*2, 100*2)
            
            self.at = L.Linear(100*2, 1)
#            self.at1 = L.Linear(100*2, 100) # 200->100->1じゃなくて200->1でもいいかも
#            self.at2 = L.Linear(100, 1)
            
            self.out = L.Linear(100*2, 9) # 200->9じゃなくて200->100->9でもいいかも
#            self.out1 = L.Linear(100*2,100)
#            self.out2 = L.Linear(100, 9)
            
    def __call__(self, xs):
        """
        xs : list(Variable)
        y  : Variable
        """
        # _/_/_/RNN_Top(Bi-LSTM)
        hy, _, _ = self.xh(None, None, xs) # shape:(2,batch,units)
        h1 = F.relu(F.concat(F.concat(F.split_axis(hy, 2, axis=0),axis=2),axis=0)) # shape:(batch,units*2)

        # relu
        # _/_/_/FC
        h = F.relu(self.hy1(h1)) #shape:(batch,100*2)
        h = F.split_axis(h, h.shape[0],axis=0) #tuple:(batch,1,100*2)
        
        # _/_/_/FC for twoclass
#        h_self = F.relu(self.h_100_self(h1)) #shape:(batch,100*2)
#        h_self = F.split_axis(h_self, h_self.shape[0],axis=0) #tuple:(batch,1,100*2)
#        h_qyn = F.relu(self.h_100_qyn(h1))
#        h_qyn = F.split_axis(h_qyn, h_qyn.shape[0],axis=0)
#        h_qw = F.relu(self.h_100_qw(h1))
#        h_qw = F.split_axis(h_qw, h_qw.shape[0],axis=0)
#        h_ayn = F.relu(self.h_100_ayn(h1))
#        h_ayn = F.split_axis(h_ayn, h_ayn.shape[0],axis=0)
#        h_aw = F.relu(self.h_100_aw(h1))
#        h_aw = F.split_axis(h_aw, h_aw.shape[0],axis=0)
#        h_res = F.relu(self.h_100_res(h1))
#        h_res = F.split_axis(h_res, h_res.shape[0],axis=0)
#        h_fil = F.relu(self.h_100_fil(h1))
#        h_fil = F.split_axis(h_fil, h_fil.shape[0],axis=0)
#        h_con = F.relu(self.h_100_con(h1))
#        h_con = F.split_axis(h_con, h_con.shape[0],axis=0)
#        h_req = F.relu(self.h_100_req(h1))
#        h_req = F.split_axis(h_req, h_req.shape[0],axis=0)
        
        # reluなし
        # _/_/_/FC
#        h = self.hy1(h1) #shape:(batch,100*2)
#        h = F.split_axis(h, h.shape[0],axis=0) #tuple:(batch,1,100*2)
        
        # _/_/_/FC for twoclass
        h_self = self.h_100_self(h1) #shape:(batch,100*2)
        h_self = F.split_axis(h_self, h_self.shape[0],axis=0) #tuple:(batch,1,100*2)
        h_qyn = self.h_100_qyn(h1)
        h_qyn = F.split_axis(h_qyn, h_qyn.shape[0],axis=0)
        h_qw = self.h_100_qw(h1)
        h_qw = F.split_axis(h_qw, h_qw.shape[0],axis=0)
        h_ayn = self.h_100_ayn(h1)
        h_ayn = F.split_axis(h_ayn, h_ayn.shape[0],axis=0)
        h_aw = self.h_100_aw(h1)
        h_aw = F.split_axis(h_aw, h_aw.shape[0],axis=0)
        h_res = self.h_100_res(h1)
        h_res = F.split_axis(h_res, h_res.shape[0],axis=0)
        h_fil = self.h_100_fil(h1)
        h_fil = F.split_axis(h_fil, h_fil.shape[0],axis=0)
        h_con = self.h_100_con(h1)
        h_con = F.split_axis(h_con, h_con.shape[0],axis=0)
        h_req = self.h_100_req(h1)
        h_req = F.split_axis(h_req, h_req.shape[0],axis=0)
        
        # _/_/_/全結合層1層目を全部くっつける
        hs = [] # shape:(b,10,100*2)
        for h1,s,qy,qw,ay,aw,r,f,c,r in zip(h,h_self,h_qyn,h_qw,h_ayn,h_aw,h_res,h_fil,h_con,h_req):
            hs.append(F.concat([h1,s,qy,qw,ay,aw,r,f,c,r], axis=0))
        
        """
        A : 内積取らずにattention計算
        """
        
        # _/_/_/attention計算
        concat_hs = F.concat(hs, axis=0) # (10*b,100*2)
        # 1層でattention計算
        attn = F.tanh(self.at(concat_hs))
        # 2層でattention計算
#        attn = F.relu(self.at1(concat_hs)) # leaky_reluでもいいかも
#        attn = self.at2(attn) # (10*b,1)
        
        sp_attn = F.split_axis(attn, len(hs), axis=0) # tuple:(b,10,1)
        sp_attn_pad = F.pad_sequence(sp_attn, padding=-1024.0) #(b,10,1)
        attn_softmax = F.softmax(sp_attn_pad, axis=1)
                
        # _/_/_/形をそろえてbroadcast
        hs_pad = F.pad_sequence(hs, length=None, padding=0.0) # (b,10,100*2)
        hs_pad_reshape = F.reshape(hs_pad, (-1, hs_pad.shape[-1])) # (10*b,100*2)
        
        attn_softmax_reshape = F.broadcast_to(F.reshape(attn_softmax, (-1, attn_softmax.shape[-1])), hs_pad_reshape.shape) # (10*b,100*2)
        
        # _/_/_/attentionを出力にかけてsoftmax方向に足す！
        attention_hidden = hs_pad_reshape * attn_softmax_reshape # (10*b,100*2)
        attention_hidden_reshape = F.reshape(attention_hidden, (len(hs), -1, attention_hidden.shape[-1])) # (b,10,100*2)
        
        result = F.sum(attention_hidden_reshape, axis=1) # (b,100*2)
        
        """
        B : 内積とってattention計算
        """
#        hs = F.concat([F.expand_dims(h, axis=0) for h in hs], axis=0) # (b,10,100*2)
#        # _/_/_/attention計算
#        score = F.batch_matmul(hs, hs, transb=True)
#        scale_score = 1. / UNITS ** 0.5
#        score = score * scale_score # scaled dot-product
#        attention = F.softmax(score, axis=2)
#        
#        # _/_/_/加重平均とってsoftmax方向に足してtanh！
#        c = F.batch_matmul(attention, hs)
#        result = F.tanh(F.sum(c, axis=1))
        
        """
        出力
        """
        
        # _/_/_/出力層
        # 1層で出力
        y = self.out(result)
        # 2層で出力
#        y = F.dropout(F.relu(self.out1(result)))
#        y = self.out2(y)
        return y

# 同じ名前の層のみパラメータをコピー        
def copy_model(src, dst):
    assert isinstance(src, Chain)
    assert isinstance(dst, Chain)
    for child in src.children():
        if child.name not in dst.__dict__: continue
        dst_child = dst[child.name]
        if type(child) != type(dst_child): continue
        if isinstance(child, Chain):
            copy_model(child, dst_child)
        if isinstance(child, chainer.Link):
            match = True
            for a, b in zip(child.namedparams(), dst_child.namedparams()):
                if a[0] != b[0]:
                    match = False
                    break
                if a[1].data.shape != b[1].data.shape:
                    match = False
                    break
            if not match:
                print('Ignore %s because of parameter mismatch' % child.name)
                continue
            for a, b in zip(child.namedparams(), dst_child.namedparams()):
                b[1].data = copy.deepcopy(a[1].data)
            print('Copy %s' % child.name)
            
def classify(model, keys, utterances):
    print('classify')
    
            
if __name__ == '__main__':
    print('main')