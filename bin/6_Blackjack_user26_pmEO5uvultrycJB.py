# Mini-project #6 - Blackjack

import simplegui
import random

# For debugging purposes
DEBUG = False

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

DEALER_CARD_POSITION = (50, 250)
PLAYER_CARD_POSITION = (50, 400)

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    
    
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        description = "Hand contains"
        for card in self.hand:
            description += " " + str(card)
        return description
 
    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        contains_ace = False
        for card in self.hand:
            value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                contains_ace = True
        if contains_ace and value + 10 <= 21:
            value += 10            
        return value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        position = list(pos)
        for card in self.hand:
            card.draw(canvas, position)
            position[0] += 1.2 * CARD_BACK_SIZE[0]
            
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck.append(card)

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal last card object from the deck
        card = self.deck.pop()
        return card
            
    def __str__(self):
        # return a string representing the deck
        description = "Deck contains"
        for card in self.deck:
            description += " " + str(card)
        return description

    
#define event handlers for buttons
def deal():
    global deck, hand_player, hand_dealer, outcome, in_play, score

    outcome = "Hit or stand?"

    if in_play == True:
        outcome = "New deal while still in play. Lost round.."
        score += -1
    
    # create and shuffle the deck (stored as a global variable)
    deck = Deck()
    deck.shuffle()

    # create new player and dealer hands (stored as global variables)
    hand_player = Hand()
    hand_dealer = Hand()
    
    # add two cards to each hand
    hand_player.add_card(deck.deal_card())
    hand_dealer.add_card(deck.deal_card())
    hand_player.add_card(deck.deal_card())
    hand_dealer.add_card(deck.deal_card())
    
    # DEBUG: hands should be printed to the console with an appropriate message 
    if DEBUG:
        print "Player:", hand_player
        print "Dealer:", hand_dealer
        
    in_play = True

def hit():
    global deck, hand_player, outcome, in_play, score

    # if the player has busted, remind the player that they have busted.
    if hand_player.get_value() > 21:
        outcome = "You have busted. New deal?"
        pass

    # if the hand is in play, hit the player
    if in_play:
        hand_player.add_card(deck.deal_card())
    
        # if busted, assign a message to outcome, update in_play and score
        if hand_player.get_value() > 21:
            outcome = "You have busted. New deal?"
            in_play = False
            score += -1
       
def stand():
    global deck, hand_player, hand_dealer, outcome, in_play, score

    # if the player has busted, remind the player that they have busted.
    if hand_player.get_value() > 21:
        outcome = "You have busted. New deal?"
        pass

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while hand_dealer.get_value() < 17:
            hand_dealer.add_card(deck.deal_card())
    
        # assign a message to outcome, update in_play and score   
        # If the dealer busts, let the player know. Otherwise, compare the value of the player's and dealer's hands.
        if hand_dealer.get_value() > 21:
            outcome = "Dealer has busted. You win! New deal?"
            score += 1
        
        else:
            # If the value of the player's hand is less than or equal to the dealer's hand, the dealer wins. Otherwise the player has won.
            if hand_player.get_value() <= hand_dealer.get_value():
                outcome = "You lose! New deal?"
                score += -1
            else:
                outcome = "You win! New deal?"
                score += 1
        
        in_play = False

        
# draw handler    
def draw(canvas):

    # Draw hands
    # TODO
    hand_dealer.draw(canvas, DEALER_CARD_POSITION)
    hand_player.draw(canvas, PLAYER_CARD_POSITION)

    # if round is in play, cover dealer's first card
    if in_play:
        canvas.draw_image(card_back, 
                      CARD_BACK_CENTER, 
                      CARD_BACK_SIZE, 
                      [DEALER_CARD_POSITION[0] + CARD_BACK_CENTER[0], DEALER_CARD_POSITION[1] + CARD_BACK_CENTER[1]], 
                      CARD_BACK_SIZE)

    # Draw the title of the game, "Blackjack".
    canvas.draw_text("Blackjack", (200, 100), 50, 'Red')

    # Draw dealer and player texts.
    canvas.draw_text("Dealer:", (DEALER_CARD_POSITION[0], DEALER_CARD_POSITION[1] - 10), 20, 'Black')
    canvas.draw_text("Player:", (PLAYER_CARD_POSITION[0], PLAYER_CARD_POSITION[1] - 10), 20, 'Black')

    # Draw message
    canvas.draw_text(outcome, (50, 550), 20, 'Black')

    # Draw score
    canvas.draw_text("Score:" + str(score), (480, 550), 20, 'Black')
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
