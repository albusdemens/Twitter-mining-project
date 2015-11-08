"""
@author: Simon Benfeldt - s103182
Group: Mads Frøding Engels(s103201) & Simon Benfeldt Jørgensen
"""
###This is a twitter-bot that can follow, unfollow, tweet and retweet 
###Import twitter api, pretty-print and json
import twitter #the original twitter API found https://dev.twitter.com/docs/api/1.1
import pprint
import json
import time
import random

#################################
### Access a Twitter profile
### from dev.twitter.com
### Create an Application
### Remember to turn on read and write in the application in the 
#################################

###The below credentials has been removed. Put try out with your own Twitter account 

#Tested on the twitter bot created for the purpose @Amatthesen
CONSUMER_KEY = 'w0dtvFtn2L85s8SwVUHPxx'
CONSUMER_SECRET = 'HFstXQbuQZFLjECY7TrVe5uAxWt60K7Xk04ZrDYIxx'
OAUTH_TOKEN = '1909083666-LTaztsDcPShoLA7WTCes47NgHN0T4eJPjuXspxx'
OAUTH_TOKEN_SECRET = 'ZqaaTavwn8NepV4KMNbWltaLEt2hdcnhOnvnH9rxx'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

###The API is now defined:
api = twitter.Twitter(auth=auth)
###Post to your twitter profile:
api.statuses.update(status='Jeg elsker Danmark')

###Save all your friends & followers to lists by IDs
friends = api.friends.ids()['ids']
followers = api.followers.ids()['ids']

###Compare which followers who's also friends:
my_friends = set.intersection(set(followers),set(friends))
print 'So many friends do I have: ', len(my_friends)

###Lets find who's following me, who I am not following:
should_follow = set(followers) - set(my_friends)
print 'So many should I follow', len(should_follow)

###Lets follow who that I don't follow:
for follower in should_follow:
    api.friendships.create(user_id=follower)
    print 'Now following: ', follower
    time.sleep(1*random.randrange(1,2))
    
### Remove who I follow, but doesn't follow me back
doesnt_follow_me = set(friends) - set(followers)
print 
for hater in doesnt_follow_me:
    api.friendships.destroy(user_id=hater)
    print 'Now unfollowing: ', hater
    time.sleep(0.1*random.randrange(1,10))

### Lets get the first 200 tweets on my timeline:
timeline_tweets = api.statuses.home_timeline(count=200)

### Use json to sort the timeline tweets
json.dumps(timeline_tweets, indent=1)
pp = pprint.PrettyPrinter(indent=1)
tweet_ids = [status['id'] for status in timeline_tweets]
tweet_texts = [status['text'] for status in timeline_tweets]
retweet_counter = [status['retweet_count'] for status in timeline_tweets]

###Gets the most retweet tweet from the timeline and retweet it if not the word "follow" is in the tweet
m = max(retweet_counter)
RT_id_counter = [i for i, j in enumerate(retweet_counter) if j == m]
tweet_to_RT = tweet_texts[RT_id_counter[0]]
string_check = "follow"
if string_check in tweet_to_RT:
    print string_check," has been found in ", tweet_to_RT
else:
    print string_check, " has not found in ", tweet_to_RT
    api.statuses.retweet(id=tweet_ids[RT_id_counter[0]])
    
###In the future to implement with a skeleton for use with a twitter-bot running 24/7