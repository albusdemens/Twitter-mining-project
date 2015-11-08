# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 11:34:46 2013
"""

import re
import time
import robotparser
import urllib2
from bs4 import BeautifulSoup

regex = re.compile(
        r'^(?:http|ftp)s?://' 
        # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' 
        #domain...
        r'localhost|' 
        #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' 
        # ...or ip
        r'(?::\d+)?' 
        # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

regex_recipes=re.compile(
        r'(?:http://allrecipes.com/Recipe/(?:[A-Z0-9-])*)',re.IGNORECASE)
        #domain for recipes

regex_recipes_block=re.compile(
        r'(http://allrecipes.com/Recipe/(?:[A-Z0-9]-*)*)',re.IGNORECASE)
        #normalize the recipe code



def isValidUrl(url):
#function to check if the url is valid one
    if regex.match(url) is not None:
        return True;
    return False
    
def isRecipe(url):
#function to check if the url is within the recipe's domain
    if regex_recipes.match(url) is not None:
        if "reviews.aspx" not in url:
        #take out reviews because it's not useful for us
            return True;
        return False;
    return False
    
def isBlock(url):
#function to normalize the recipe code
    match = regex_recipes_block.match(url)
    return match.group(1)

def crawler(SeedUrl):
    tocrawl=[SeedUrl]
    #urls to be crawled
    crawled=[]
    #urls already crawled
    match=[]
    #urls we want
    rp = robotparser.RobotFileParser()
    rp.set_url(SeedUrl)
    rp.read()
    #for reading the restric domains in robots.txt
    opener = urllib2.build_opener()
    #set up url opener
    opener.addheaders = [("User-agent", "phuangbotforeducation (Po-Hao Huang)")]
    #set up user agent for administrter to recognize
    f = open('test_urls_allrecepies.txt', 'a+')
    #open files to write
    while tocrawl:
    #the crawler continues to crawling when there are still urls not being crawled yet
        page=tocrawl.pop()
        #pop next url for crawling
        pagesource=opener.open(page)
        s=pagesource.read()
        soup=BeautifulSoup(s)
        links=soup.findAll('a',href=True)
        #using Beautifulsoup to parse urls out from html of the crawling url                    
        if page not in crawled:
        #check if this page hasn't been crawled yet
            for l in links:
            #go through all links with in this page                 
                if isValidUrl(l['href']):
                #check if the link is valid
                    if rp.can_fetch("*",l['href']) and isRecipe(l['href']):
                    #check if the link can be fetch and is a recipe link
                        tocrawl.append(l['href'])
                        #if so,add it to tocrawl list
                        temp = isBlock(l['href'])
                        if temp not in match:
                        #if it is not yet recorded and it is a recipe link
                            match.append(temp)
                            #add to list to show it has been mached 
                            print 'Find-OK:'+temp
                            #message to oberserve the crawling
                            f.write(temp+'\n')
                            #write the recipe into txt file
            time.sleep(1)
            #delay 1 sec after crawling one page
            print 'Crawled:'+page
            crawled.append(page)
            #add the crawled page to list
    f.close()
    #close the file     
    return 
    
crawler('http://allrecipes.com/Recipe/Chicken-Parmesan/')