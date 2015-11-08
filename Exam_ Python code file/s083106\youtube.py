#!/usr/bin/env python

# Important: To use this class properly, you will need the Youtube API version 2, namely gdata.youtube
# It can either be installed with PIP, or downloaded from the google code website.
# Further instructions can be found on the google developer site: https://developers.google.com/gdata/articles/python_client_lib 

import gdata.youtube.service

class YoutubeComment(object):

	# Initialize class with movie name and youtube ID. Define two additional internal variables for storing data
	def __init__(self, name, yid):
		self.name = name
		self.yid = yid
		self.ctext = []
		self.cdate = []

	# Return YouTube video name
	def getname(self):
		return self.name

	# Return YouTube video ID
	def getyid(self):
		return self.yid

	#  Fetch 'num' comments. Note that this is the least amount of comments aquired, given that enough comments exists. 
	def getcomments(self, num=50): # Might actually return up to 49 more comments!
		self.yts = gdata.youtube.service.YouTubeService()
		url = "http://gdata.youtube.com/feeds/api/videos/%s/comments?start-index=%d&max-results=50" % (self.yid, 1)
		while (len(self.ctext) < num):
			self.ytfeed = self.yts.GetYouTubeVideoCommentFeed(uri=url)
			self.ctext.extend([comment.content.text for comment in self.ytfeed.entry])
			self.cdate.extend([comment.published.text for comment in self.ytfeed.entry])
			if not self.ytfeed.GetNextLink(): break
			url = self.ytfeed.GetNextLink().href
		return self.ctext


# Lets check out some of 2010's great movie trailers!
inception = YoutubeComment(name="Inception", yid="8hP9D6kZseM").getcomments(10000)
the_social_network = YoutubeComment(name="The Social Network", yid="lB95KLmpLR4").getcomments(10000)

print "5 most recent comments for Inception:\n"
for comment in inception[0:5]: 
	print comment 

print "5 first comments for The Social Network:\n"
for comment in the_social_network[-6:-1]: 
	print comment + "\n\n"

print "Total comments: \n   The Social Network: %d\n   Inception: %d" % (len(the_social_network), len(inception))
# (Be patient, we cannot load more than 50 comments at a time per movie :-)