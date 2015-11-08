'''
Created on 30/09/2013

@author: Kasper

Sentiment analysis on a given youtube video
Test code at the bottom
'''
def GetComments(video_id):
    '''
    Created on 30/09/2013
    
    @author: Kasper
    
    Function to retrieve the comments of a given youtube video 
    and return a data entity with only the comments
    '''
    import gdata.youtube.service
    
    #Setting up the youtube service
    yt_service = gdata.youtube.service.YouTubeService()
    yt_service.ssl = True
        
    #Get all the comments, not just the first 25
    def comments_generator(client, video_id):  
        comment_feed = client.GetYouTubeVideoCommentFeed(video_id=video_id)  
        while comment_feed is not None:  
            for comment in comment_feed.entry:  
                yield comment  
            next_link = comment_feed.GetNextLink()  
            if next_link is None:  
                comment_feed = None  
            else:  
                comment_feed = client.GetYouTubeVideoCommentFeed(next_link.href)  
    
    #Retrieve comments
    comment_feed = comments_generator(yt_service, video_id)
    
    #Data structure for only the comments
    comments = []
        
    for comment in comment_feed:
        #author_name = comment.author[0].name.text
        text = comment.content.text.strip()    
        # Fixes most of the strange characters in the text
        text = text.replace(b'\xEF\xBB\xBF', b'') 
        #text = text.decode('utf-8-sig')
        #text = text.encode('utf-8') 
        
        #Put only the comments in a new data structure    
        comments.append(text)
    
        #print the comments    
        #print("{}: {}".format(author_name, text))

    return comments

#different videos for testing
video1 = '39Uib7XW57k' #HoM "go to the mall" 32 comments, fast to load
video2 = '0Vyj1C8ogtE' #scotty 15507 comments - limits at API

#Get the comments
video_comments = GetComments(video1)

#Checking if comments are retrieved
i = 0
for x in video_comments:
    print x
    i += 1

print i