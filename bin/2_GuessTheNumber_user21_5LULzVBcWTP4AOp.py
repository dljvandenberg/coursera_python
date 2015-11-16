# "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console


## import modules

import random
import math
import simplegui


## define helper functions

def maxturns(maxrange):
    """ calculate maximum necessary number of turns """
    return math.ceil(math.log(maxrange+1, 2))

def newgame(max):
    """ set maxrange to guess from, determine secret number, reset turn counter """
    global maxrange, secret, turn
    maxrange = max
    secret = random.randrange(0, max)
    turn = 0
    print "\nNew game: choose from [0,"+str(max)+")"

        
## initialize global variables maxrange, secret, turn using newgame()

newgame(100)


## define event handlers for control panel
    
def range100():
    """ button that changes range to [0,100) and restarts """
    newgame(100)
    
def range1000():
    """ button that changes range to [0,1000) and restarts """
    newgame(1000)

def get_input(guess):
    """ compares guess to secret, new game after maxturns or correct answer """
    global turn
    if int(guess) == secret:        
        print str(guess)+" is correct!"
        newgame(maxrange)
    elif int(guess) < secret:
        print "Higher than "+str(guess)
        turn +=1
        if turn >= maxturns(maxrange):
            print "Maximum allowed turns has been reached."
            newgame(maxrange)
    elif int(guess) > secret:
        print "Lower than "+str(guess)
        turn += 1
        if turn >= maxturns(maxrange):
            print "Maximum allowed turns has been reached."
            newgame(maxrange)

        
## create frame
frame = simplegui.create_frame("Guess the number", 200, 200)


## register event handlers for control elements
textinput = frame.add_input("Guess", get_input,100)
button100 = frame.add_button("Range: 0 - 100", range100,100)
button1000 = frame.add_button("Range: 0 - 1000", range1000,100)


## start frame
frame.start()
