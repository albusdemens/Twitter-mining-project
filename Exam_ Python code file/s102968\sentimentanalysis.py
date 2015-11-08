# -*- coding: utf-8 -*-
import operator
"""
Created on Wed Oct 02 23:00:28 2013

@author: Kaare Rievers
"""
"""
This script is to be used in sorting out the sentiment in tweets
And is therefore to be used with another script, fetching tweets from twitter
For this script, a dummy tweet was used.
"""
text = 'obama is awesome, ??obama sucks, #obama is eating a potato'
text2 = list(text)

for a in xrange(len(text2)):
    char = text2[a]
    if char.isalpha():
        continue
    elif char =='-':
        continue
    else:
        text2[a] =' '
        
text = ''.join(text2)
print ''.join(text2)

words = text.split()
print words

""" 
Finn Aarup Nielsen has created code for sentiment analysis, 
this is used for this script and is available from
http://www2.imm.dtu.dk/pubdb/views/publication_details.php?id=6010
"""

sentiment = dict(map(lambda (k,v): (k,int(v)),
                     [ line.split('\t') for line in open("AFINN-111.txt") ]))

def obama(w):
    try:
        return sentiment[w]
    except:
        return 0

def sentimentAna(value):
    if value <0:
        return 'negative'
    elif value>0:
        return 'postive'
    else:
        return 'neutral'

tweetValue = 0;
values = map(obama, words)
tweetValue = reduce(operator.add, values,0)
print 'The sentimental value of the tweet is:'
print tweetValue
print 'Which means it is ' + sentimentAna(tweetValue)

