# -*- coding: utf-8 -*-
"""
Yahtzee roller!
Created on Wed Oct 02 19:01:14 2013

This script has been tested in Python 2.7.5.
'raw_input' is not included in Pyhon 3.x

@author: Andreas Svendsen (s072623)
"""
import random

numDice = 5 # Number of dice to roll
dieSides = 6 # Number of sides on each die
maxNumRolls = 3 # Total number of rolls allowed per turn
reply = 's'

while (reply != 'q'):

    # First, the dice are rolled:
    dice = []
    for i in range(numDice):
        dice.append(randint(1,dieSides))
    numRolls = 1

    # The roll is displayed to the user, and the user inputs a choice which is testeed for validity
    print('You rolled: ' + repr(dice))
    reply=raw_input('Would you like to (q)uit, (r)eroll or start (n)ew turn?\n')
    while(reply != 'q' and reply != 'r' and reply != 'n'):
        print('Invalid response! Please enter one of the following characters: q, r, n.\n')
        reply=raw_input('Would you like to (q)uit, (r)eroll or start (n)ew turn?\n')
    
    # If r for reroll is selected, the rerolling commences:
    if (reply == 'r'):
        while (numRolls < maxNumRolls):
            print('You have ' + repr(maxNumRolls - numRolls) + ' roll(s) left including this one.\n')
            dieNum = 1
            for j in range(numDice):
                print('Die number ' + repr(dieNum) + ' is: ' + repr(dice[j]))
                dieNum += 1

            keepers = [] # List of dice that shall not be rerolled
            keeper = 1 # keeper is just initialized so the while-loop below can start
            
            while(keeper != 0):
                keeper = int(raw_input('Please enter die number of a die you want to keep (0 finalises keeper list): '))
                if keeper != 0:
                    if (keeper > 0 and keeper <= numDice):
                        keepers.append(keeper)
                    else:
                        print('Invalid die number! Please input a number between 1 and ' + repr(numDice))
                    print('The keeper list is currently: ' + repr(keepers))

            print('Rerolling...')
            for i in range(numDice):
                if (i+1) not in keepers:
                    dice[i] = randint(1,dieSides)

            print('New roll reveals: ' + repr(dice))
            numRolls +=1

        reply=raw_input('Would you like to (q)uit or start (n)ew turn?\n')
        while(reply != 'q' and reply != 'n'):
            print('Invalid response! Please enter one of the following characters: q, n.\n')
            reply=raw_input('Would you like to (q)uit or start (n)ew turn?\n')
