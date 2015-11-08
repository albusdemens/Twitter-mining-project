# -*- coding: utf-8 -*-
"""
Script: Message_Saver
Version: 0.1
Course: 02819 Data Mining using Python
Assignment: Exam: Python code file
Author: Mikkel Holm Abrahamsen (s132440)

The long-term goal of this script is to aid me later when I am mining web data 
e.g. Twitter 'tweets'. The current version takes user input and saves it,
using the interactive interpreter.
"""

import datetime
import sys

class Message_Saver:
    
    """Message_Saver allows the user to write messages which are saved to
    a file. These files can also be loaded again."""
        
    def __init__(self, filename):
        """The file extension should be .txt, so any periods and trailing
        characters are removed and replaced by ".txt".
        
        Keyword arguments:
        filename -- the name of the file which messages are saved to.
        
        """
        
        self.filename = str(filename).split('.')[0]
        self.filename += ".txt"
        self.username = ''
        
    def store_message(self):
        """Writes the latest user input to a file. Must be called after
        the variable 'user_input' is set."""
        
        # This should be optimized when used in a different context, but for
        # the purpose of this script, it should work.
        message = user_input        
        
        # Open a file and prepare for saving by adding a timestamp.
        # If file opening fails, the program will exit.                                 
        try:
            with open(self.filename, 'a') as f:
                date_time = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M")
                text_record = "{0} {1}: {2}\n".format(date_time,self.username,message)
                f.write(text_record)
        except IOError:
            sys.stderr.write("Could not open file! Exiting..\n")
            sys.exit()
            
    def load_data(self):
        """Loads the previously saved data (that has the same name as
        specified when the script was started) and prints it. If the file
        is not found, the program will exit."""
        
        sys.stdout.write("Loading previously recorded messages..\n")
        try:
            with open(self.filename, 'r') as f:
                sys.stdout.write("\n" + f.read() + "\n")
        except IOError:
            sys.stdout.write("Could not open file!\n")
            
    def set_name_prompt(self):
        """Prompts the user to input a new name that will be used to label
        the records of messages that are saved."""
        
        username = raw_input("Would you kindly enter a hilarious fake username?\n-->")
        # Check to see if the username is valid (anything but just whitespace)
        while (''.join(username.split()) == ''):
                sys.stderr.write("Empty or invalid username! "
                                 "Please set a username.\n")
                username = raw_input("Try a name again:\n-->")
                
        self.username = username.upper()                                 
        sys.stdout.write("Username changed to: '{0}'\n".format(username))
        
    def get_help(self):
        """Writes a short message about the user's options."""        
        
        sys.stdout.write("\nThese are your options:\n"
                 "- Write messages that are saved to a file\n"
                 "- Print previously saved messages by typing 'load_data'\n"
                 "- Change your current user name by typing 'change_name'\n"
                 "- Quit the program by typing 'quit'\n\n")

# MAIN LOOP SECTION STARTS HERE
# Here is what will be run when the script is run            
print "\nHello reviewer. Welcome to the program created by student s132440\n"

filename = raw_input("Please enter a filename without extension"
                     " (for example 'unimaginative')\n-->")
ts = Message_Saver(filename)
ts.set_name_prompt()

# Depending on what the user writes, we want different things to happen.
options = {"load_data": ts.load_data,
           "change_name": ts.set_name_prompt,
           "help": ts.get_help,
           "quit": exit}    

# The message/input loop which runs until the program is shut down.
while True:
    user_input = raw_input("Write messages or write 'help':\n-->")
    options.get(user_input, ts.store_message)()
# END OF MAIN LOOP SECTION