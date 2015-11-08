# -*- coding: utf-8 -*-
"""

@author: s110848 Magdalena Furman

"""
from matplotlib.finance import quotes_historical_yahoo
from matplotlib.dates import num2date
import datetime
import httplib
import urllib2
import numpy
import pandas

"""
The code consist of class implementation, that has mathods able to acquire
data from Yahoo Finance about companies within the specified time frame.
Optionally you can download the list of companies for this url:

URL = "http://www.student.dtu.dk/~s110848/companylist.csv"

and perform the actions for all companies.

Sample execution:

>>>START = datetime.date(2013, 1, 10)
>>>NUM_DAYS = 10
>>>URL = "http://www.student.dtu.dk/~s110848/companylist.csv"
>>>SC = StockCrawl()
>>>SC.get_datelist_days(START, NUM_DAYS)
DateList initialized. From: 2013-01-10 To: 2013-01-19
>>>len(SC.date_list)
10
>>>SC.get_multi_stock(["GOOG","MSFT"])
Fetching: GOOG
Fetching: MSFT
Data cleaned from useless rows.
>>>SC.stock_data["MSFT"][0]
26.065835222978077
>>>SC.stock_data["MSFT"][date(2013, 1, 10)]
26.065835222978077
"""

class StockCrawl:
    """Class containing methods for collecting the stock data of the
    specified companies within the specified period of time.
    
    """

    def __init__(self):
        """Initialize"""
        self.date_list = []
        self.company_list = []
        self.stock_data = []
        self.temp_stock_data = []
        
    def get_datelist_days(self, start_date, days):
        """Generate a list of days within the specified date and the number of
        days. Stored in self.date_list.

        """
        self.date_list = [ start_date + datetime.timedelta(days = x) \
                           for x in xrange(0, days) ]
        print "DateList initialized. From: " + str(self.date_list[0]) + \
              " To: " + str(self.date_list[-1])
        
    def get_datelist_start_end(self, start_date, end_date):
        """Generate a list of days withing the specified start and end date"""
        delta = end_date - start_date
        self.get_datelist_days(start_date, delta.days)

    def get_csv_from_url(self, url):
        """Read the csv file containing the company names from url."""
        request = urllib2.Request(url)
        try: 
            response = urllib2.urlopen(request)
            self.company_list = pandas.DataFrame({"Companies" : \
            [line for line in response.read().split("\r\n")  \
            if (line != '' and line != "Companies") ]})
            print "Fetching data from " + url
        except urllib2.HTTPError, e:
            print 'HTTPError = ' + str(e.code)
        except urllib2.URLError, e:
            print 'URLError = ' + str(e.reason)
        except httplib.HTTPException, e:
            print 'HTTPException'
            
    def get_csv_content(self, filename):
        """Read the csv file. Content stored in self.company_list."""
        self.company_list = pandas.read_csv(filename)

    def get_stock_data(self):
        """Collect the stock data for specified companies. Save the closing
        stock prices for a specified period of time for a specified companies.
        Data stored in self.stock_data.

        """
        if self.date_list == [] :
            print "Please specify the list of dates to extract. Use method " \
            + "get_datelist_days to generate the date list and then use method "\
            + "get_stock_data."
            return

        if self.company_list.Companies.count() == 0:
            print "Please specify the list of companies to extract. Use " \
            + "method get_csv_content or get_csv_from_url to generate the " \
            + "list of companies and then use method get_stock_data."
            return### 

        temp_company_list = []
        # initialize the temporary company names list
        
        for single_company in self.company_list.Companies: 
            try:
                quotes = quotes_historical_yahoo(single_company, 
                                                 self.date_list[0],
                                                 self.date_list[-1])
                # get the data from yahoo finance
                quote_dict = dict( [ (single_date, numpy.nan) \
                         for single_date in self.date_list ] )
                # initialization of the dictionary with dates and nan values
                # so that we get all the dates at the end
                for row in quotes:
                    quote_dict[ num2date(row[0]).date() ] = row[1]
                # row[0] - date, row[1] - closing price
                self.temp_stock_data.append(quote_dict)
                temp_company_list.append(single_company)
            except urllib2.HTTPError:
                print 'Could not download data about: ' + single_company
            print "Fetching: " + single_company
        self.company_list = pandas.DataFrame({"Companies" : temp_company_list})
        self._to_pandas_table()
        self._clean_useless_rows()
        
    def get_single_stock(self, company_name):
        """Collect the stock data for specified company. Save the closing
        stock prices for a specified period of time for a specified companies.
        Data stored in self.stock_data.

        """ 
        self.company_list = pandas.DataFrame({"Companies" : [company_name]})
        self.get_stock_data()    
        
    def get_multi_stock(self, company_list):
        """Collect the stock data for a list of companies."""
        self.company_list = pandas.DataFrame({"Companies" : company_list})
        self.get_stock_data()
        
    def _clean_useless_rows(self):
        """Clean the useless rows in self.stock_data, such that weekends and
        off from work, that do not contain any stock information.

        """
        self.temp_stock_data = pandas.DataFrame()
        dates = []
        for i in xrange(0, self.stock_data[self.company_list.Companies.irow(0)].count()):
            #print i
            row = self.stock_data.irow(i)
            if len(row[numpy.isnan(row)]) == len(row):
                dates.append(self.date_list[i])
                
        for single_date in dates:
            self.stock_data = self.stock_data.drop(pandas.Timestamp(single_date))
        print "Data cleaned from useless rows."
        
    def save_data(self, filename):
        """Save the data stored in self.stock_data to a csv file.

        """
        self.stock_data.to_csv(filename)
    
    def _to_pandas_table(self):
        """Convert the data stored in self.stock_data to a pandas table.

        """
        temp = dict()
        column_names = self.company_list.Companies
        for i in xrange(0, len(column_names)):
            temp[column_names[i]] = self.temp_stock_data[i]
        self.stock_data = pandas.DataFrame(temp, index = self.date_list) 