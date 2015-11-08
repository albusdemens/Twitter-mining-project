
"""
__author__ = "Ioannis Petridis"

"""

import twitter
import json
import io
#importing the twitter module and initiating connection
#with twitter using the OAUTH tokens

def oauth_login(): 
    CONSUMER_KEY = 'jHQIw8r6kfBVUOFsUETmJw'
    CONSUMER_SECRET = 'Zm4uDbCWxxSyYlFoFPskSFQbRBDOdx0bVGbrxCKjw4'
    OAUTH_TOKEN = '1876717710-AqchRzIOfuqUIUdjWUTBo7gwGbdzzAbxjXFWwuz'
    OAUTH_TOKEN_SECRET = 'jWyPk2qowcdFNOgdnzg5aeiTaPWogpk9NES8IFhI'
    
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api
    
#search for recent tweets on twitter. 

def twitter_search(twitter_api, q, max_results = 100):
    results = twitter_api.search.tweets(q=q, result_type='recent', max_results = max_results)
    statuses = results['statuses']
    for _ in range(1):
        print "Length of statuses", len(statuses)
        try:
            next_results = results['search_metadata']['next_results']
        except KeyError:
            break
        
        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']
        if len(statuses) > max_results: 
            break
            
    return statuses

#saving and restoring data to a.json file in D:/

def save_json(filename, data):
    with io.open('D:/tweets.json'.format(filename), 
                 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(data, ensure_ascii=False)))
        
def load_json(filename):
    with io.open('D:/tweets.json'.format(filename), 
                 encoding='utf-8') as f:
        return f.read()

q = "football"
twitter_api = oauth_login()      
results = twitter_search(twitter_api, q, max_results = 10)
save_json(q, results)
results = load_json(q)
   
#extracting the text from tweets
        
statuses = json.loads(open('D:/tweets.json').read())   
status_texts = [ status['text'] for status in statuses ]
print json.dumps(status_texts[0:10], indent=1) # explore the first 10 items from each tweet





