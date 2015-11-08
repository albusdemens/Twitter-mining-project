import tweepy
import pylab as pl
import numpy as np

#oAuth authentication
consumer_key="08DJOIwxTrCmdtVhr8wUrw"
consumer_secret="akfRbXuKX5n7V8Tqrs8iuS2e3tCWeNoJlaXaM8rkA0"
access_token="5962522-RnYYkdZKtHGpikSDDkK8O0rvbXo1js7t6vzIyRyHA"
access_token_secret="sr9FZxP6UECauKrsDn93abGTeVKLWhVdhNBDmFmld0Y"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)       
api = tweepy.API(auth)

pl.clf()
#insert a twitter screen_name, look for the latest 100 tweets, the first 20 followers, and
# other informations related to his account
print 'You can run this script 15 times every 15 minutes (otherwise you would exceed the rate limit of tweepy)'
try:
    name = raw_input("insert a twitter screen_name (e.g. nytimes): ")
    user = api.get_user(name)
    result = api.user_timeline(name, exclude_replies = 'true', count = 100)
    fol = api.followers(name)    

    print('Name: ' + user.name)
    print('Location: ' + user.location)
    print('Friends: ' + str(user.friends_count))
    print 'checking ' + user.name + ' tweets'
    hashtag = {}
#Looking for the hastags in the latest 100 tweets
    for v in result:  
        for word in v.text.split():
            if '#' in word:
                if hashtag.has_key(word):
                    hashtag[word] = hashtag[word] +1
                else:
                    hashtag[word] = 1

#Looking for the hastags in the latest 100 tweets of the followers of 
# 'name' (only 14 in order to not exceed the rate limit)

    for c in fol:
        try:
            name = c.screen_name
            user = api.get_user(name)
            result = api.user_timeline(name, exclude_replies = 'true', count = 100)
            print 'checking ' + name + ' tweets'
            for v in result:  
                for word in v.text.split():
                    if '#' in word:
                        if hashtag.has_key(word):
                            hashtag[word] = hashtag[word] +1
                        else:
                            hashtag[word] = 1
  # some account are protected and you can look their tweets
        except tweepy.error.TweepError as k:
            if k[0] == "Not authorized.":
                print 'Skipping ' + name + ' because you are not authorized'
            else:
                print k
                break
                    
    print sorted(hashtag.items(), key=lambda (k,v):(-v,k))
    #Print a histogram 
    X = np.arange(len(hashtag))
    pl.bar(X, hashtag.values(), align='center', width=0.5)
    pl.xticks(X, hashtag.keys())
    ymax = max(hashtag.values()) + 1
    pl.ylim(0, ymax)
    pl.show()

except tweepy.error.TweepError as t:
       print t

