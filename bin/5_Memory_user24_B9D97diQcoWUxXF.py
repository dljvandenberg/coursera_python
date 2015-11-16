# implementation of card game - Memory

import simplegui
import random


# parameter for debugging
DEBUG = False


# define parameters
CARDRANGE = range(0, 8)
# CARDRANGE = ['P', 'Y', 'T', 'H', 'O', 'N']
CARDWIDTH = 50
CARDHEIGHT = 2 * CARDWIDTH
TEXTSIZE = int(CARDWIDTH)


# helper function to initialize globals
def new_game():
    global cardlist, exposed, lastcardnum, previouscardnum, clicknum

    # card order
    cardlist = CARDRANGE + CARDRANGE
    random.shuffle(cardlist)

    # exposed and previous cards
    exposed = [False for cardnum in cardlist]
    lastcardnum = None
    previouscardnum = None
    
    # number of clicks
    clicknum = 0
        
    # DEBUG
    if DEBUG:
        print "new_game: cardlist =", cardlist
        print "new_game: exposed =", exposed
        print "new_game: clicknum =", clicknum

    
# mouseclick handler
def mouseclick(pos):
    global lastcardnum, previouscardnum, clicknum
    
    # determine index of card clicked on
    if pos[1] >= 0 and pos[1] < CARDHEIGHT and pos[0] >= 0 and pos[0] < len(cardlist) * CARDWIDTH:
        cardnum = pos[0] / CARDWIDTH
        
        # if not exposed yet: update number of clicks, cover unmatched previous cards, expose current card
        if exposed[cardnum] == False:

            # update number of clicks
            clicknum += 1               

            # cover unmatched previous cards in case of first click of current turn
            if clicknum % 2 == 1 and clicknum > 2:
                if cardlist[previouscardnum] != cardlist[lastcardnum]:
                    exposed[previouscardnum] = False
                    exposed[lastcardnum] = False
                
            # expose current card
            exposed[cardnum] = True
            
            # update previously clicked cards
            previouscardnum = lastcardnum
            lastcardnum = cardnum

        
        # DEBUG
        if DEBUG:
            print "mouseclick: cardnum", cardnum
            print "mouseclick: cardvalue", cardlist[cardnum]
            print "mouseclick: exposed[cardnum]", exposed[cardnum]
        

# draw handler
def draw(canvas):
    # draw cards
    for cardnum in range(len(cardlist)):
        if exposed[cardnum]:
            canvas.draw_text(str(cardlist[cardnum]), ((cardnum + 0.21) * CARDWIDTH, 0.62 * CARDHEIGHT), TEXTSIZE, 'White')
        else:
            canvas.draw_polygon([[cardnum * CARDWIDTH, 0], [(cardnum + 1) * CARDWIDTH - 1, 0], [(cardnum + 1) * CARDWIDTH, CARDHEIGHT - 1], [cardnum * CARDWIDTH, CARDHEIGHT - 1]], 2, 'Green', 'Black')

    # derive number of turns from number of clicks and update label
    label.set_text("Turns = " + str((clicknum + 1) // 2))


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 2 * CARDWIDTH * len(CARDRANGE), CARDHEIGHT)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
