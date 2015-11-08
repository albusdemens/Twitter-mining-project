# -*- coding: utf-8 -*-
"""
Created on Tue Oct 01 14:15:46 2013

@author: alku
"""

import numpy

def calcDenomRV(data, type="orig"):
    vecdenom = []
    p = range(numpy.shape(data)[1])
    n = numpy.shape(data1)[0]
    combDenom = [(i,j) for i in p for j in p]
    for i in combDenom:
        elemdenom = numpy.square(numpy.cov(data[:,i[0]], data[:,i[1]])[0,1])
        if type=="mod":
           elemdenom -=  sum((data[:,i[0]] ** 2) * (data[:,i[1]]) ** 2)/numpy.square(n-1)
        vecdenom.append(elemdenom)
    return sum(vecdenom)
    

def RV(data1, data2, type="orig"):
    """
    Framework for RV coefficient. Computes original, modified 
    RV as in:
    C.-D. Mayer, J. Lorent, G.W. Horgan (2011). Exploratory Analysis of
    Multiple Omics Datasets Using the Adjusted RV Coefficient. Statistical
    Applications in Genetics and Molecular Biology. Vol 10, Issue 1, Article 14.
    
    <dataList> type list holding data arrays
    <mode> type string
    """
    
    n = numpy.shape(data1)[0]
    p1 = range(numpy.shape(data1)[1])
    p2 = range(numpy.shape(data2)[1])
    comb = [(i,j) for i in p1 for j in p2]
    
    #calculate numerator    
    vecnum = []   
    for i in comb:   
         elemnum = numpy.square(numpy.cov(data1[:,i[0]], data2[:,i[1]])[0,1])
         # for the modified
         if type=="mod":
             elemnum -=  sum((data1[:,i[0]] ** 2) * (data2[:,i[1]]) **2)/numpy.square(n-1)           
         vecnum.append(elemnum)
    num = sum(vecnum)
   
   #calculate denominator 1    
    denom1 = calcDenomRV(data1, type)
        
   #calculate denominator 2    
    denom2 = calcDenomRV(data2, type)
        
    
    RV = num/numpy.sqrt(denom1*denom2)
    
    return RV
    
######################################################################
####  TEST the RV coefficient
######################################################################
data1 = array([[ 52.31,  39.96,  36.63,  36.92,  30.13,  30.6 ,  47.08,  38.17,
         31.48,  48.88,  25.  ,  16.29,  43.6 ,  28.58,  20.31,  13.4 ],
       [ 57.63,  52.83,  35.25,  43.46,  44.69,  41.81,  64.77,  65.79,
         33.17,  58.77,  21.58,  11.35,  61.38,  56.73,  24.56,   9.6 ],
       [ 41.4 ,  41.58,  19.19,  54.15,  51.9 ,  54.46,  47.27,  41.88,
         29.69,  56.44,  16.9 ,  13.06,  41.42,  29.23,  17.92,  10.23],
       [ 64.75,  40.81,  43.54,  52.58,  52.19,  55.56,  56.52,  43.48,
         27.08,  52.63,  29.08,  30.17,  49.44,  30.48,  16.46,  22.9 ],
       [ 66.83,  46.92,  65.35,  79.65,  66.27,  78.35,  74.54,  41.96,
         21.4 ,  49.13,  69.42,  48.77,  66.31,  37.83,  17.67,  46.73]]);
         
         
###
         
data2 = array([[ 63.33,  67.17,  13.67,  53.83,  53.5 ,  55.33,  69.67,  29.,
         65.5 ,  76.33,  15.83,  29.67,  70.83,  20.33,  40.67,  42.17],
       [ 68.83,  77.33,  18.  ,  41.17,  40.5 ,  50.83,  69.83,  39.83,
         64.67,  66.83,  11.67,  17.33,  71.83,  37.83,  36.67,  45.5 ],
       [ 59.5 ,  25.67,  46.33,  68.83,  71.83,  75.17,  67.5 ,  26.5 ,
         58.17,  73.17,  20.  ,  44.5 ,  68.67,  22.  ,  50.67,  51.67],
       [ 74.  ,  37.17,  62.33,  65.83,  66.33,  68.5 ,  35.5 ,  20.5 ,
         36.5 ,  44.83,  15.5 ,  58.5 ,  47.17,  13.33,  30.17,  50.83],
       [ 63.33,  44.83,  44.67,  69.17,  73.17,  74.17,  66.33,  25.67,
         51.83,  59.67,  32.17,  67.17,  65.  ,  16.67,  51.33,  68.83]])        

### center the data
data1 = (data1 - data1.mean(axis=0)) #/ numpy.std(data1, axis=0, ddof=1)

data2 = (data2 - data2.mean(axis=0)) #/ numpy.std(data2, axis=0, ddof=1)



## test the function RV
RV(data1, data2, type="mod")

RV(data1, data2)
