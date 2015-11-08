# -*- coding: utf-8 -*-

# Python script for reading and possible futher analysis of articles from the danish newspaper, Politiken.

from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
import re

# We import "urlopen" to read the url from Politiken.dk. 're' is used for the regular expressions in the article, to extract the relevant parts.
# BeautifulSoup is a module that will be very convenient in order to deal with the articles.

webpage = urlopen('http://politiken.dk/nyheder/')
# The website is downloaded.

content  = webpage.read()
encoding = webpage.headers['content-type'].split('charset=')[-1]
# This line gives the variable 'encoding' the value 'ISO-8859-1', which enables us to read the text as Unicode.

ucontent = unicode(content, encoding)
# Transform to Unicode.

PolitikTitles  = re.compile('<a href="http://politiken.dk/politik/ECE.*">([\w\s]*)</a>',re.UNICODE)
OekonomiTitles = re.compile('<a href="http://politiken.dk/oekonomi/ECE.*">([\w\s]*)</a>',re.UNICODE)
SportsTitles   = re.compile('<a href="http://politiken.dk/sport/ECE.*">([\w\s]*)</a>',re.UNICODE)

# Politics, economics and Sports articles titles  are now found by using the html source kode from politiken.dk and regular-expressions 
# The titles are followed by a link to the article and is encapsulated by a '>' and a '</a>. '([\w\s]*)' makes sure that the text in between
# consists of either word-characters, spaces or newlines, such that we only find the titles.


findPolTit   = re.findall(PolitikTitles,ucontent)
findOekTit   = re.findall(OekonomiTitles,ucontent)
findSportTit = re.findall(SportsTitles,ucontent)


# Regular Expressions' 're.findall'-function is now used to find all the places in the html-code that match the string defined by 're.compile'
# In this way, we obtain a list of all the articles.

PolLinks    = re.compile('<a href="(http://politiken.dk/politik/ECE.*)">[\w\s]*</a>',re.UNICODE)
OekLinks    = re.compile('<a href="(http://politiken.dk/oekonomi/ECE.*)">[\w\s]*</a>',re.UNICODE)
SportsLinks = re.compile('<a href="(http://politiken.dk/sport/ECE.*)">[\w\s]*</a>',re.UNICODE)

findPolLinks    = re.findall(PolLinks,ucontent)
findOekLinks    = re.findall(PolLinks,ucontent)
findSportsLinks = re.findall(PolLinks,ucontent)

# Above, the links to the articles are found in a similar way. The string we try to match is identical to the one used to find the article itself. In this way we
# ensure that the articles and their corresponding links get the same indices in the list. only the paranthesis has to be moved so that we save the part
# that we are interested in.

# In the following we will try to find all the article text for articles about politics:

for i in range(1,len(findPolLinks)):
    print findPolTit[i] 
    print findPolLinks[i]
    print '\n'
    
    # Here, the articles titles and links are printed below each other, in pairs.
    
    PolArtpage = urlopen(findPolLinks[i]).read()
    BeginRead  = PolArtpage.find('<div id="art-body"')
    PolArt     = PolArtpage[BeginRead:(BeginRead+3000)]
    
    # The relevant part of the article is found (in the case with Politiken it is everything that comes after '<div id="art-body"' in the code, which is where
    # the article text begins.
    
    soup = BeautifulSoup(PolArt)
    
    Paragraphs = soup.findAll('p')
    
    # Now, finally BeautifulSoup is used to find all the places in the article where '<p>' is. That is, whenever a paragraph starts.
    
    for i in Paragraphs:
        print i
        
    print '\n'
    print '\n'
    
    # Her we do a for-loop inside the other, to show all the paragraphs in the articles, below title and link.
    # The entire for-loop then prints title, link, and all the paragraps in the article, which is outputted.
    
    # Hereafter, one can, for example, use the found articles for sentiment analysis.

# Christian Kragh, 3-10-2013.
