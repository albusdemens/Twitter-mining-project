"""
Module

"""

__version__ = 0.01
__author__ = "Christian Graver Larsen"
__all__ = ["WebpageTester"]

import urllib2
import re

class WebpageTester(str):
    """
    >>> web = WebpageTester('http://google.com')
    >>> print web.numberOfExOnPage('div')
    115

    >>> print web.isNumberOfHtmlElementsEven('div')
    False
    """
    def __init__(self,str):

        #Add user-agent to the request to avoid bot blocks.
        user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'

        #Building the request
        req = urllib2.Request(str, None, { 'User-Agent' : user_agent })

        #sending the request to the web page
        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError, err:
            if err.code == 404:
                print "Page not found!"
            elif err.code == 403:
                print "Access denied!"
            else:
                print "Something happened! Error code", err.code
        except urllib2.URLError, err:
            print "Some other error happened:", err.reason

        #Saving response string to instance
        self.page = response.read()

    def printPage(self):
        """
        Print the response
        """
        print self.page

    def numberOfExOnPage(self,ex):
        """
        Find number of expressions(ex) on page
        """
        return len(re.findall(ex,self.page))

    def isNumberOfHtmlElementsEven(self, element):
        """
        Finds if number of specified html elemet (element) is even (return true) or odd (return false)
        """
        if len(re.findall(element,self.page))%2==0:
            return True
        else:
            return False