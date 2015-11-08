# -*- coding: utf-8 -*-

from pattern.web import Twitter
from pattern.en import tag
from pattern.vector import KNN, count
import urllib2

twitter = Twitter()
knn = KNN()


def getSearchWords():
    '''Function that returns list of search words'''
    # Test data, we will use synonyms for war (found in nltk word net)
    words = ['war', 'conflict', 'jihad', ]
    return words


def getCountries():
    '''Function that returns list of countries
       downloaded from static url.
    '''
    url = r'https://raw.github.com/umpirsky/' \
          'country-list/master/country/cldr/en/country.csv'
    response = urllib2.urlopen(url)
    # TODO, check encoding
    data = response.read()
    country_data = data.split('\n')
    country = country_data[1]
    countries = []
    for country in country_data[1:]:
        if country:
            split_country = country.split(',')
            countries.append(split_country[1])
    # Test data
    # countries = ['Syria', 'Egypth', 'Iraq',]
    return countries[:20]  # Only get data for 20 first countries when testing


def getTweets(words, countries):
    tweets = []
    for word in words:
        for country in countries:
            results = twitter.search('%s AND %s' % (word, country),
                                     start=1,
                                     count=10
                                     )
            tweets.extend(results)
    return tweets.items()


def main():
    words = getSearchWords()
    # print getCountries()
    countries = getCountries()
    tweets = getTweets(words, countries)
    return tweets


if __name__ == '__main__':
    print main()
