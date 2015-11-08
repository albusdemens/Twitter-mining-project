#!/macports/bin/python
# -*- coding: utf-8 -*-

#
#### Python 3.3.2 (default, Sep 29 2013, 11:33:09) 
#### [GCC 4.2.1 Compatible Apple Clang 4.0 ((tags/Apple/clang-421.0.60))] on darwin
#
#### this program will definitively !!!NOT!!! work in any version of python below 3.1
#

__version__ = 0.03
__author__ = "s022518 - Bjarne D Mathiesen"
__all__ = ["getURL"]

import sysconfig
if float(sysconfig.get_python_version()) < 3.1:
    exit('your version of python is below 3.1')

import io
import re
import json
from lxml import etree      #### lxml     isn't a standard library
import httplib2             #### httplib2 isn't a standard library
http = httplib2.Http('httplib2.cache')
http.force_exception_to_status_code = True

def getURL (URL):
    '''
    GETs an URL and returns 
    -- the http status code (hopefully 200)
    -- a parsed html structure ready for further analysis with eg xpath
    '''

# override the 
# ++ cache-control: private, max-age=0 
# ++ outdated expires 
# that the DTU servers set in order to hit the cache
    headers= \
        {
         'cache-control': 'public, max-age=36000',
         'expires': 'Sun, 20 Sep 2014 07:41:11 GMT'
        }
    response, content = http.request(URL,headers=headers)
    parser = etree.HTMLParser()
    html   = etree.parse(io.BytesIO(content), parser)
    return response.status, html

if __name__ == '__main__':
    '''
    On the search page, Kursusdatabasen sends the results as
    an html document to the browser in which the courses are described
    in rows in an html table in this way :
    <tr style="background-color:#f1f1f1">
        <td style="padding:6px">
            <div style="padding-bottom:4px">
                <a href="01035.aspx?menulanguage=da" style="color:#990000;font-weight:bold">01035 - Matematik 2</a>
            </div>
            <div style="color:gray">
                <strong>Dansk | 5 ECTS | 2013/2014 | E1A (man 8-12) eller E2B (tors 8-12) eller F2B (tors 8-12)</strong>
            </div>
        </td>
        <td style="vertical-align:top;padding:4px">
            <strong>Bachelor</strong>
        </td>
    </tr>
    '''
#
# get every course from kursusdatabasen
    status, html = getURL('http://www.kurser.dtu.dk/search.aspx?lstTeachingPeriod=E1;E2;E3;E4;E5;E1A;E2A;E3A;E4A;E5A;E1B;E2B;E3B;E4B;E5B;E,F1;F2;F3;F4;F5;F1A;F2A;F3A;F4A;F5A;F1B;F2B;F3B;F4B;F5B;F&YearGroup=2013-2014&btnSearch=Search')
    if status != 200:
        exit('kursusdatabasen couldn\'t be loaded')

#
# Every course is uniquely defined by how the URL in the table row has been styled
# We can't use the <tr> to find all the courses, because the <tr>s are alternately
# coloured and not coloured
# Thus, the <a> tags are found, and we back up three levels to the <tr>
    kurser = html.xpath("//a[@style=\"color:#990000;font-weight:bold\"]/../../..")

    kursusInfo = {}

    for kursus in kurser:
        NavnNummer = kursus.xpath('.//a/text()')[0].split('-',maxsplit=1)   # '-' can also be in the course name so care must be taken only to split on the 1st '-'
        Info       = kursus.xpath('./td/div/strong/text()')[0].split('|')
        Niveau     = kursus.xpath('./td/strong/text()')
        kursusInfo[NavnNummer[0].strip()] = \
            {
             'navn'   : NavnNummer[1].strip(),
             'sprog'  : Info[0].strip(),
             'ects'   : re.findall(r"\d+\.?\d*",Info[1])[0],                # only the number of ECTS points are needed
             'årgang' : Info[2].strip(),
             'skema'  : Info[3].strip(),
             'niveau' : Niveau[0].strip()
            }

#
# just to show I can do it the result is stored in a json file
    with open('kursusInfo.json', mode='w', encoding='utf-8') as f:
        json.dump(kursusInfo,f,indent=4)

#
# Every course has a slightly different set of headings
# I want to find the complete set for use int the further analysis
# A set is used to store the values as I can just dump new values into it
# getting the advantage of automatic duplicate removal
    tagbag = set()
    for kursus in iter(kursusInfo.keys()):
        status , html = getURL('http://www.kurser.dtu.dk/'+kursus+'.aspx')
        if status != 200:
            break
        '''
        <tr>
            <td>
                <h3>Engelsk titel: </h3>
            </td>
            <td class="value">Advanced Engineering Mathematics 1 </td>
        </tr>
        '''
        tags = html.xpath("//h3/text()")
        for tag in tags:
            tagbag.update({tag.strip()})
    print(tagbag)
