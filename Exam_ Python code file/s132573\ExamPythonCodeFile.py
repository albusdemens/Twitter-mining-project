from __future__ import division
import  math, numpy

#if this file is saved the same place that a script is run from you can import the functions from this file

def hamming(a,b):
#finds hamming distance between two vectors of same length
    c=0
    for i in range(1,len(a)): 
        if not a[i]==b[i]:
            c+=1
    return c

def euclidean(a,b):
#finds the euclidean distance between two vectors of same length
    c=0
    for i in range(1,len(a)):
        c+=(a[i]-b[i])**2
    return math.sqrt(c)

def vectorops2v(a,b):
#makes usefull vector operations with variables as lists
    a1=numpy.array(a)
    b1=numpy.array(b)
    add=a1+b1
    dotp=numpy.dot(a1,b1)
    print 'a+b=',add
    print 'dot product=',dotp 
    if len(a)==2 or len(a)==3:
        crossp=numpy.cross(a1,b1)
        print 'cross product=',crossp
    retrun add,dotp

def vectorops3v(a,b,c):
#makes usefull vector operations with variables as lists
    a1=numpy.array(a)
    b1=numpy.array(b)
    c1=numpy.array(c) 
    if len(a)==2 or len(a)==3:
        if len(b)==2 or len(b)==3:
            crossp=numpy.cross(b1,c1)
            if len(a)==len(b):
                if len(a)==len(c):
                    scaltrib=numpy.dot(a1,crossp)
                    print 'Scalar triple product=',scaltrib
                else:
                    print 'Scalar triple product is not computable for selected vectors'
            vecttrib=numpy.cross(a1,crossp)
            print 'Vector tripple product=',vecttrib
        else: 
            print 'Length of vectors must be 2 or 3'
    else:
        print 'Length of vectors must be 2 or 3'
    return vecttrib

