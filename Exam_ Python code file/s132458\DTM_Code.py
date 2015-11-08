#### INSTRUCTIONS ####
'''
You can use pip to install the three libraries I'm using:
pip install twitter
pip install json
pip instal tkinter

To be able to run the code you need a Twitter Developer account and an registered application.
It's free and it takes 2 minutes. See here:

If you cannot figure it out, here's an image of the result:
http://mathiasmortensen.com/dmp.png
Or better yet, here's the file with my Twitter friends you can save to the same directory as this file:
http://mathiasmortensen.com/friends.txt
'''

import twitter
import json
from Tkinter import *

#----Connect to Twitter
def oauth_login():
    CONSUMER_KEY = '' #Insert
    CONSUMER_SECRET = ''#Insert
    OAUTH_TOKEN = ''#Insert
    OAUTH_TOKEN_SECRET = ''#Insert
    
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
                               
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

twitter_api = oauth_login()


#----Get friends and save to file
def update_friends():
    friends = twitter_api.friends.ids(screen_name='') #Insert your own screen name here

    with open('friends.txt', 'w') as outfile:
        json.dump(str(friends['ids']).strip('[]'), outfile)

    print "friends list has been updated"

# Only call the first time you run the script
#update_friends()

#----Read from file
def read_friends_from_file():
    friends_file = open('friends.txt')
    friends_ids = json.load(friends_file)
    friends_file.close()
    print "friends read"
    return friends_ids

#----GUI
root = Tk()

root.title('Your Twitter Friends')
root.geometry("450x450+450+450")

#Display Twitter friends
text = Text(root)
text.insert(INSERT, "friends: ")
text.insert(END, read_friends_from_file())
text.pack()

text.tag_add("highlight", "0.0", "1.7")
text.tag_config("highlight", background="yellow", foreground="blue")


root.mainloop()



