# IMPORTANT: To use the class properly, you need to install praw, a python wrapper module of reddit api. 
# To install praw module, you can type `pip install praw` or `easy_install praw`. For more information on
# how to install, please refer to `https://praw.readthedocs.org/en/latest/#installation`

__author__ = 'Oguz Demir'

import praw
import re
import nltk
from collections import Counter

class RedditCrawler:
	""" A reddit.com crawler class """

	# Initializes crawler instance
	def __init__(self):
		self.crawler = praw.Reddit(user_agent = 'Data Mining using Python')

	# Get comments of a subreddit, returns a list of strings 
	def get_subreddit_comments(self, subreddit, limit=None):
		comments = self.crawler.get_subreddit(subreddit).get_comments(limit=limit)
		try:
			return map(lambda comment: comment.body.encode('utf-8'), comments)
		except Exception:
			return []

	# Get submissions of a subreddit, returns a list of strings (submission texts)
	def get_subreddit_submissions(self, subreddit, limit=None):
		submissions = self.crawler.get_subreddit(subreddit).get_hot(limit=limit)
		try:
			return map(lambda submission: submission.title.encode('utf-8'), submissions)
		except Exception:
			return []

	def __eq__(self, other):
		return (isinstance(other, RedditCrawler) and
			self.crawler == other.crawler)

	def __str__(self):
		return str(self.crawler).encode('utf-8')		

# Let's take a look at what people are talking about Python on Reddit
if __name__ == '__main__':
	crawler = RedditCrawler()
	comments = crawler.get_subreddit_comments('Python', 200)

	words = [word for comment in comments 
				  for sentence in nltk.sent_tokenize(comment) 
			      for word in re.split('\W+', sentence)]
	adjectives_dict = Counter([word for word, tag in nltk.pos_tag(words) if tag == 'JJ'])
	print adjectives_dict.most_common(20)

	
			


