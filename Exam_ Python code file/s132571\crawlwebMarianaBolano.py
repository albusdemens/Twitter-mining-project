from __future__ import division
__author__ =  'Mariana Bolano - S132751'

#!/usr/bin/python
# -*- coding: utf-8 -*-

'''This python script is able to open a given url, get all the text, remove html coding, tokenize words, remove unwanted words and punctuation, and prints the words depended on frequency in the terminal . Running it saves the list of tokenized words and part of speech tagged words in txt files.'''

import re
import numpy as np
import nltk
from urllib import urlopen
import matplotlib.pyplot as plt


### select and define data sets and lists 
url = "http://www.brainpickings.org/index.php/2012/05/08/100-ideas-that-changed-graphic-design/"  # website to be used

wordsX = ['facebook', 'rss', 'email', 'twitter', 'SoundCloud', 'Amazon', 'RSS', '#', 'Popova', 'Pickings','Maria', 'Boston' , 'Josh', 'Subscribe']  #list of unwanted words
punctuation =re.compile(r'[.?,":;]')  # list of punctuation to be removed from text


### load data 
html = urlopen(url).read().lower()   # open url , read, convert to lowercase and store to a list
raw = nltk.clean_html(html)    # clean the data from html 
tokens =nltk.word_tokenize(raw)  # create a list of tokenized text 
tags = nltk.pos_tag(tokens)     # use pos tagger to tokenize the text.a tuple


### saves the list of tokens and pos tagged words into text files
tokenizedwords = np.savetxt('tokenizedwords.text',tokens, fmt="%s")
postaggedw = np.savetxt('postaggedwords.text',tags,fmt="%s")  


freq_dic = {}  # create dictionary to store frequent words and counts

for i in tokens:   # for every element in the tokenized text list
     if i in wordsX:   # if the element/token is in the unwanted word list
         tokens.remove(i)   #remove it


### store the words and frequency in the dictionary
for i in tokens: 
    i = punctuation.sub("",i)  #remove punctuation
    try: 
        freq_dic[i] += 1
    except: 
        freq_dic[i] = 1 


freq_list = freq_dic.items()  # create a list of pairs for words and frequency
freq_list.sort()   # sort by key or value


###visualize results

#create a list of the occurencies of words that appear more than once
freq=[]
for i in freq_dic.values():
    if i != 1:
        freq.append(i)

#create a list of the words with occurencies more than once
fkeys=[]
for i in freq_dic.keys():
    if i not in freq:
        ((freq_dic.keys()).remove(i))
        fkeys.append(i)

#print frqlist.shape , len(freq_list)  # shape = 731, 2  tokens = 1731 , reduced = 1696 
        
#print tokens
#print tags
#print      tokens[:100]      # len(tokens) # 6041

print ' Those are frequent words found in the website brainpickings.org, a website about reading and creative writing' 
