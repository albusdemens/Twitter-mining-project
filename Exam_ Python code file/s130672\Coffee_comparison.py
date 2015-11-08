# October 2 2013, AC
# Coffee_comparison.py counts how many coffee-related tweets have been sent in Copenhagen and Stockholm in the last two days

from twitter import *

#In case you have problems with the previous command, download the 
#twitter package from https://pypi.python.org/packages/source/t/twitter/twitter-1.10.0.tar.gz
#and copy the files in the folder with this file

import sys
import os.path
import simplejson as json
import tweepy
import csv
from datetime import datetime, date, timedelta
import time
import numpy as np 
import pylab as pl
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

print ('Is Copenhagen more caffeinated than Stockholm or is it the other way around?\nThis piece of code will check the tweets from the last couple of days\n')

#We start getting the date of yesterday. We will use it to extract the tweets
yesterday = date.today() - timedelta(days=1)
date_yesterday = yesterday.strftime("%Y-%m-%d")

#log into Twitter
OAUTH_TOKEN = '26865311-XIJKtCW0ZKZOg5wspiwEjZs6Z8JTVscPSh6vmCLHX'
OAUTH_SECRET = 'LinK9UBVbOteW6wJaa1NPLG262rzNzUCtRFR6J9w'
CONSUMER_KEY = 'qmCNF3XdcPwcDlNmQmaew'
CONSUMER_SECRET = 'tbbnqcljdqh8uVJ87gFdmdsgbnDJhRw6aUoEDo0mbE'

t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

def parse_created(timestamp):
    _, m, d, t, _, y = timestamp.split(' ')
    return datetime.strptime('%s %s %s %s' % (m, d, t, y), '%b %d %H:%M:%S %Y').strftime('%s')

#I consider the centre of Copenhagen as a 4km radius circle centered at Norreport Station
result_Cph = t.search.tweets(q="kaffe",geocode="55.683333,12.571667,4km",count=100,since=date_yesterday) 
    #with open('data_Cph.txt', 'w') as outfile:
#json.dump(result_Cph, outfile)
tweets_Cph = result_Cph['statuses']
tweets_data_Cph = [(x['user']['name'], x['text'], parse_created(x['created_at']))
               for x in tweets_Cph]

time_Cph = [time for (user, text, time) in tweets_data_Cph]
n_tweets_Cph = len(time_Cph)
print ('Number of tweets from Copenhagen= %s\n' % n_tweets_Cph)

#Similarly, the centre of Stockholm is a 4km radius circle centered in Gamla stan
result_Sto = t.search.tweets(q="kaffe",geocode="59.325,18.070833,4km",count=100,since=date_yesterday)
    #with open('data_Sto.txt', 'w') as outfile:
#json.dump(result_Sto, outfile)
tweets_Sto = result_Sto['statuses']
tweets_data_Sto = [(x['user']['name'], x['text'], parse_created(x['created_at']))
               for x in tweets_Sto]

time_Sto = [time for (user, text, time) in tweets_data_Sto]
n_tweets_Sto = len(time_Sto)
print ('Number of tweets from Stockholm= %s\n' % n_tweets_Sto)

if n_tweets_Sto > n_tweets_Cph:
    print("People tweet more about coffee in central Stockholm")
else:
    print("People tweet more about coffee in central Copenhagen")
    time_Sto = time_Cph
    n_tweets_Sto = n_tweets_Cph

# Now I plot the tweet distribution for the most coffeinated city

y = range(0, n_tweets_Sto, 1)
time_Sto_2 = time_Sto[::-1]
x = [row.split(' ')[0] for row in time_Sto_2]
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(x,y, c='r', label='the data')
plt.grid()
if n_tweets_Sto > n_tweets_Cph:
    fig.suptitle('Tweets about coffe in Stockholm')
else:
    fig.suptitle('Tweets about coffe in Copenhagen')
plt.xlabel('Time')
plt.ylabel('Cumulative number of tweets')
plt.show()

#To dos:
# - set up a real-time search, so to save the tweets as they stream 
#   (http://people.fas.harvard.edu/~astorer/twitter/twitter.html#sec-4-3-1)
# - change time to a readable format
# - plot the histogram of the binned values instead of the cumulative tweet number