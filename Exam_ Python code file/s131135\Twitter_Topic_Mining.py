# This program try to answer what people are talking about right now by the following two steps
# First, grab the most popular topics in Twitter
# Second, mine the tweets of a specific topic to have a deeper looking inside the trending issues
# It will not work unless you fill in belowing empty string values that are defined as placeholders.
# Go to http://dev.twitter.com/apps/new to create an app and get values for these credentials that you'll need to provide
# It takes you less than ten minutes to create the necessary app and get accesss to mining an exiting world
import twitter,json,nltk
from collections import Counter
import matplotlib.pyplot as plt

# Obtain the access to data in Twitter
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
my_api = twitter.Twitter(auth=auth)

# Gain the 10 most popular topics around the world and in your chosen place, in this case UK. Try to find common ones
# According to The Yahoo! Where On Earth, the entire world's ID is 1, while different places's IDs vary
# See more information at http://developer.yahoo.com/geo/geoplanet/guide/concepts.html
WORLD_ID = 1
PLACE_ID = 23424975 #UK  e.g. 23424977 #US    
# Denmark 23424796, doesn't work in this case. return to details: {"errors":[{"message":"Sorry, that page does not exist","code":34}]} 
world_trends = my_api.trends.place(_id=WORLD_ID)
place_trends = my_api.trends.place(_id=PLACE_ID)
print json.dumps(world_trends, indent=1)
print 
print json.dumps(place_trends, indent=1)
# See if there exist common trends between two data sets
world_trends_set = set([trend['name'] for trend in world_trends[0]['trends']])
place_trends_set = set([trend['name'] for trend in place_trends[0]['trends']]) 
common_trends = place_trends_set.intersection(world_trends_set)
print common_trends

# Set this variable q to a trending topic. It is strongly recommanded picking one from the result of codes above  
# The query below, 'Joe Hart' was a trending topic when I was running the program
# Grab tweets on topic q, answer "what are people talking about the topic right now?" by analysing content of tweets
topic = 'Joe Hart' 
num = 100
mining_results = my_api.search.tweets(q=topic, count=num)
statuses = mining_results['statuses']
status_texts = [ status['text']
                 for status in statuses ]
words = [ w 
          for t in status_texts 
              for w in t.split() ]
w_length=len(words)
unique_w_length=len(set(words))
print "words length is", w_length
print "unique words length is" ,unique_w_length
print "lexical diversity is" ,1.0*unique_w_length/w_length
print

freq_dist=nltk.FreqDist(words)
print freq_dist.keys()[:20]
print
print freq_dist.keys()[-20:]

word_counts = sorted(Counter(words).values(), reverse=True)
plt.loglog(word_counts)
plt.ylabel("Frequency")
plt.xlabel("Word Rank")