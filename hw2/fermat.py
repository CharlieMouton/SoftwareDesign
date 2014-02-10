# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:40:58 2014
Exercise 5.3 - fermat 
@author: CharlieMouton
"""

def check_fermat(a,b,c,n):
    
    if a**n+b**n == c^n and n>2:
        print 'Holy smokes, Fermat was wrong!'
    else:
        print "No, that doesn't work"
        