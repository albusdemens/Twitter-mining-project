#the intention is to create an web scraper that finds articles and performs supervised learning to classify them based on style of the source medium
import urllib2
from urllib2 import *
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
from BeautifulSoup import BeautifulSoup


def articlefromurl(url): 
  script=urlopen(url).read()#reads html of article at given url
  script=nltk.clean_html(script)#removes html markup
  return script

def wordfreq(text):
  text=text.split()# splits text on spaces returning words
  return Counter(text) #counts occurrences of each word

  
def listarticles(url):#at newyorker.com every html linked to from the front page is an article, this function lists links with .html extension
  html=urllib2.urlopen(url)
  soup=BeautifulSoup(html)
  articles=[]#instantiates list
  for item in soup.findAll('a'):
    if item.get('href').split('.')[-1]=="html": #tests for .html extension
      articles.append(item.get('href')) #appends url for articles
  return articles

ai=raw_input(["please enter url: "])#prompt for front page from which to get articles
a=listarticles(ai)

b=[] #list of articles
for article in a:
  b.append(articlefromurl(ai+article))


#two crude comparison algorithms
def comparevocabsize(art1,art2):
  if len(wordfreq(art1)/len(art1)>len(wordfreq(art2)/len(art2):#compares number of different words used per length of article
    return art1
  else: 
    return art2 

def compareNN(art1,art2):#compares number of adverbs used
  1=nltk.pos_tag(art1)#part of speech tagging art1, creates a tuple for every word where the 0th item is the word and the 1st item is the part of speech
  2=nltk.pos_tag(art2)
  1counter=0
  2counter=0
  for i in 1:
    if i[1]=='RB': 1counter+=1 #counts occurrences of 'RB' which means adverb
  for j in 2:
    if j[1]=='RB':2counter+=1
  if 1counter/len(art1)>2counter/len(art2):
    return art1
  else: 
    return art2 #prevalence of adverbs is a common indicator of style, this function compares 2 articles and returns the one with higher insidence of adverbs per word
