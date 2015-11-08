#!/usr/bin/env python
#title           :ytvidfeed.py
#description     :Creates a file that contains the comments of a youtube video.
#author          :toxokrotalos
#date            :20130930
#version         :0.1
#usage           :python ytvidfeed.py
#notes           :For the moment this script gets the first 25 comments. 
#python_version  :2.7.3 (32-bit)  
#==============================================================================

# Import the modules needed to run the script.
import gdata.youtube
import gdata.youtube.service
import os
import urlparse
import urllib2

#This function extracts video ID from YouTube's url supporting the 4 different 
#formats shown below:
# http://youtu.be/ecED5Q9gnrU
# http://www.youtube.com/watch?v=ecED5Q9gnrU
# http://www.youtube.com/embed/ecED5Q9gnrU
# http://www.youtube.com/v/ecED5Q9gnrU?version=3&amp;hl=en_US
def extract_video_id(url):
 
    url_data = urlparse.urlparse(url)
	
    if url_data.hostname == 'youtu.be':	
        return url_data.path[1:]
    if url_data.hostname in ('www.youtube.com', 'youtube.com'):	
        if url_data.path == '/watch':	
            query = urlparse.parse_qs(url_data.query)
            return query['v'][0]
        if url_data.path[:7] == '/embed/':	
            return url_data.path.split('/')[2]
        if url_data.path[:3] == '/v/':	
            return url_data.path.split('/')[2]
			
    return None

#This function checks if a url is valid
def check_url(url):
    try:
        urllib2.urlopen(url)
        return True         
    except ValueError, e:
        return False 
    except urllib2.HTTPError, e:
        return False	
    except urllib2.URLError, e:
        return False
		
	
#The user enters a YouTube url as input from the keyboard. The ulr given has to
#be in the string format inside quotes: 
#e.g. 'http://www.youtube.com/watch?v=IVjZMIWhz3Y'
while True:
    url = input('Enter a YouTube url in quotes \'\': ')
    video_id = extract_video_id(url)

    #Check if url exists by sending API GET request.
    url_feed = 'http://gdata.youtube.com/feeds/api/videos/'+video_id
    exists = check_url(url_feed)
    if exists == True:
	    break
    print 'Inavalid url!Try again.'	
		
yt_service = gdata.youtube.service.YouTubeService()

#Retrieving comments and title for a video using the YouTubeService object.
comment_feed = yt_service.GetYouTubeVideoCommentFeed(video_id=video_id)
entry = yt_service.GetYouTubeVideoEntry(video_id=video_id)
title = entry.media.title.text

# Create a file that the video comments can be written to.
f = open(title+".txt", "w")

#Iterate through the first 25 comments.
for comment in comment_feed.entry:
    # Write each comment to the file. 
    f.write(comment.content.text.replace('\xef\xbb\xbf', '')+'\n')

# Close the file after writing to it.	
f.close()

print "The file "+title+".txt has been created."