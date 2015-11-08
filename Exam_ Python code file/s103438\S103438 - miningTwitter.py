"""
This class in getting data from twitter. The tweets are for now regarding the game League of Legends, but might be changed.
Please make sure you have all the librarys installes. For this use pip or easy_install.
"""
#Using tornado web server
import tornado.ioloop 
import tornado.web
# Twython api used for twitter mining
from twython import Twython 
import socket
 
APP_KEY = "zwQTPl9VuocSGYeB0320Q"
APP_SECRET = "y1lYaHdwR9LtBivfAeTvgzGofjBXp7PQjoy3puqKRE"
serverPort = 8888 #the port the webapplication use

class Tweet(object):
    """Class containing the objects for the tweets"""
    def __init__(self, userName, screenName, tweet):
        self.userName = userName
        self.screenName = screenName
        self.tweet = tweet

def twittersearch(query):
	"""twittersearch using twython api to create a twitter search"""
	twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2) #creating the twython using oauth version 2
	ACCESS_TOKEN = twitter.obtain_access_token() #getting an acces token from twitter
	twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN) #using the access token
	return twitter.search(q=query, result_type='recent', count='10') #searching twitter for the query input

def savingTheTwitterSearch(twittersearch):
    """savingTheTwitterSearch is creating an array of tweet objects"""
    #Should be changed to some kind of database instead of an array
    statuses = twittersearch[u'statuses']
    tweets = []
    for result in statuses:
        user = result[u'user']
        #defining the username,screenName and tweettext variable before creating the object
        userName = str(user[u'name'].encode('ascii', 'ignore'))
        screenName = str(user[u'screen_name'].encode('ascii', 'ignore'))
        tweetText = result[u'text'].encode('ascii', 'ignore')
        #creating the tweet object and append it to the tweets array
        tweet = Tweet(userName, screenName, tweetText) 
        tweets.append(tweet)
    return tweets

class MainHandler(tornado.web.RequestHandler):
	"""Function creating the front page for the web application"""
	def get(self):
            self.write("Twitter Mining in Python" + "<br/>") #Writing helloWorld to the webpage
            results = twittersearch('#LeagueOfLegends') #getting tweets regarding the game league of legends
            tweets = savingTheTwitterSearch(results)
            #writing the tweets on the homepage
            for tweet in tweets:
                self.write("User Name: "+ tweet.userName + "<br/>")
                self.write("Screen Name: "+ tweet.screenName + "<br/>")
                self.write("Tweet: " + tweet.tweet + "<br/>")  
    	
#Creating web application variable using the MainHandler
application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    try:
        application.listen(serverPort) #creating the application on port 8888.
        tornado.ioloop.IOLoop.instance().start() #starting the main event loop in the web application
    except socket.error: #giving an error if the port is already in use.
        print "Socket Error. The defined port might already be in use, try another port."
        print "If the python application is already running the port is in use, try stopping the python application."
