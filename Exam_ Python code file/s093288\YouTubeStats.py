# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 10:55:58 2013

@author: Martin

Program for analysing comments of YouTube videos

This program will take the video ID of a YouTube video and then 
analyse it's comments. It will use the AFINN list of weighted 
words to find the comments that uses the most positive words, 
negative words and the comments that uses the most of both
positive and negative words.
It will also give an overall average of the comments, where an
average of above 0 means that the users are in general making
comments in a positive way, while an average belove 0 means the
opposite.
"""

import re
import gdata
import gdata.youtube.service

#The video ID. Right now set to match Andy McKee's video of "Drifting"
#Try to insert different video ID's to see what the user's think of
#different artists. 
videoID = "Ddn4MGaS3N4"

yts = gdata.youtube.service.YouTubeService()
ytfeed = yts.GetYouTubeVideoCommentFeed(video_id=videoID)
#Getting the comments for the video
comments = [ comment.content.text for comment in ytfeed.entry ]
firstComment = comments[0]

entry = yts.GetYouTubeVideoEntry(video_id=videoID)
#Printing information on the video
print 'Video title: %s' % entry.media.title.text
print 'Video view count: %s' % entry.statistics.view_count
print 'Video rating: %s' % entry.rating.average

#Reading in the AFINN word list file, code also used in slides
#Make sure the file is somewhere where it can be read...
filenameAFINN = 'AFINN/AFINN-EN.txt'
afinn = dict(map(lambda (w, s): (w, int(s)), [ 
            ws.strip().split('\t') for ws in open(filenameAFINN) ]))
            
# Word splitter pattern
pattern_split = re.compile(r"\W+")

#Main method for the program
def sentiment(comments):
    #Initializing variables:
    totalSent = 0
    worstComment = comments[0]
    bestComment = comments[0]
    emotionalComment = comments[0]
    worstCommentValue = float("inf")
    bestCommentValue = float("-inf")
    emotionalCommentValue = 0
    totalPositive = 0
    totalNegative = 0
    totalAbsolute = 0
    #Going throught the comments to get the most positive/negative
    #comment
    for comment in comments:
        words = pattern_split.split(comment.lower())
        #Assign values to the words of the comment (code also from
        #slides):
        sentiments = map(lambda word: afinn.get(word, 0), words)
        if sentiments:
        #Here the method for evaluating how positive / negative
        #a comment is, is simply the sum of the words's values.
        #This method is choosen, as compared to for instance 
        #normalizing the sum, because summing gives larger 
        #values for long comments, and long comments tends to 
        #express the most emotions.
        #The absoluteSentiments look at the sum of the absolute of the
        #words in the comment to give an expression for how many weighted
        #words are in the comment:
            absoluteSentiments = float(sum(map(lambda x: abs(x), sentiments)))
            totalAbsolute = totalAbsolute + absoluteSentiments
            #The code below stores the total amount of positive and
            #total amount of negative words in all the comments
            for b in sentiments:
                if b > 0:
                    totalPositive = totalPositive + b
                if b < 0:
                    totalNegative = totalNegative + b
            sentiments = float(sum(sentiments))
            totalSent = totalSent + sentiments
            #The code below stores the comments with most postive words,
            #negative words and positive + abseloute of negative words
            if sentiments > bestCommentValue:
                bestCommentValue = sentiments
                bestComment = comment
            if sentiments < worstCommentValue:
                worstCommentValue = sentiments
                worstComment = comment   
            if absoluteSentiments > emotionalCommentValue:
                emotionalCommentValue = absoluteSentiments
                emotionalComment = comment    
        else:
            sentiments = sentiments + 0
    #Printing all the data:
    print "Best comment: %s" % bestComment
    print "With value: %s" % bestCommentValue
    print "Worst comment: %s" % worstComment
    print "With value: %s" % worstCommentValue
    print "Most emotional comment: %s" % emotionalComment
    print "With value: %s" % emotionalCommentValue
    print
    print "Total positive comments value: %s" %totalPositive
    print "Total negative comments value: %s" %totalNegative
    print "Total emotional comments value: %s" %totalAbsolute
    return totalSent/len(comments)

#Calling the function and printing the average sentiment of the
#comments
print 'Average sentiment rating: %s' % sentiment(comments)