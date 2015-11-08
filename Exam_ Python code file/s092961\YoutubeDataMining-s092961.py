
########
#Description: This code shows how to mine a youtube video for comments
#Student: Shafi Nazar s092961
#Course: Data mining with python 02819
########

#gdata module is needed for accessing youtube
#gdata module depend on following modules: ElementTree, httplib and urllib.
import gdata.youtube
import gdata.youtube.service

#In order to access and perform operations with the YouTube Data API, 
#a gdata.youtube.service.YouTubeService object has to be initialized.
yt_service = gdata.youtube.service.YouTubeService()

#Turn on HTTPS/SSL access.
yt_service.ssl = True

#Get the comment feed of a video given a video_id
#Parameter: a youtube video ID 
#Returns: a list of comment entries
def SaveCommentFeed(video_id):
    
    #Comments are saved in this list
    comments=[]
    
    #Video comment feed URL
    comment_feed_url = "http://gdata.youtube.com/feeds/api/videos/%s/comments"
    url = comment_feed_url % video_id
    
    #Fetching the comment feed of a particular youtube video given an URL
    comment_feed = yt_service.GetYouTubeVideoCommentFeed(uri=url)
    
    try:
        while comment_feed:
            #Appending all comment entries to the list
            for comment_entry in comment_feed.entry:
                comments.append(comment_entry)
            
            #Get next page of comments
            comment_feed = yt_service.Query(comment_feed.GetNextLink().href)
        
    except:
            pass
        
    #Return list of saved comment entries
    return comments


### Using the function WriteCommentFeed
#Example video: www.youtube.com/watch?v=MjZJkgXTIRU 
video_id = 'MjZJkgXTIRU' 

video_comments = SaveCommentFeed(video_id)

#Amount of comments fetched from feed: max limit = 1000 comments/video
print "Fetched comments in total: %d" %len(video_comments)

#Print Author name, published data and comment nicely spaced for 50 comment entries
sample_comments = video_comments[0:50]
for comment in sample_comments:
    print [comment.author[0].name.text, comment.published.text]
    print comment.content.text
    print

