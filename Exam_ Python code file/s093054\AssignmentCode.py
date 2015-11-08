# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 11:21:58 2013

@author: Martin
"""

#This bit of code writes a list of all primenumbers below 1000, 
#and writes the number of primes below 1000.
#NB: appearantly this does give the correct result when run by itself
#but not when running the entire file.
import math

def WritePrimesBelow(temp1):
    PrimeList = []
    for i in range(2,temp1+1):
        IsPrime = 1
        temp2 = int(math.ceil(i**(1/2)))
        for j in range(2,temp2+1):
            if i % j == 0 and j != i:
                IsPrime = 0
                break
        if IsPrime == 1:
            PrimeList += [i]
    x = len(PrimeList)
    print('All them prime numbers below ', temp1,' are:', PrimeList)
    print('The number of primes below ',temp1,' is ',x)
WritePrimesBelow(1000)


#Project Euler Problem 1
#This bit of code finds the sum of all multiples of 3 and 5 below 1000
def WriteMultiplesOf3And5Below(MultiplesBelow):
    NumberList = []
    for i in range(1,1000):
        if i%3 == 0 or i%5 == 0:
            NumberList += [i]
    ans = sum(NumberList)
    print('The sum of all multiples of 3 and 5 below 1000 is', ans)
WriteMultiplesOf3And5Below(1000)
            

#Project Euler Problem 2
#This bit of code finds the sum of all even Fibonacci numbers below 4000000
FibonacciList = [1,2]
while FibonacciList[-1] < 4000000:
    FibonacciList += [FibonacciList[-1] + FibonacciList[-2] ]
EvenFibList = []
for element in FibonacciList:
    if element%2 == 0:
        EvenFibList += [element]
answer = sum(EvenFibList)
print(answer)

#Project Euler Problem 56
#This bit of code finds (by using brute force) the largest sum of the 
#digits (base 10) in a number a^b, where a,b < 100.
def Euler56(Var):
    c = 0
    for a in range(1,Var):
        for b in range(1,Var):
            temp = str(a**b)
            tempSum = 0
            for digit in temp:
                tempSum = tempSum + int(digit)
                if tempSum > c:
                    c = tempSum
    print('The largest sum of digits is',c)
Euler56(100)


#This Program finds out if a number is Harshad
def isharshad( a ):
    b = str(a)
    d = 0
    for letter in b:     
        c = int(letter)
        d = d + c
    modad = a%d
    if  (modad == 0):
       print(b , ' is Harshad')
    else:
       print(b , ' is not Harshad')
isharshad(81)