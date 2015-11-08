"""
The game of Yatzy. 

This is a simple version of Yatzy, where the game belive in people, and the
userinput. It's not a finished game, but a good start.
"""

#Imports
from random import randint

def list_to_string(list_to_convert):
    """Returns a string with a commaseperatet list from the list"""
    return str(list_to_convert).strip('[]')

class DiceCup:
    """Implement a dice bear, with n cubes"""
    
    def __init__(self, number_of_cubes=5, eyes=6):
        self.rolls = []
        self.number_of_cubes = 0
        self.eyes = eyes

        #Sets the number of cubes, and evaluate the input
        self.set_number_of_cubes(number_of_cubes)


    def get_number_of_cubes(self):
        """Returns the number of cubes"""
        return self.number_of_cubes
    
    def set_number_of_cubes(self, number_of_cubes):
        """Set the number of cubes, and make sure it's correct"""
        try:
            self.number_of_cubes = int(number_of_cubes)
            if self.number_of_cubes < 0:
                print "You can't have a negative number of cubes!"
                print " Cubes set to 5"
                self.number_of_cubes = 5
        except ValueError:
            print("That's not an int!")

    def get_last_roll_string(self):
        """Returns a string with a commaseperatet list of the cubes"""
        return list_to_string(self.rolls)

    def get_last_roll(self):
        """Returns the last roll"""
        return self.rolls

    def raffel(self):
        """Raffel the bear with all the cubes"""
        self.rolls = []
        for _ in range(self.number_of_cubes):
            self.rolls.append(randint(1, self.eyes))

        self.rolls.sort()        
        return self.rolls

    def reraffel(self, saved_cubes):
        """Raffel the bear, without the cubes who was put away. (and given)"""
        self.rolls = saved_cubes
        for _ in range((self.number_of_cubes - len(saved_cubes)) ):
            self.rolls.append(randint(1, self.eyes))
        
        self.rolls.sort()
        return self.rolls

class Rules:
    """The rules of the game"""

    def __init__(self):
        self.cubes = []

    def set_cubes(self, cubes):
        """Set the cubes value"""
        self.cubes = cubes
        
    def ones(self):
        """Return value for ones"""
        return self.cubes.count(1)

    def twos(self):
        """Return value for twos"""
        return self.cubes.count(2) * 2

    def threes(self):
        """Return value for trees"""
        return self.cubes.count(3) * 3

    def fours(self):
        """Return value for fours"""
        return self.cubes.count(4) * 4

    def fives(self):
        """Return value for fives"""
        return self.cubes.count(5) * 5

    def sixes(self):
        """Return value for sixs"""
        return self.cubes.count(6) * 6


class Game:
    """The game_class, who controles the game"""
    
    def __init__(self):
        #self.playser = {0: {'name': 'Thomas', points: {'ones': 4, 'Fives': 0}}}
        self.players = {}
        #we ues the "simple" yatzy.
#        self.types_of_roles = ["Ones", "Twos", "Threes", "Fours", "Fives", \
#                       "Sixes", "One Pair", "Two Pairs", \
#                       "Three of a Kind", "Four of a Kind", \
#                       "Small Straight", "Large Straight", \
#                       "House", "Yatzy", "Chance" 
#                      ]
        self.types_of_roles = ["Ones", "Twos", "Threes", "Fours", "Fives", \
                               "Sixes"
                              ]

        self.turn = 0
        self.player_turn = 0
        
        #get rules
        self.rules = Rules()

        #make a dice_bear
        self.bear = DiceCup()
        
        #Set all the players names.
        self.set_players()
        
        #Start the game
        self.play()
        

        
    def set_players(self):
        """Set the players names"""
        
        print """Type in the players name. When you have added all players, 
                 press enter to type in a blank line, and start the game."""
        player_count = 0
        name = None
            
        #Make sure the name is not empty or two players has the same name.
        while (name != None or name != ""):
            name = raw_input("What is player%i's name: " % (player_count+1))

            #If the name exist
            if name in self.get_players_list():
                print "The name is already in use, please select an other name."
            #If the name is empty (finished typing in players
            elif name == "":
                player_count -= 1
                print "%i players added: (%s)" % (player_count+1, \
                                                  self.get_players_string())
                break
            #else read new player name.
            else:
                self.players[player_count] = {'name': name, 'points': {}}
                player_count += 1
    
    def game_end(self):
        """See if the game is finished."""
        if self.turn >= len(self.types_of_roles):
            return True
        else:
            return False
    
    def play(self):
        """Controle the gameplay""" 
        while not self.game_end():
            print "%s's tur, round: %i" % \
                (self.players[self.player_turn]['name'], self.turn)
            command = raw_input("What to do?: ")
            if command.lower() == "raffel" or command == 'roll':
                print "Raffels: %s" % self.bear.raffel()
                self.turn += 1
            elif command.lower() == 'moves':
                print self.get_moves_points_string()
            elif command.lower() in ['ones', 'twos', 'threes', 'fours', \
                                     'fives', 'sixes']:
                print self.make_move(command.lower())
                self.next_turn()
            elif command.lower() == 'points':
                print self.see_points_string()
            else:
                print "Unknown command."

        print "Game Ended. Someone won!"

    def get_moves(self):
        """Return list of moves, who haven't been used."""
        return list(set(self.types_of_roles) - \
                    set(self.players[self.player_turn]['points'].keys()) )

    def get_moves_points_string(self):
        """Returns a string with the posible moves and there points."""
        #Get a list of the posible moves
        moves = self.get_moves()

        #Make an empty string for the return string.
        moves_string  = ""

        #Set the cubes for the points.
        self.rules.set_cubes(self.bear.get_last_roll())

        #Makes the string with if-sentens.
        if "Ones" in moves:
            moves_string += "Ones: " + str(self.rules.ones()) + " points, "

        if "Twos" in moves:
            moves_string += "Twos: " + str(self.rules.twos()) + " points, "

        if "Threes" in moves:
            moves_string += "Threes: " + str(self.rules.threes()) + " points, "

        if "Fours" in moves:
            moves_string += "Fours: " + str(self.rules.fours()) + " points, "

        if "Fives" in moves:
            moves_string += "Fives: " + str(self.rules.fives()) + " points, "

        if "Sixes" in moves:
            moves_string += "Sixes: " + str(self.rules.sixes()) + " points, "

        #Return the whole string (minus the last ", "
        if len(moves_string) > 1:
            return moves_string[:-2]
        else: #Can't orcure!
            return "There are no moves"
            
    def get_players_string(self):
        """Returns a string with a commaseperatet list of all players"""
        return list_to_string([self.players[names]['name'] \
               for names in self.players.keys()])

    def get_players_list(self):
        """Returns a string with a commaseperatet list of all players"""
        return [self.players[names]['name'] for names in self.players.keys()]

    def make_move(self, section):
        """Make a move, and save the points for the player"""
        
        #Sets the rules cubes.
        self.rules.set_cubes(self.bear.get_last_roll())
        
        if section == 'ones':
            points = self.rules.ones()
        if section == 'twos':
            points = self.rules.twos()
        if section == 'threes':
            points = self.rules.threes()
        if section == 'fours':
            points = self.rules.fours()
        if section == 'fives':
            points = self.rules.fives()
        if section == 'sixes':
            points = self.rules.sixes()
        self.players[self.player_turn]['points'][section] = points
        return "%i points added to %s" % (points, section)
        
    def see_points_string(self):
        """Returns a string with playernams and points."""
        points_string = ""
        
        for player in range(len(self.players)):
            if len(self.players[player]['points']) > 0:
                points = sum(self.players[player]['points'].values())
            else:
                points = 0 

            points_string += self.players[player]['name'] + ": " + \
            str(points) + ", "

        return points_string[:-2]
        
    def next_turn(self):
        """Control the turns."""
        number_of_players = len(self.players)
        
        #Next player
        self.player_turn += 1
        
        #If we reached max players, start over, and make the round +1
        if (self.player_turn == number_of_players):
            self.player_turn = 0
            self.turn += 1

Game()

