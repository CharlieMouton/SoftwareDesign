# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:34:57 2014

@author: pruvolo
"""

# you do not have to use these particular modules, but they may help
from random import randint
import Image
import math

def build_random_function(min_depth, max_depth):
    """ Creates a function with a set minimum and maximum depth. This depth 
        determines how many nested functions are allowed to exist.  We will be 
        using the building blocks of prod, cos, sin, x, y, square, and abs. 
        
        This function returns A, a list containing nested lists that can be 
        processed to produce a randomly generated algorithm.
    """
    depth1 = ['x','y']                                               # if depth is 1, you will return either x or y
    if max_depth == 1:                                               # if max_depth is 1, (BASE CASE)
        return depth1[randint(0,1)]                                  # then return a random variable from x or y
    depth = randint(min_depth,max_depth)                             # set a depth that is between min and max depth
    bb = ['avg','square','cos_pi','sin_pi','X','Y','prod']           # a list containining all building blocks
    b = randint(0,6)                                                 # b chooses a random element in bb
    if b < 4 and b > 0:                                              # if b selects a command that takes one input
        A = [bb[b],build_random_function(depth-1,depth-1)]           # set up a list that is two long
    else:                                                            # Otherwise, 
        A = [bb[b],build_random_function(depth-1,depth-1),build_random_function(depth-1,depth-1)] #set up a list that is three long

    return A                                                         # return the list
    

def evaluate_random_function(f, x, y):
    """ This function takes as input, f, a list that contains many commands to perform tasks, x, the x value that we will look at, and y, the y value
    that we will look at when performing the function, f. This function will process the commands in f and execute them, and then output the value that 
    results from the following functions.
    """
    
    if f[0] == 'x':                                                  # A series of if statements that check which building block
        return x        #BASE CASE                                   # is at the beginning of the list, and then performing that math
    if f[0] == 'y':     
        return y        #BASE CASE
    # next two cases seem very redundant. What's the point of doing it?
    if f[0] == 'X':
        return evaluate_random_function(f[1],x,y)
    if f[0] == 'Y':
        return evaluate_random_function(f[2],x,y)
    if f[0] == 'avg':
        return ((evaluate_random_function(f[1],x,y)+(evaluate_random_function(f[2],x,y)))/2)
    if f[0] == 'square':
        return (evaluate_random_function(f[1],x,y))**2               #
    if f[0] == 'cos_pi':
        return math.cos(math.pi*evaluate_random_function(f[1],x,y))
    if f[0] == 'sin_pi':
        return math.sin(math.pi*evaluate_random_function(f[1],x,y))
    if f[0] == 'prod':
        return evaluate_random_function(f[1],x,y)*evaluate_random_function(f[2],x,y)

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Maps the input value that is in the interval[input_interval_start, input_interval_end]
        to the output interval [output_interval_start, output_interval_end].  The mapping
        is an affine one (i.e. output = input*c + b).
    
        This function is useful for converting values from one number series to another, and 
        will be very useful in creating your random picture.
    """
    n = float((val-input_interval_start))/float((input_interval_end-input_interval_start)) # division of the difference of val from input_interval_start and the total diff of input_interval
    
    return output_interval_start+n*(output_interval_end-output_interval_start) # then converting from that to the output interval


def random_picture(filename):
    """
        This function takes as a input the filename to save the photo as, and calculates
        a randomly generated picture based off of three randomly built functions for each
        color channel.        
    """
    fred = build_random_function(5,7)                              # a random function for the red channel
    fblue = build_random_function(10,15)                           # a random function for the green channel
    fgreen = build_random_function(8,10)                           # a random function for the blue channel
    
    im = Image.new('RGB',(1600,900))                               # create a new image to use as canvas
    pix = im.load()                                                # create a pixel map to work with
    x = 0                                                          # reset iteration variable
    while x < 1600:                                                # iterate x from 0 to 1600
        y = 0                                                      # reset iteration variable
        while y < 900:                                             # iterate y from 0 to 900
            # most certainly break the next three lines up so they're readable
            R = remap_interval(evaluate_random_function(fred,remap_interval(x,0,1600,-1,1),remap_interval(y,0,900,-1,1)),-1,1,0,255) # uses remap and evaluate to find the R value at this pixel
            G = remap_interval(evaluate_random_function(fblue,remap_interval(x,0,1600,-1,1),remap_interval(y,0,900,-1,1)),-1,1,0,255) # uses remap and evaluate to find the G value at this pixel
            B = remap_interval(evaluate_random_function(fgreen,remap_interval(x,0,1600,-1,1),remap_interval(y,0,900,-1,1)),-1,1,0,255) # uses remap and evaluate to find the B value at this pixel
            pix[x,y] = (int(R),int(G),int(B))                      # assigns the values to that pixel using a duble
            y = y + 1                                              # iteration addition equation
        x += 1                                                     # iteration addition equation
        
    im.save(filename)                                              # save the new image as the input filename
    im.show()                                                      # using imagemagick, display the image
    
    