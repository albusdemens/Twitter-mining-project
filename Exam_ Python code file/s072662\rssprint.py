"""
Author: Lars Kristensen, s072662
"""

import sys
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup as BS
import re

"""
Reads an RSS feed, and stores the categories in a dictionary, indicating 
the number of ocurrences for each category. 
NOTE: This method is currently not used. It is to be expanded later, for
statistics on categories.
"""
def Topics(feedUrl):
    topics = dict()    
    webpage = urlopen(feedUrl).read()
    pattern = re.compile('<category>(.*)</category>')
    
    categories = re.findall(pattern, webpage)
    
    for cat in categories:
        if cat in topics:
            topics[cat] += 1
        else:
            topics[cat] = 1
    return topics


"""
Reads an RSS feed, and prints the paragraphs, of the first 3 entries in the
RSS feed.
"""
def PrintArticles(feedUrl):
    print 'Fetching articles from: ' + feedUrl + '\n\n'
    
    try:
        webpage = urlopen(feedUrl).read()
        
        patternTitle = re.compile('<title>(.*)</title>')
        patternLink = re.compile('<link>(.*)</link>')
        
        Titles = re.findall(patternTitle, webpage)
        Links = re.findall(patternLink, webpage)
        
        articleIter = []
        articleIter[:] = range(1,4)
        
        for index in articleIter:
            print '---' + Titles[index] + '---'
                    
            content = urlopen(Links[index]).read()
            articleStart = content.find('<section class="body">')
            article = content[articleStart:(articleStart + 1000)]
            
            soup = BS(article)
            
            paragraphs = soup.findAll('p')
            for p in paragraphs:
                print p
            print '\n'
    except:
        print '\n-ERROR-'
        print 'An error occurred - Are you sure the specified input is an RSS feed?'
        

"""
A link to an RSS feed can be provided when running the Main method. If nothing
is specified, a default feed is used.
"""
if __name__ == "__main__":
    feed = 'http://www.version2.dk/it-nyheder/rss'

    if len(sys.argv) > 1:
        feed = sys.argv[1]
        
    PrintArticles(feed)    