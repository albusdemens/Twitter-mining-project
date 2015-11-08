from datetime import datetime
from gdata.youtube import service

#Defining the youTubeService which is used to get content from YouTube
youTubeService = service.YouTubeService()

#Login in with api key and id
youTubeService.developer_key = 'AIzaSyAoJF77FUfDEsVJqAm8WzZXI7PZoZTe-eI'
youTubeService.client_id = '333122242833.apps.googleusercontent.com'

#Video id for the celected YouTube video
video_id = 'lYcIvvKJWek'

#Count comments
count = 0

#Tracking the time for every file(per/day)
q = datetime.now().strftime('%Y-%m-%d')+".txt"
f = open(q, 'a')

#Getting the content of the video
content = youTubeService.GetYouTubeVideoEntry(video_id=video_id)
f.write("Video title: "+content.media.title.text)
f.write("\nVideo description: "+content.media.description.text)
f.write("\nVideo views: "+content.statistics.view_count+"\n\n\n")
f.write("Comments: \n\n")


#By using a generator, we can get all the comments from a given video
def comments(youTubeService, video_id):
    
    #Get the comments form the video
    comment_feed = youTubeService.GetYouTubeVideoCommentFeed(video_id=video_id)
    
    #To get all the comments a while loop is used to go through all the links
    #While comment is not null, we should continue to get the comments
    while comment_feed is not None:
        for comment in comment_feed.entry:
             yield comment
        #When all the comments in one link has been yielded we continue to the next link
        nextLink = comment_feed.GetNextLink()
        #If no more links are available the while loops stops
        if nextLink is None:
             comment_feed = None
        #Else the comment feed continue
        else:
             comment_feed = youTubeService.GetYouTubeVideoCommentFeed(nextLink.href)

#Loop through all the comments generated in the comments(youTubeService, video_id)
for comment in comments(youTubeService, video_id):
    f.write(comment.author[0].name.text+": ")
    f.write(comment.content.text+"\n\n")
    count = count+1
f.write("Video comments: "+str(count))
f.close()
print "Done loading..."