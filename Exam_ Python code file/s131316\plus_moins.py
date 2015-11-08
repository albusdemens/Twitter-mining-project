# game of plus/minus in python:
# the player has to find a random number between 1 and a chosen limit

import random

playing = True
MIN = 1

print ("Welcome to the plus-minus python game !")

# main loop, the program keeps on running until the player wants to stop
while playing == True:

	win = False
	nb_try = 0

	# getting the limit according to the level chosen by the player
	try:
		level = int(raw_input('Choose a level : 1, 2 or 3'))
	except:
		print("Not a number ...")

	if level == 1:
		maxi = 100
	elif level == 2:
		maxi = 1000
	elif level ==3:
		maxi = 10000

	# generating the mystery number between 1 and the limit	
	mystery_nb = random.randint(1, maxi)

	# game loop, runs until the number is found
	while win == False:

		# counting the number of tries it takes the player to find the number
		nb_try = nb_try + 1	

		try:
			entry = int(raw_input('Enter an integer between 1 and %s?'%(maxi)))
		except:
			print("Not a number ...")

		# comparing the user's value with the mystery number	
		if entry < mystery_nb:
			print ("Too low")
		elif entry > mystery_nb:
			print ("Too high")
		elif entry == mystery_nb:
			print ("Congratulation you found the mystery number in %s tries!!" %(nb_try))	
			win = True	

	# checking if user wants to keep on playing or not
	keepPlaying = raw_input('Do you want to play another game ? (y/n)')	
	if keepPlaying == 'y':
		playing = True
	elif keepPlaying == 'n':
		playing = False