# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/cmouton/.spyder2/.temp.py
"""

def exclusive_or_dict(dict1,dict2):
    dictres = {}
    
    for entry in dict1:
        print entry
        if entry in dict2:
            pass
        else:
            dictres[entry] = dict1[entry]
            
    for entry in dict2:
        print entry
        if entry in dict1:
            pass
        else:
            dictres[entry] = dict2[entry]
            
    print dictres
    
exclusive_or_dict({'a':5,'b':3},{'a':7,'c':3})