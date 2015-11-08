"""
twitterCaller class
"""

__version__ = 1.00
__author__ = "Emil Bunk"
__all__ = ["twitterCaller"]

import twitter, time # The twitter module can be downloaded with $ pip install twitter

class twitterCaller:
	"""
	This class facilitates the use of API-calls in the Twitter REST-API to avoid error 429 (Too many requests).
	The REST-API is documented here: https://dev.twitter.com/docs/api/1.1
	"""
	def __init__ (self, oauthToken, oauthTokenSecret, consumerKey, consumerSecret):
		"""
		Initiate an authenticated connection with Twitter.com, using the twitter module.
		"""
		self.api = twitter.Twitter(auth=twitter.oauth.OAuth(oauthToken, oauthTokenSecret, consumerKey, consumerSecret))
		self.ratelimits = self.api.application.rate_limit_status()
		self.forced = False
	
	def setForced():
		"""
		Change the forced setting, establishing wether to wait for a new request-window or not.
		"""
		self.forced = not self.forced
		
	def limitCheck(self, method, forced = None):
		"""
		Checks if there are any remaining calls for the method in question.
		If forced, the script will sleep till a new window opens.
		"""
		if forced is None:
			forced = self.forced

		resource = method[1:].split('/')[0]
		if self.ratelimits['resources'][resource][method]['remaining'] > 0:
			self.ratelimits['resources'][resource][method]['remaining'] -= 1
			return True
			
		if forced:
			timeout = self.ratelimits['resources'][resource][method]['reset']-time.time()
			
			if timeout > 0:
				time.sleep(timeout+5)
				
			self.ratelimits = self.api.application.rate_limit_status()
			self.ratelimits['resources'][resource][method]['remaining'] -= 1
			return True
		
		self.limitCheck('/application/rate_limit_status', True)
		
		if self.ratelimits['resources'][resource][method]['remaining'] > 0:
			self.ratelimits['resources'][resource][method]['remaining'] -= 1
			return True
		return False
		
	def getTweetsFromSearch(self, query, maxcount = 100):
		"""
		Utilisation of the class for retrieving tweets from a search query.
		"""
		method = '/search/tweets'
		
		if self.limitCheck(method):
			return self.api.search.tweets(q = query, count = maxcount)
		return []
		
	def getTimeline(self):
		"""
		Utilisation of the class for retrieving tweets from authenticated users timeline.
		"""
		method = '/statuses/user_timeline'
		
		if self.limitCheck(method):
			return self.api.statuses.user_timeline()
		return []