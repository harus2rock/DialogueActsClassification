# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 14:12:55 2019

@author: izumi
"""
import numpy as np
import consts
import models
import functions

"""
好きな発話から推定する．
"""

xp = np
            
def classify(model, keys, utterances):
    print('classify')
    
if __name__ == '__main__':
    functions.reset_seed()
    print('main')
    import models as output
    output_text_class = output.output_text()
    output_text_class.output_date(1)
    print(consts.CONST_TEST)