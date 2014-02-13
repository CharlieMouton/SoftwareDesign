# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Charlie Mouton
    with assistance by: Stack Overflow, Paul Ruvolo, and official Python docs
"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons
from random import shuffle

def collapse(L):
    """ Converts a list of strings to a string by concatenating all elements of the list """
    output = ""
    for s in L:
        output = output + s
    return output

def cut_into_codons(dna):
    
    index = 0
    A = [0]*(len(dna)/3)                    #introduces the list to store our divided input
    while index<(len(dna)/3):               # we are periodically looking at three at a time
       A[index] = dna[3*index :3*index+3]   # assigning the first three letters to a string in a list
       index = index + 1                    # working the index
    S = [dna[3*index:len(dna)]]
    return A+S

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment
    """
    A = cut_into_codons(dna)
    
    i = 0                                   # establishing initial for indexing which string to access in A
    x = [0] * len(A)                        # establishing initial for seeing where 
    ans = [0] * len(A)

    while i < len(A):                       # while loop to look at different elements in list, A
        j = 0                               # establishing initial for indexing which list in Codons to access
        while j < len(codons):              # while loop to look at different lists in list, codons
            templist = codons[j]            # a temporary list of codons[j]
            k = 0                           # establishing initial for indexing through this list, codons[j]
            while k < len(templist):        # while loop to look through list, codons[j], looking for matches with A[i]
                 if templist[k] == A[i]:    # does templist[k] = A[i], if it matches, 
                     x[i] = j               # store where it happens in codons
                 #print k
                 k = k + 1                  # indexing addition for k    
            j = j + 1                       # indexing addition for j
        ans[i] = aa[x[i]]                   # what amino acids are these related too?
        i = i + 1                           # indexing addition for i
    return collapse(ans)                    # condense the answer into one string

    


def coding_strand_to_AA_unit_tests(inp,expout):
    """ Unit tests for the coding_strand_to_AA function """
    
    answer = coding_strand_to_AA(inp)       # run the actual program
    print 'input:' + inp                    # display the input
    print 'expected output:' + expout       # display what the user expected to be the output
    print 'actual output:' + answer         # display what is actually the output

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    """
    i = 0                                   # establishing initial for indexing which value in dna we are accessing
    dnac = [0]*len(dna)                     # establishing the list for the ans
    while i < len(dna):
        if dna[len(dna)-1-i]=='A':          # bad way to switch to the complement
            dnac[i] = 'T'
        elif dna[len(dna)-1-i]=='T':
            dnac[i] = 'A'
        elif dna[len(dna)-1-i]=='C':
            dnac[i] = 'G'
        elif dna[len(dna)-1-i]=='G':
            dnac[i] = 'C'
        i = i + 1
        
    return collapse(dnac)
   
    
def get_reverse_complement_unit_tests(inp,expout):
    """ Unit tests for the get_complement function """
        
    answer = get_reverse_complement(inp)    # run the actual program
    print 'input:' + inp                    # display the input
    print 'expected output:' + expout       # display what the user expected to be the output
    print 'actual output:' + answer         # display what is actually the output

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    """
    F = cut_into_codons(dna)                # cutting my input into codons to process it
    i = 0                                   # resetting i for indexing
    stopvalue = len(F)-1                    # the value that we cut out input. defaulted to return whole string
    while i < len(F):                       # while loop to change which codon we are looking at
        if F[i] == 'TGA' or F[i] == 'TAA' or F[i] == 'TAG': #checks to see if the codon we are at is a stop codon
            stopvalue = i                   # make not of where the stop codon is
            break                           # stop the while loop because we are at the stop codon
        i = i + 1                           # iteration addition equation
        
    return collapse(F[0:stopvalue])         # return dna from the start to the stop codon            
    

def rest_of_ORF_unit_tests(inp,expout):
    """ Unit tests for the rest_of_ORF function """

    answer = rest_of_ORF(inp)               # run the actual program
    print 'input:' + inp                    # display the input
    print 'expected output:' + expout       # display what the user expected to be the output
    print 'actual output:' + answer         # display what is actually the output 
        
def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence"ATGTGAA"
        returns: a list of non-nested ORFs
    """
    A = cut_into_codons(dna)               # make the input manageable            print i
    i = 0                                  # reset iteration variable
    xi = 0                                 # reset access variable for X
    X = [0]*len(A)                         # Initializes the workspace for X
    while i < len(A):                      # while loop that allows us to index looking through A
            if A[i] == 'ATG':              # searching for the start codon
                nstart = i                 # note the starting location of this sequence
                while i < len(A):          # while loop that looks for the end codon
                    if A[i] == 'TAG' or A[i] == 'TGA' or A[i] == 'TAA': # is this element the end codon?
                        break              # if so, break the current while loop
                    i = i + 1              # if not, let's look at the next element
                X[xi] = A[nstart:i]        # once we find the end codon, record that series of elements
                xi = xi + 1                # if we found one, then record the next one in the next section of X
            i = i + 1                      # iteration addition equation
    
    while 0 in X:                          # Does X have a bunch of zeros at the end?
        i = 0                              # reset the iteration variable
        while i < len(X):                  # Go through X,
            if X[i] == 0:                  # and if you find a element that is zero
                del X[i]                   # get rid of it.
            else:                          # if not,
                X[i] = collapse(X[i])      # collapse that element
            i = i + 1                      #  iteration addition variable
                                           # NOTE: due to the fact that del changes len(X), this method needs to
                                           # repeat until all zeroes are gone
            
    return X                               # YOU DID IT! =)
                
     
     
     
     
def find_all_ORFs_oneframe_unit_tests(inp,expout):
    """ Unit tests for the find_all_ORFs_oneframe function """

    answer = find_all_ORFs_oneframe(inp)    # run the actual program
    print 'input:',
    print inp                               # display the input
    print 'expected output:',
    print expout                            # display what the user expected to be the output
    print 'actual output:' ,
    print answer                            # display what is actually the output 

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    
    A = find_all_ORFs_oneframe(dna)          # run for regular dna
    dna = dna[1:]                            # drop the first term
    B = find_all_ORFs_oneframe(dna)          # run it again
    dna = dna[1:]                            # drop the second term
    C = find_all_ORFs_oneframe(dna)          # run it again

    return A+B+C                             # the concacenation of all the runs 
     

def find_all_ORFs_unit_tests(inp,expout):
    """ Unit tests for the find_all_ORFs function """
        
    answer = find_all_ORFs(inp)             # run the actual program
    print 'input:',
    print inp                               # display the input
    print 'expected output:',
    print expout                            # display what the user expected to be the output
    print 'actual output:' ,
    print answer                            # display what is actually the output

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
     
    A = find_all_ORFs(dna)                  # find all the ORFs for normal dna
    B = find_all_ORFs(get_reverse_complement(dna)) # find them all for the reverse complement
     
    return A+B                              # return the results

def find_all_ORFs_both_strands_unit_tests(inp,expout):
    """ Unit tests for the find_all_ORFs_both_strands function """

    answer = find_all_ORFs_both_strands(inp)# run the actual program
    print 'input:',
    print inp                               # display the input
    print 'expected output:',
    print expout                            # display what the user expected to be the output
    print 'actual output:' ,
    print answer                            # display what is actually the output

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string"""        
    A =  find_all_ORFs_both_strands(dna)   # Find all the ORFs
    B = [0]*len(A)                         # Initiates B, which will measure lengths
    i = 0                                  # reset the iteration variable, i
    while i < len(A):                      # while loop to set B = len(A)
        B[i] = len(A[i])                   # doing that equality
        i = i + 1                          # iteration addition equation
    n = max(B)                             # finding the longest element
    j = 0                                  # reset the iteration variable, j
    while j < len(B):                      # while loop for finding where the longest one was
        if n == B[j]:                      # is this element the longest one we found above?
            break                          # if so, break the loop
        j = j + 1                          # iteration addition equation
    return A[j]                            # return where in A the longest variable exists

def longest_ORF_unit_tests(inp,expout):
    """ Unit tests for the longest_ORF function """
 
    answer = longest_ORF(inp)               # run the actual program
    print 'input:',
    print inp                               # display the input
    print 'expected output:',
    print expout                            # display what the user expected to be the output
    print 'actual output:' ,
    print answer                            # display what is actually the output

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
   
    i = 0                                   # reset the iteration variable
    A = [0]*num_trials                      #initializing the list for the longest ORFs
    B = [0]*num_trials                      # intializing the list of how long those ORFs are
    while i < num_trials:                   # while loop that iterates through trials
        l_dna = list(dna)                   # converts dna into a list
        shuffle(l_dna)                      # scrambles the elements of l_dna
        A[i] = longest_ORF(collapse(l_dna)) # condenses and finds the longest ORF for each trials
        B[i] = len(A[i])                    # notes the length of the longest ORF
        i = i + 1                           # iteration addition equation

    return B                                # returns the lengths of the longest ORF in each trial

def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """

    A = find_all_ORFs_both_strands(dna)    # Finds all ORFs in our large sequence 
    i = 0                                  # reset the iteration variable
    while i < len(A):                      # while loop that looks through all the ORFS
        A[i] = coding_strand_to_AA(A[i])   # converts the ORFs to protein codes
        if len(A[i])< threshold/3:         # if that protein sequence is shorter than threshold/3, then it doesnt pass our threshold
            A[i] = 0                       # if it doesnt, set it to zero
        i = i + 1                          # iteration addition equation
    A = filter(lambda a: a != 0, A)        # filters out all those zeroes that we made before
    
    return A                               # returns a list of potential protein sequences