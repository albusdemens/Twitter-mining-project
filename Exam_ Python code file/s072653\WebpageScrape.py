# -*- coding: utf-8 -*-
"""
Module Simple Webpage Scraper
"""

__version__ = 1.00
__author__ = "s072653"
__all__ = ["TextScrapeModule"]

import nltk 
import requests 
import urlparse
import robotparser

class TextScrapeModule:
    """
    The TextScrape module takes an input of webpages. The module will try to
    find a robot.txt file for the corresponding hostname, thus determine
    whether or not download is allowed. If the page exist and can be 
    downloaded, the basic html will be removed, and a wordlist is saved.
    
    The module uses the natural language toolkit to find a frequency
    distribution, and use this to generate a plot of the 50 most used 
    words from the prevously downloaded pages.
    
    >>> textScraper = TextScrapeModule()
    >>> textScraper.urllist = ['google.dk/search', 'http://google.dk', 'tv2.dk']
    >>> textScraper.scrape()
    Downloaded 2 of 3
    2
    
    """
    def __init__(self, urllist=None):
        if (urllist == None):
            self.urlist = []
        else:
            self.urllist = urllist
        self.pages = []
        self._robotfiles = {}

    def scrape(self):
        """
        Attempt to download a wordlist for each specified url. 
        Returns the amount of succesful page downloads. 
        """
        #pylint: disable=E1103 
        
        if(self.urllist == None or len(self.urllist) == 0):
            raise Exception("No webpages has been specified")
        succes_count = 0
        
        for url in self.urllist:        
            data = self.__http_download(url)
            if (data == None or not data.ok):             
                continue
            
            succes_count += 1
            self.pages.append((url, nltk.word_tokenize(
                nltk.clean_html(data.content))))
                
        print "Downloaded %d of %d" % (succes_count, len(self.urllist))
        return succes_count
        
    def plot_wordfrequency(self):
        """
        Calculate the wordfrequency for all words saved and outputs a 
        graph of the 50 most used words. 
        """
        if(len(self.pages) == 0):
            return
            
        words = []
        for page in self.pages:
            words.extend(page[1])
            
        word_dist = nltk.FreqDist([w.lower().encode('ascii', errors='replace') 
                                      for w in words])
                
        word_dist.plot(50, cumulative=False)
       
        
    def __http_download(self, url_string):
        """
        returns a reponse object if page exist and if allowed by 
        the corresponding robots.txt file. 
        """
        
        try:
            if(url_string[:7] != "http://"):
                url_string = "http://" + url_string
            
            if (self.__is_allowed(url_string)):               
                return requests.get(url_string, 
                                    headers={"User-Agent": 
                                        "student@Dtu_bot/0.1"})
                
        except requests.exceptions.RequestException:
            pass
        return None

    def __is_allowed(self, url_string):
        """
        return a boolean value of whether or not a page download is allowed
        based on the robots.txt file. If no file is available, true
        is assumed. 
        """
        try:
            host = urlparse.urlparse(url_string).hostname
            if(not self._robotfiles.has_key(host)):
                robo = robotparser.RobotFileParser()
                robo.set_url("http://" + host + "/robots.txt")
                robo.read()
                self._robotfiles[host] = robo
            return self._robotfiles[host].can_fetch("*", url_string)     
        except IOError:
            return True        

if __name__ == "__main__":
    import doctest
    doctest.testmod()