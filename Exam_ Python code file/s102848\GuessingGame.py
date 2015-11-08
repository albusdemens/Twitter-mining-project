#!/usr/bin/python

"""GuessingGame 

Game: the program will guess the number you are thinking of in log2(N) guesses
Used packages: Tkinter and tkMessageBox"""
__author__ = "Pascal Timshel (s102848)"
__copyright__ = "No Copyright"

from Tkinter import *
import tkMessageBox

tries = 0
min_bound = 0
max_bound = 10
guess = int((min_bound + max_bound)/2)
def callback(user_response):
    """Main algotihm for GuessingGame"""
    global tries 
    global min_bound 
    global max_bound     
    global guess
    tries += 1    
  
    if user_response == "higher":
        min_bound = guess + 1
    if user_response == "lower":
        max_bound = guess - 1
    if user_response == "correct":
        str_msg = "Haha, I guessed your number in %d guesses - I am so good.\nComputers FTW!" % tries
        tkMessageBox.showinfo("Game over", str_msg)
        root.destroy()
    if min_bound > max_bound:
        str_msg = "Now you are lying to me... I only play with fair players. \nGoodbye!"
        tkMessageBox.showwarning("Warning", str_msg)
        root.destroy()
    if min_bound == max_bound:
        str_msg = "Ahhh, now I know what number you were thinking of. It was %d!" %max_bound
        tkMessageBox.showinfo("Game over", str_msg)
        root.destroy()
        
    guess = int((min_bound + max_bound)/2)
    guess_current.set("My guess is %d" % guess)
    status_guess.set("Guess number %d." % tries)
 
def remove_widgets():
    """ Removes widgets prior to playing game """
    l_guess.grid_remove()
    l_status.grid_remove()
    b_lower.grid_remove() 
    b_correct.grid_remove() 
    b_higher.grid_remove() 

def show_widgets():
    """ Shows widgets """
    l_guess.grid()
    l_status.grid()
    b_lower.grid()
    b_correct.grid()
    b_higher.grid()


def show_rules():
    """ Displays a tkMessageBox with the rules of the game """
    rules = """ Think of a number between 0 and 10.
I will use my computer powers to try an guess you number in less than log2(11)=~4 tries - can you explain why?
Click the button "you've got it!" if my guess is correct
Click the button "higher" if your number is higher than my guess
Click the button "lower" if your number is lower than my guess"""
    tkMessageBox.showinfo("Rules", rules)


def play_game():
    """ Initiatiates game by displaying widgets and callback """
    b_play.grid_remove()
    show_widgets()
    callback(None)
    

# Scripting level code
root = Tk() # Main root window
root.title("Guessing Game")
#root.geometry("300x225")


b_rules = Button(root, text="Rules", command=show_rules)
b_rules.grid(row=0, column=0)

b_play = Button(root, text="Play", command=play_game)
b_play.grid(row=0, column=1)

# frame widget for decoration (seperation)
separator = Frame(height=50, bd=2, relief=SUNKEN)
separator.grid(row=1, columnspan=3, padx=5, pady=5)

guess_current = StringVar()
l_guess = Label(root, textvariable=guess_current)
guess_current.set("My guess is %d" % guess)
l_guess.grid(row=2, columnspan=3)

status_guess = StringVar()
l_status = Label(root, textvariable=status_guess)
status_guess.set("Guess number %d." % tries)
l_status.grid(row=3, columnspan=3)

b_lower = Button(root, text="lower", command=lambda: callback("lower"))
b_lower.grid(row=4, column=0)

b_correct = Button(root, text="you've got it!", command=lambda: callback("correct"))
b_correct.grid(row=4, column=1)

b_higher = Button(root, text="higher", command=lambda: callback("higher"))
b_higher.grid(row=4, column=2)

# Initiating Tkinter GUI
remove_widgets()
root.mainloop()


# DEBUGGING STUFF
#    print "user response", user_response
#    print "min_bound", min_bound
#    print "max_bound", max_bound
#    print "guess", guess    
#    

