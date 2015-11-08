# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:29:21 2013

@author: 
@student no: 
    
    This script is to get the retweet relationship from Twitter about a 
    designated topic which you can define it yourself in the command.
    
    https://code.google.com/p/xxxxxxxxxx/
"""

import os
import twitter
import networkx as nx

from twitter.oauth import write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance

# Some important infomation about your application of Twitter
APP_NAME = 'Your app name'
CONSUMER_KEY = 'Your consumer key'
CONSUMER_SECRET = 'Your consumer secret'

# Get access to Twitter with your application applied on https://dev.twitter.com/
# It save the token and token secret locally to avoid verify every time using the 
# app.
def authenticate(app_name='',
                consumer_key='',
                consumer_secret='',
                token_file='auth/twitter.oauth'):
    try:
        (access_token, access_token_secret)=read_token_file(token_file)
    except IOError:
        (access_token, access_token_secret) = oauth_dance(app_name, consumer_key, 
            consumer_secret)
        
        if not os.path.isdir('auth'):
            os.mkdir('auth')
        
        write_token_file(token_file,access_token,access_token_secret)
        
        print "OAuth Success. Token file stored to ", token_file
    # Connect to Twitter
    return twitter.Twitter(domain='api.twitter.com', api_version='1.1',
                           auth=twitter.oauth.OAuth(access_token, access_token_secret,
                                                    consumer_key, consumer_secret))
# Get the origins of retweets
def retweet_origin(tweet):
    rt_origins = []
    if tweet.has_key("retweeted_status"):
        rt_origins += [tweet['retweeted_status']['user']['screen_name'].lower()]
    
    return list(set([rto.strip("@").lower() for rto in rt_origins]))

# Create the relationship using networkX, in which the nodes stands for users, 
# edges for retweet relationship.
def make_graph(tweets):
    g=nx.DiGraph()
    
    for tweet in tweets:
        rt_origins = retweet_origin(tweet)
        if not rt_origins:
            continue
        for rt_origin in rt_origins:
            g.add_edge(rt_origin, tweet['user']['screen_name'],{'tweet_id': tweet['id']})
    return g

    
if __name__ == '__main__':
    # Connect to Twitter, and get the authenticated API
    t=authenticate(APP_NAME, CONSUMER_KEY, CONSUMER_SECRET)
    # Keyword
    # TODO: Make it in the command
    Q='Justin'
    # How many results
    # TODO: Make it in the command
    COUNT = 200
    search_results = []  
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    search_results = t.search.tweets(q=Q, count=COUNT)
    all_tweets = search_results['statuses']#searchmetadata, statuses
    # TODO: Check out what searchmetadata is for and work on it
    
    # Use the searched tweet to get the relationship of retweets.
    g=make_graph(all_tweets)
    # TODO: Try to visulize it 
    
    print "Number nodes:", g.number_of_nodes()
    print "Num edges:", g.number_of_edges()
    print "Num connected components:", len(nx.connected_components(g.to_undirected()))
    print "Node degrees:", sorted(nx.degree(g))
    