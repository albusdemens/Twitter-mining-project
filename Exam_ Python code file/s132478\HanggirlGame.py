# Python Code File
# By: Jacob Elbæk, s132478
# Hangman Game, in favor of the boys
# The game might have some errors, sorry about that

# Imports the random library
import random

# Defines the drawings for the game, turn by turn
drawing = [
'  *----*   \n  |    |   \n      |   \n      |   \n      |   \n      |   \n========= \n',
'  *----*   \n  |    |   \n  0~   |   \n      |   \n      |   \n      |   \n========= \n',
'  *----*   \n  |    |   \n  0~   |   \n  |    |   \n      |   \n      |   \n========= \n',
'  *----*   \n  |    |   \n  0~   |   \n /|    |   \n      |   \n      |   \n========= \n',
'  *----*   \n  |    |   \n  0~   |   \n /|\\   |   \n      |   \n      |   \n========= \n',
'  *----*   \n  |    |   \n  0~   |   \n /|\\   |   \n /    |   \n      |   \n========= \n',
'  *----*   \n  |    |   \n  0~   |   \n /|\\   |   \n / \\  |   \n      |   \n========= \n'
]

# Defines the Hangirl class
class Hanggirl:
        def __init__(self,word):
                self.word = word
                self.wrong_letters = []
                self.guessed_letters = []

        # Checks the guesses      
        def guess(self,letter):
                # Checks whether the guessed letter is already in the guessed letters
                if letter in self.word and letter not in self.guessed_letters:
                        self.guessed_letters.append(letter)
                # Checks whether the guessed letter is already in the wrong letters
                elif letter not in self.word and letter not in self.wrong_letters:
                        self.wrong_letters.append(letter)
                else:
                        return False
                return True
       
        def hanggirl_won(self):
                if '_' not in self.hidden_letter():
                        return True
                return False

        # Show the letter if it is correct, else make it stay hidden
        def hidden_letter(self):
                rtn = ''
                for letter in self.word:
                        if letter not in self.guessed_letters:
                                rtn += '_'
                        else:
                                rtn += letter
                return rtn
        
        def hanggirl_over(self):
                return self.hanggirl_won() or (len(self.wrong_letters) == 6)
        
        # Print feedback for the user        
        def status(self):
                print drawing[len(self.wrong_letters)]
                print 'Word: ' + self.hidden_letter()
                print '\nWrong Letters: ', 
                for letter in self.wrong_letters:
                        print letter, 
                print 
                print '\nGuessed Letters: ',
                for letter in self.guessed_letters:
                        print letter,
                print 

# Defines the words that the user might have to guess. 
def guessWord():
        
        words = ['python','assignment','programming']
        return words[random.randint(0,len(words))]

def main():
        
        HanggirlGame = Hanggirl(guessWord())
        # When the game is not over, prompt the user to enter a letter
        while not HanggirlGame.hanggirl_over():
                HanggirlGame.status()
                user_input = raw_input('\nEnter a letter: ')
                HanggirlGame.guess(user_input)

        # Print the status of the game, depending on the outcome
        HanggirlGame.status()	
        if HanggirlGame.hanggirl_won():
                print '\nYou totally saved that girl!'
        else:
                print '\nShe died!'
                
if __name__ == "__main__":
        main()
        
        
