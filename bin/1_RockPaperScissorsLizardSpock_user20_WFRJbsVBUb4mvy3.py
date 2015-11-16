# Rock-paper-scissors-lizard-Spock game by Dennis van den Berg


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors


## import modules

import random


## helper functions

def number_to_name(number):
    # convert number to a name using if/elif/else
    if number == 0:
        name = "rock"
    elif number == 1:
        name = "Spock"
    elif number == 2:
        name = "paper"
    elif number == 3:
        name = "lizard"
    else:
        name = "scissors"
    return name


def name_to_number(name):
    if name == "rock":
        number = 0
    elif name == "Spock":
        number = 1
    elif name == "paper":
        number = 2
    elif name == "lizard":
        number = 3
    else:
        number = 4
    return number


def rpsls(player_name): 
    # convert name to player_number using name_to_number
    player_number = name_to_number(player_name)
    
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 5)
    
    # compute difference of player_number and comp_number modulo five
    player_comp_difference = (player_number - comp_number) % 5
    
    # use if/elif/else to determine winner
    if player_comp_difference == 1 or player_comp_difference == 2:
        winner = "Player"
    elif player_comp_difference == 3 or player_comp_difference == 4:
        winner = "Computer"
    else:
        winner = "None"
        
    # convert comp_number to comp_name using number_to_name
    comp_name = number_to_name(comp_number)
    
    # print results
    print "Player chooses " + number_to_name(player_number)
    print "Computer chooses " + comp_name
    if winner == "None":
        print "Player and computer tie!"
    else:
        print winner + " wins!"
    print ""


## test code

rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")