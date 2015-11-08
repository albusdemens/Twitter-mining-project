# -*- coding: utf-8 -*-
"""
@author: Mads F. Engels - s103201
Group member: Simon B. Jørgensen - s103182
"""

###Import twitter api, pretty-print and json
import twitter
import pprint
import json
import time
import rand

#################################
### Access your Twitter profile
### from dev.twitter.com
### Create an Application
#################################

###The below tokens has been removed, 
###since the tokens gives you direct
###access to your twitter account
CONSUMER_KEY = 'consumer_key'
CONSUMER_SECRET = 'consumer_secret'
OAUTH_TOKEN = 'oauth_token'
OAUTH_TOKEN_SECRET = 'oauth_token_secret'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

###The API is now defined:
api = twitter.Twitter(auth=auth)

###Post to your twitter profile:
#api.statuses.update(status='I love using the twitter api!')

###Save all your friends & followers to lists by IDs
friends = api.friends.ids()['ids']

followers = api.followers.ids()['ids']

###Compare which followers who's also your friends:
my_friends = set.intersection(set(followers),set(friends))
len(my_friends)

##Lets find who's following me, who I am not following:

should_follow = set(followers) - set(my_friends)
len(should_follow)

###Lets follow 10 that I don't follow:

for follower in should_follow[:10]:
    api.friendships.create(follower)
    ###set a timer, and add a user every minut
    time.sleep(60 + random.randrange(1,10))

###Now lets remove 10 who I follow, but doesn't follow me back
doesnt_follow_me = set(friends) - set(followers)

for hater in doesnt_follow_me[:10]:
    api.friendships.destroy(hater)
    time.sleep(60 + random.randrange(1,10))

### Lets get the first 20 tweets on my timeline:
tweets = api.statuses.home_timeline(count=20)

### Use json to sort the tweets
json.dumps(tweets, indent=1)
tweet_texts = [ status['text'] for status in tweets]
tweet_ids = [status['ids'] for status in tweets]

###Lets retweet a random tweet from our list
api.statuses.retweet(id=tweet_ids[random.randrange(1,20)])



