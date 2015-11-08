# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 20:21:00 2013

@author: Jeppe
"""

try:
    import urllib3 as urllib
except ImportError:
    try:
        import urllib2 as urllib
    except ImportError:
        import urllib as urllib

import string #Pylint warning is a known bug: http://www.logilab.org/ticket/2481
import re
import os

FILE_PATH = "%s" + os.sep + "%s.txt"

class CourseCrawler:
    """Class for crawling the DTU course pages 
    to recieve all course ids and their raw HTML page"""
    
    opener = urllib.build_opener()
    opener.addheaders = [("User-agent","Participants of course 02819")]    
    baselink = ("http://www.kurser.dtu.dk/search.aspx"
                        "?YearGroup=2013-2014"
                        "&btnSearch=Search"
                        "&menulanguage=en-GB"
                        "&txtSearchKeyword=%s")
    course_baselink = "http://www.kurser.dtu.dk/%s.aspx?menulanguage=gb-en"
    
    def __init__(self, search_directory="course_search_results", 
                 course_directory="course_pages"):
        self.search_dir = search_directory
        self.course_dir = course_directory
        
    def download_coursebase_courses(self, force_download=False):
        """Query the DTU coursebase for all courses. It is not possible to
        simply get all courses in one page, therefore the method searches for
        courses containing the letters a-z one by one. 
        
        It stores the raw HTML search results as a.txt, b.txt etc.
        
        As default it only downloads pages which are not already downloaded.
        However setting forceDownload=True will force it to download everything.
        
        Everything is stored in the class' init search directory.
        """
        for letter in string.ascii_lowercase:
            # If True. Download searchpage, even if it exist.
            if force_download:
                print 'Forced search for courses with searchkey: %s' % letter
                content = self.__get_page_content(self.baselink % letter)
                self.save_txt_in_file(self.search_dir, letter, content)
            # If False. Only download searchpage, if not exist.
            elif not self.exist_txt_file(self.search_dir, letter):
                print 'Search for courses with searchkey: %s' % letter
                content = self.__get_page_content(self.baselink % letter)
                self.save_txt_in_file(self.search_dir, letter, content)
            
    def get_course_ids_from_files(self):
        """Extracts all course IDs from the downloaded raw html pages from
        the DTU coursebase. Returns the IDs in a Set."""
        course_ids = set()
        # Loops over a-z and searches for courses.
        for letter in string.ascii_lowercase:
            if self.exist_txt_file(self.search_dir, letter):
                content = self.get_txt_from_file(self.search_dir, letter)
                letter_search_courses = self.__get_course_ids(content)
                course_ids.update(letter_search_courses)
                print ("Courses for search %s: %s" % 
                    (letter, len(letter_search_courses))) 
        return course_ids
        
    def download_all_course_pages(self, force_download=False): 
        """Downloads all the course pages from the coursebase and stores 
        the raw HTML pages in the class' init course directory. 
        
        Remember to download the coursebase course list first"""
        for course_id in self.get_course_ids_from_files():
            # If True. Download coursepage, even if it exist.
            if force_download:
                print 'Forced download of course page with ID: %s' % course_id
                content = self.__get_page_content(self.course_baselink % 
                                                    course_id)
                self.save_txt_in_file(self.course_dir, course_id, 
                                           content)      
            # If False. Only download coursepage, if not exist.
            elif not self.exist_txt_file(self.course_dir, course_id):
                print 'Download of course page with ID: %s' % course_id
                content = self.__get_page_content(self.course_baselink %
                                                    course_id)
                self.save_txt_in_file(self.course_dir, course_id, content) 
     
    def __get_page_content(self, url):
        """Requests a website by an URL and returns its raw content."""
        try:
            page = self.opener.open(url)
        except IOError, message:
            print "There was an error loading requested page: %s" % message
        content = page.read()
        return content
        
    @staticmethod   
    def __get_course_ids(text):
        """Returns a list with everything between <a href=" AND 
        .aspx?menulanguage=en-gb, which is the the course IDs"""
        pattern = r'<a href="(.*?).aspx\?menulanguage=en-gb'
        course_ids = set()
        course_ids.update(re.findall(pattern, text))
        return course_ids
        
    @staticmethod        
    def exist_txt_file(directory, filename):
        """Checks if a file exist in the init directory.
        Returns True if exist, otherwise False"""
        current_file_path = FILE_PATH % (directory, filename)
        if os.path.isfile(current_file_path):
            return True
        else: 
            return False

    @staticmethod
    def save_txt_in_file(directory, filename, text):
        """Saves a text as a .txt file in a given directory"""
        if not os.path.exists(directory):
            os.makedirs(directory)
        current_file_path = FILE_PATH % (directory, filename)
        with open(current_file_path, 'w') as txtfile:
            txtfile.write(text)
    
    @staticmethod
    def get_txt_from_file(directory, filename):
        """Loads a file by filename in a given directory 
        and returns its raw content."""
        current_file_path = FILE_PATH % (directory, filename)
        with open(current_file_path, 'r') as txtfile:
            return txtfile.read()
                            

CRAWLER = CourseCrawler()
CRAWLER.download_coursebase_courses()
CRAWLER.download_all_course_pages()
COURSE_IDS = set(CRAWLER.get_course_ids_from_files())
print "Total number of courses: %s" % len(COURSE_IDS)
#print course_ids