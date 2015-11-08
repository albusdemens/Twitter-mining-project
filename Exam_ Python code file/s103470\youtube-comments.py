"""
This program retrieves comments from a YouTube video,
and saves them in a file along with the title and author.
"""

import gdata.youtube.service, urllib2
yts = gdata.youtube.service.YouTubeService() 

"""
Promts the user for the web address (url) of the video.
"""
original_url = raw_input('Please enter the video address:\n>')

"""
Promts the user for the start index of the comments, e.g. if the user wants to skip comments.
"""
comment_start = raw_input('What comment index should we start from? (1 = from the latest)\n>')

"""
Promts the user for the wanted amount of comments to be retrieved.
"""
max_results = raw_input('How many comments do you want to retrieve? (Max 50)\n>')

"""
To test the program without user input.
"""
#original_url = 'http://www.youtube.com/watch?v=x0rk5zh7RaE'
#comment_start = '1'
#max_results = '6'

"""
The address where the comments can be retrieved.
"""
gdata_yt = 'http://gdata.youtube.com/feeds/api/videos/'

"""
The "ID" of the video.
"""
video_id = original_url.replace('http://www.youtube.com/watch?v=', '')

"""
Concatenates the input to get access to the comments of the requested video with the given parameters.
"""
url = '%s%s/comments?start-index=%s&max-results=%s' % (gdata_yt, video_id, comment_start, max_results)

"""
The list which will hold the comments.
"""
comments = []

"""
Retrieves the comments of the video and fill them into the list.
"""
ytfeed = yts.GetYouTubeVideoCommentFeed(uri=url) 
comments.extend([ comment.content.text for comment in ytfeed.entry ]) 

"""
The title and author of the video.
"""
video = yts.GetYouTubeVideoEntry(video_id=video_id)
title = video.title.text
author = video.author[0].name.text

"""
Saves all the comments in a file, divided by a line of the character '-'.
"""
f = open('%s_%s-comments.txt' % (title, video_id), 'w')
f.write('%s\nby %s\n\n' % (title, author))
for comment in comments:
    f.write(comment + '\n' + '-' * 40 + '\n')
f.close()

"""
To print it to the console.
"""
#for comment in comments:
    #print comment + '\n' + '-' * 40 + '\n'