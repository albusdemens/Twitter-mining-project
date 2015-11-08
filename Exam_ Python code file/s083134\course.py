# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 10:31:28 2013

@author: Tomasz
"""

try:
    import urllib3 as urllib # There is nothing called urllib3
except ImportError:
    try:
        import urllib2 as urllib # urllib2 might be installed
    except ImportError:
        import urllib as urllib

try:
    import BeautifulSoup as bs
except ImportError, message:
    print "There was an error loading BeautifulSoup: %s" % message
    
import re, os

class Course:
    """
    Class for fetching and parsing DTU course pages from an course ID or from
    locally stored raw HTML pages.
    """
    opener = urllib.build_opener()
    opener.addheaders = [("User-agent","Participants of course 02819")]    
    baselink = "http://www.kurser.dtu.dk/%s.aspx?menulanguage=gb-en"
    
    def __init__(self, course_id, course_directoty="course_pages", 
                 fetch_local=True):
        self.course_id = course_id
        
        if (fetch_local == True):
            self.content = self.__fetch_page_local(self.course_id, 
                                                   course_directoty)
        else:
            self.content = self.__fetch_page_inet(self.course_id)
            
        (self.blocking_courses, self.qualified_prerequisites, self.text, 
         self.title, self.department) = (self.parse_raw_page(self.content))
    
    def __fetch_page_local(self, course_id, course_dir):
        """
        Method to fetch DTU course page from a given course ID and directory
        containing the HTML source for the course.
        
        File format must be <course_dir>\\<course_id>.txt
        """
        return self.get_txt_from_file(course_dir, course_id)
        
    def __fetch_page_inet(self, course_id):
        """
        Method to fetch DTU course page from a given course ID
        """
        
        url = self.baselink % course_id
        try:
            page = self.opener.open(url)
        except IOError, message:
            print "There was an error loading course page: %s" % message
        return page.read()
    
    @staticmethod
    def get_title_from_raw(raw_page):
        """
        Gets the course title from the raw HTML source
        """
        
        if not raw_page:
            raise Exception("raw_page is empty!")
            
        # get the title (it is always in the only h2 tag)
        title = bs.BeautifulSoup(raw_page).find("h2").string
        # remove the course number and remove excessive whitespaces
        title = re.sub(r"\d{5}", "", title).strip()
        return title   
    
    def get_text_from_raw(self, raw_page):
        """
        Gets the course description from the raw HTML source
        """

        if not raw_page:
            raise Exception("raw_page is empty!")        
        
        text = ""
        for section in bs.BeautifulSoup(raw_page).findAll(
                                            "div", attrs={"class":"section"}):
            header = section.find("h3")
            if header:
                if "Responsible" in header.string:
                    continue
                elif "Green challenge participation" in header.string:
                    continue
            
            text += self.__remove_html_markup(str(section))
        return text
    
    def parse_courses(self, raw_page):
        """
        Get the blocking courses to a course and the qualified prerequisites
        from the raw HTML source
        """

        if not raw_page:
            raise Exception("raw_page is empty!")        
        
        # Only interested in divs
        soup = bs.BeautifulSoup(raw_page, 
                                parseOnlyThese=bs.SoupStrainer('div'))
        
        # get XPath /html/body/form/div[2]/table/tbody/tr[7]/td/table/tbody/
        # tr[3]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div
        # /div/div and get the tables in the CourseViewer class
        
        soup = bs.BeautifulSoup(
            str(soup.find(attrs={"class":"CourseViewer"})), 
            parseOnlyThese=bs.SoupStrainer("table"))
            
        # find the tables with style="table-layout:fixed" as last one is always
        # the one we are interested in
        tables = soup.findAll(name="table", 
                              attrs={"style":"table-layout:fixed"})
        
        blocking_courses = set()
        qualified_prerequisites = set()
        
        # find all table rows
        for row in tables[len(tables) -1].findAll("tr"):
            # find all columns in row
            # information is always stored in two columns
            cols = row.findAll("td")
            index = 0
            for col in cols:
                # find the header
                header = col.find("h3")
                if header:
                    # Blocking courses
                    if "Not applicable" in header.string:
                        not_applicable = cols[index + 1]
                        courses = re.compile(r"\d{5}").findall(
                                                    str(not_applicable))
                        blocking_courses = set(courses)
                    # Qualified prerequisites
                    if "Qualified" in header.string:
                        qualified = cols[index + 1]
                        courses = re.compile(r"\d{5}").findall(str(qualified))
                        qualified_prerequisites = set(courses)
                        if self.course_id in qualified_prerequisites:
                            qualified_prerequisites.remove(self.course_id)
                index += 1
        return blocking_courses, qualified_prerequisites
    
    @staticmethod    
    def parse_department(raw_page):
        """
        Gets the department from the raw HTML source
        """
        if not raw_page:
            raise Exception("raw_page is empty!")
        
        # Find all tables
        soup = bs.BeautifulSoup(raw_page, 
                                parseOnlyThese=bs.SoupStrainer('table'))
                                
        # Department is always contained in class="SubTableLevel2"
        table = soup.find('table', attrs={'class': 'SubTableLevel2'})
        # and is always contained in the first row
        row = table.findAll("tr")[0]
        # and is always contained in the second column
        department = row.findAll("td")[1]
        return department.string.strip()
        
    
    def parse_raw_page(self, raw_page):
        """
        Parses the raw page using BeautifulSoup, to get the course
        prerequisites, blocking courses, title and department.
        """
        if not raw_page:
            raise Exception("raw_page is empty!")
        
        blocking_courses, qualified_prerequisites = self.parse_courses(
                                                                    raw_page)
        
        text = unicode(self.get_text_from_raw(raw_page), errors='ignore')
        title = unicode(self.get_title_from_raw(raw_page))
        
        department = unicode(self.parse_department(raw_page))
        
        return (blocking_courses, qualified_prerequisites, text, title,
                department)
            
    @staticmethod
    def __remove_html_markup(html_string):
        """
        Nice method to remove html markup from string borrowed from:
        http://stackoverflow.com/a/14464381/368379
        input is a string containing HTML, what it returns is a string without
        any HTML tags
        """
        tag = False
        quote = False
        out = ""
    
        for char in html_string:
            if char == '<' and not quote:
                tag = True
            elif char == '>' and not quote:
                tag = False
            elif (char == '"' or char == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + char
        return out

    @staticmethod        
    def get_txt_from_file(directory, filename):
        """
        Loads a file by filename in a given directory 
        and returns its raw content.
        """
        current_file_path = "%s%s%s.txt" % (directory, os.sep, filename)
        with open(current_file_path, 'r') as txtfile:
            return txtfile.read()

### Sample usage ###
# pylint: disable=C0103  
c = Course("02819", "", False)
print "Title: %s" % c.title
print "Course: %s" % c.course_id
print "Department: %s" % c.department
print "Blocking courses: %r" % c.blocking_courses
print "Qualified prerequisites: %r" % c.qualified_prerequisites
####################