# -*- coding: utf-8 -*-

import gdata.youtube.service 
import nltk 
import numpy

# Set up the YouTube API
youtube = gdata.youtube.service.YouTubeService() 

def get_youtube_comments(video_id):
	"""Creates a list with the latest 1000 
	comments from the given video. """

	urlpattern = 'http://gdata.youtube.com/feeds/api/videos/%s/comments?start-index=%d&max-results=25' 
	index = 1 
	url = urlpattern % (video_id, index)
	comments = []

	# Create a list with the 1000 latest comments.
	# There is a limit to only get 1000 comments. 
	for n in range(39): 
	  ytfeed = youtube.GetYouTubeVideoCommentFeed(uri=url) 
	  for comment in ytfeed.entry:
	  	comments.append(comment.content.text.decode('utf-8-sig'))
	  url = ytfeed.GetNextLink().href 
	  print url 

	return comments

def create_nltk_text(my_list):
	"""Creates a list with the words in
	the given list"""

	# Create a string from the given list
	text = ''.join(my_list)
	# Use the NLTK to split the words into 
	# a list of words in the order of appearance.
	return nltk.word_tokenize(text)

yt_video = 'My2FRPA3Gf8' # Video id

video_entry = youtube.GetYouTubeVideoEntry(video_id = yt_video)
# Print the video rating
print 'Rating: ' + str(video_entry.rating.average)

video_comments = get_youtube_comments(yt_video)

# Save the comments to a text file
comment_file = open('comments.txt', 'w')

for comment in video_comments:
	comment_file.write(comment.encode('utf-8') + '\n')

comment_file.close()


video_text = create_nltk_text(video_comments)

# Use the NLTK to make a frequency distribution
# of the comments.
fdist = nltk.FreqDist(video_text)
# Order the most common words in the comments
voca = fdist.keys()
# Top 25 used words
print 'Top 25 words:'
print voca[:25]
# Plot the 25 most common words by frequency
fdist.plot(25)


