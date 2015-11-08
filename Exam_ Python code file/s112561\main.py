import re
import urllib
import cPickle as pickle
import os.path

from BeautifulSoup import BeautifulSoup

class Course:
    def __init__(self, name, id, level):
        self.name = name
        self.id = id
        self.level = level
        self.description = dict()


    def __str__(self):
        return "Name: " + self.name + "\nID: " + self.id + "\nLevel: " + self.level

    def __repr__(self):
        return "Name: " + self.name + "\nID: " + self.id + "\nLevel: " + self.level

    
def readFromTuple(tuple):
        return Course(tuple[0], tuple[1], tuple[2])


def dumpit(variable, filename):
    pickle.dump(variable, open(filename, 'w'))


def loadit(filename):
    return pickle.load(open(filename))


def fetchBaseCourseInfo(forceRefresh=False):
    if(os.path.isfile('baseCourseInfo.p') and not forceRefresh):
        return loadit("baseCourseInfo.p")
    else:
        url = 'http://www.kurser.dtu.dk/search.aspx?lstTeachingPeriod=E1;E2;E3;E4;E5;E1A;E2A;E3A;E4A;E5A;E1B;E2B;E3B;E4B;E5B;E,F1;F2;F3;F4;F5;F1A;F2A;F3A;F4A;F5A;F1B;F2B;F3B;F4B;F5B;F,January,June,SummerSchool&YearGroup=2013-2014&btnSearch=Search'
        pages = urllib.urlopen(url)
        soup = BeautifulSoup(pages)

        courseNumberList = soup.findAll('div', style="padding-bottom:4px")
        courseLevelList = soup.findAll('td', style="vertical-align:top;padding:4px")

        baseCourseInfo = list();
        for i in range(len(courseNumberList)):
            id = courseNumberList[i].find('a')['href'][:5].encode('ascii', 'ignore')
            name = courseNumberList[i].find('a').string[8:].encode('ascii', 'ignore')
            level = courseLevelList[i].strong.string.encode('ascii', 'ignore')
            baseCourseInfo.append(Course(name, id, level))
        dumpit(baseCourseInfo, 'baseCourseInfo.p')
        return baseCourseInfo

def clearWhiteSpace(text):
    return re.sub(r'\s{2,}', " ", text)

def parseCoursePage(course):
    url = 'http://www.kurser.dtu.dk/' + course.id + '.aspx?menulanguage=en-gb'
    page = urllib.urlopen(url)
    soup = BeautifulSoup(page)
    courseViewer = soup.find('div', 'CourseViewer')

    courseDescription = dict()
    for table in courseViewer.findChildren('table'):
        tableEntries = map(lambda x: x.string.strip(), table.findAll('h3'))
        #Determine which table is which
        if('Language:' in tableEntries):
            for entry in table.findAll('tr'):
                if(len(entry.findAll('h3')) != 0):
                    title = entry.h3.string.strip().replace(":", "")
                    value = clearWhiteSpace(entry.text.replace(entry.h3.string.strip(),""))
                    courseDescription[title] = value
        if('Schedule:' in tableEntries):
            scheduleInfoTable = table

    for entry in courseViewer.findChildren('div', ''):
        if(entry.h3):
            title = entry.h3.string.strip().replace(":", "")
            value = clearWhiteSpace(entry.text.replace(entry.h3.string.strip(),""))
            courseDescription[title] = value
    course.description = courseDescription
    return course

#This method uses the url for the search for all courses to figure out the most basic
#info of the course, that is the ID, Name and Level (bachelor, master,...) of the course.
baseCourseInfo = fetchBaseCourseInfo()

#ParseCoursePage takes in a course and retrieves its description page and parses it for
#a very detailed description of the course. The parsing function is still incomplete, it
#treats new lines rather badly as it is now so a lot of words merge together. The info 
#can be accessed through the dictionary 'description'.

allCourses = map(parseCoursePage, baseCourseInfo)