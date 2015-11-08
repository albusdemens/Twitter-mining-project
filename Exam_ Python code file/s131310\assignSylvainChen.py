"""
This script will enable us to get the most active followers of one twitter account.
"""

# we will use the floating division for dividing integers by integers
from __future__ import division

# header
__version__ = 1.1
__author__ = "Sylvain Chen"


# we will use the twitter API from tweepy
import tweepy
# this will enable us to sort a dictionary
from operator import itemgetter
# we will also use datetime for a few operations (difference between two dates)
import datetime

"""
Page located at https://dev.twitter.com/apps (under "OAuth settings")
In order to use the Twitter API, we must be authenticated
Below is the authentication of my own account in the "read-only" mode
"""
consumer_key = "G11DVn342rVZj9kXv68CSA"
consumer_secret="FBrg5YphNrAGx9OragJOe7onCgoRmhNqKNqd4UXAqg"

# The access token is in the "read-only" mode so that everyone can use it without doing anything bad to my account
access_token="470913852-qMOz52wSrP91LZla1a1DFT4RHmOqbeNsUmWCnkNM"
access_token_secret="r4AF4mVCsKBcHr9Ahm0GbqUcgW2MQ0eDaNow0dA"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# you should see the name of the account print out provided that the authentication was successful
# here SylChen1
print "Active account : %s" % api.me().name

# Request the screen name and give an explanation of a "screen name"
print "Enter a Twitter screen name\n(i.e. the name after \"@\"), e.g. SylChen1 for @SylChen1"
name=raw_input()

# getting the requested user
user = api.get_user(name)

# 2 list of followers that we will get and we will sort them by number of tweets per day AND by number of followers per day
lFollowers = []
lFollowers2 = []
now = datetime.datetime.now()

"""
api.followers will return only 20 followers but we can also use the following raw
for member in tweepy.Cursor(api.followers, screen_name = name).items():
which can analyze hundreds of followers;
but due to the twitter API limitation, we cannot use this in an efficient way.
"""
for member in api.followers(screen_name = name):
    # d is the difference of time between now and the creation of the member
    d = now-member.created_at
    # avoid the case of a very recent account (a few hours)
    if d.days != 0:
        lFollowers.append((member.followers_count/d.days, member.screen_name))
        lFollowers2.append((member.statuses_count/d.days, member.screen_name))


# sorting with a descending order
lFollowers.sort(reverse = True)
lFollowers2.sort(reverse = True)

# display the intermediate results
print "\nFollowers per day"
for follower in lFollowers:
    print "%f - %s" % (follower[0], follower[1])

print "\nTweets per day"
for follower in lFollowers2:
    print "%f - %s" % (follower[0], follower[1])

# dFollowers is a dictionary
dFollowers = {}

# Add the rank of the lFollowers list member to the dictionary
i = 1
for member in lFollowers:
    dFollowers[member[1]] = i
    i = i + 1

# Add the rank of the lFollowers2 list member to the dictionary
i = 1
for member in lFollowers2:
    dFollowers[member[1]] = dFollowers[member[1]] + i
    i = i + 1

"""
inspired by http://goo.gl/ufEvt2 for sorting a dictionary by value
display the final results
"""
print "\nThe most active twitter followers of %s" % name
i = 1
for key, value in sorted(dFollowers.iteritems(), key=lambda (k,v): (v,k)):
    print "%d - %s" % (i, key)
    i = i + 1

#end of the script