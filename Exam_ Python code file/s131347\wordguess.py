import urllib2
import re

# Prompt user for name and give some instructions for the game
name = raw_input("What is your name? ")
print "\nHi %s!" %(name)
print "\nA random word has been chosen using the Random Word API at randomword.setgetgo.com\n"
print "You have 10 tries to guess the letters. After 10 incorrect letter guesses you will \nhave one final chance to guess the word.\n"

# Get a random word using setgetgo Random Word API
word = urllib2.urlopen("http://randomword.setgetgo.com/get.php").read()
# Removing extra spaces/characters in the string and making sure it is all lowercase
word = word[3:len(word)-2]
word = word.lower()
# Find the unique letters in the word
unique = list(set(word))

# Inform player of length of word
print "The length of the word is %i letters. Good luck!\n" %(len(word))

# Empty matrix that will contain guessed letters
guessed = ''
# Number of wrong guesses allowed
tries = 10;
# All letters of the alphabet for check
alph = 'abcdefghijklmnopqrstuvwxyz'
# Empty matrix that will contain the letters guessed correctly
correct = ''

# Continue until the user has made 10 incorrect guesses 
while tries > 0:
	
	# Show guessed letter present in the word, otherwise show a dash.
	for char in word:
		if char in guessed:
			print char,
		else:
			print "-",
	
	# Prompt the user to guess a letter
	letter = raw_input("\nGuess a letter [a-z]: ")		
	
	# Prompt user again if character was not a letter of the alphabet or if more
	# than one character was entered	
	while (len(letter)!=1) or (letter not in alph):
		print "You must enter a single letter [a-z].\n"
		letter = raw_input("Guess a letter [a-z]: ")
	
	# If the letter has not been previously guessed add it 'guessed'
	if (letter not in guessed):
		guessed = guessed + letter
		# If the letter is in the word add it to 'correct' 
		if (letter in word):
			correct = correct + letter
		# If the letter is not in the word subtract a try
		if (letter not in word):
			tries -= 1
	
	# If the correctly guessed letters match the unique letters of the word
	# the user wins and the program exits
	corr_list = list(set(correct))
	if corr_list == unique:
		print ("\n%s") %(word)
		print "\nYou guessed the word. You win!"
		break
	
	
	# If the user has not yet won, inform of how many tries are left and 
	# which letters have been guessed
	if tries > 0:
		print "\nYou have %i guesses left." %(int(tries))
		print "The letters guessed so far are [%s].\n" %(guessed)

# When the user runs out of tries prompt for one final guess of the word
# and check if it is correct
if tries == 0:
	word_guess = raw_input("You have 0 tries left. You must now guess the word: ")
	if word_guess == word:
		print("Correct. You win!")
	else:
		print "Incorrect. The word was %s." %(word)

# end