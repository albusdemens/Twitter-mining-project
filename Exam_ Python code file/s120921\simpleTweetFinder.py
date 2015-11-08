# In order to run this script the user should create his own Twitter
# application to obtain his own consumer_key, consumer_secret, access_token_key,
# access_token_secret. You can do it here: https://dev.twitter.com/apps/new
# You also need to install the Twitter wrapper: https://code.google.com/p/python-twitter/
import twitter
import os, string
import nltk 
from collections import defaultdict

api = twitter.Api()
api = twitter.Api(  consumer_key='',
                    consumer_secret = '', 
                    access_token_key = '', 
                    access_token_secret = '')

# Loads the stopwords from nltk. You need to download it (see Installation
# instructions of Lecture 1)
stopwords = nltk.corpus.stopwords.words('english')
userTweetsFile = open('user-tweets.txt','w')
tweetsFile = open('tweets.txt','w')

inputTerm = input('Insert a term surrounded with \'\' (eg: \'libya\'): ')

# Download random tweets (default number) related to the term that the user gave                    
initialTweets = api.GetSearch(term = inputTerm, lang = 'en')

# Write the tweets in a file
for tweet in initialTweets:
    tweetsFile.write(tweet.text.encode('UTF-8'))

tweetsFile.close()

# From the tweets in the file, we find the most frequent words
raw = open('tweets.txt').read()
words = nltk.word_tokenize(raw)  # Split the text into words
filtered_words = [w for w in words if w.lower() not in stopwords]  #Remove stopwords

# Remove punctuation
exclude = set(string.punctuation)
filtered_words = [ch for ch in filtered_words if ch not in exclude]

#Print the most used words
fdist = nltk.FreqDist(filtered_words)
vocabulary = fdist.keys()
print ('The 25 most frequently used words are:')
print vocabulary[:25]

# The following part of the code will be used later on the project. So
# far it finds the authors of the tweets related to the term(that the user
# inserts). For each user, it downloads 5 tweets and stores them in a txt
# file in this form: user -> list of tweets.

users = list() 
d = defaultdict(list)

users = [tweet.user.id for tweet in initialTweets]

for user in users:
    relativeTweets = api.GetUserTimeline(user_id = user, count = 5)
    d[user].append([t.text.encode('UTF-8') for t in relativeTweets])

for k,v in d.iteritems():
    userTweetsFile.write( "%s -> %s \n" % (str(k), str(v)))

userTweetsFile.close()
