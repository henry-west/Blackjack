#! /usr/bin/python
"""
Description: A simple game of blackjack
Author: Henry West
"""
from random import shuffle
deck = ["AS","2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS",
        "AC","2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC",
        "AH","2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH",
        "AD","2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD"]
hand = []
dealer = []
garbage_pile = []
response = ''
hand_value = 0
dealer_value = 0
over = False
player_bank = 0
initial_bank = 0
bet_value = 0
winning = 0
def restart(deck, hand, dealer):
    while len(hand) > 0:
        deck.append(hand.pop())
    while len(dealer) > 0:
        deck.append(dealer.pop())
    shuffle(deck)
# moves cards in hand to garbage_pile, if not enough cards, moves garbage_pile to deck
def setup_next_turn(deck, hand, dealer, garbage_pile):
    while len(hand) > 0:
        garbage_pile.append(hand.pop())
    while len(dealer) > 0:
        garbage_pile.append(dealer.pop())
    if len(deck) <= 8:
        while len(garbage_pile) > 0:
            deck.append(garbage_pile.pop())
        shuffle(deck)
def set_bet_value(bet_value, player_bank):
    while True:
        try:
            bet_value = int(raw_input("Enter a bet >>> "))
            break
        except ValueError:
            print "Invalid bet, try again."
    while player_bank < bet_value:
        print "You cannot bet that much, enter an amount less than or equal to >>> ", player_bank
        while True:
            try:
                bet_value = int(raw_input("Enter a bet >>> "))
                break
            except ValueError:
                print "Invalid bet, try again."
    return bet_value
def determine_bet_result(bet_value, player_bank, winning):
    if winning == 1:
        return (player_bank + bet_value)
    elif winning == 0:
        return player_bank - bet_value
        if player_bank <= 0:
            print "Bankrupt >>> Game Over"
            return 0
    else:
        return player_bank
def deal_card(hand):
    hand.append(deck.pop())
def count_score(hand):
    score = 0
    aces = 0
    for x in range(0,len(hand)):
        if hand[x][0] == 'J' or hand[x][0] == 'Q' or hand[x][0] == 'K':
            score += 10
        elif hand[x][0] == 'A':
            aces += 1
        else:
            if len(hand[x]) == 2:
                score += int(hand[x][0])
            elif len(hand[x]) == 3:
                score += int(hand[x][:2])
    for x in range(aces):
        if score >= 11:
            score += 1
        else:
            score += 11
    return score
def determine_winner(hand, dealer):
    if count_score(hand) > count_score(dealer):
        winning = 1
    elif count_score(hand) == count_score(dealer) and count_score(hand) != 21:
        winning = 2
    elif count_score(hand) == 21 and count_score(dealer) == 21:
        if "JS" in hand:
            winning = 1
        elif "JS" in dealer:
            winning = 0
        elif "JS" not in hand and "JS" not in dealer:
            winning = 2
    else:
        winning = 0
    return winning
# prints the result of the current hand
def print_result(winning):
    if winning == 0:
        print "\nDealer wins\n"
    elif winning == 1:
        print "\nYou won!\n"
    elif winning == 2:
        print "\nTie\n"
#Prints the menu
def print_help():
    print "Options >>> \n'deal' to deal \n'hit' for another card \n'stand' to keep your hand and count the score \n'new game' to end the current hand and start a new game \n'bet' to place a bet on the current hand \n'?' for help\n'quit' to quit"
"""
def write_score_to_file(initial_bank, player_bank):
    if player_bank/initial_bank >= 1:
        print "Saving scores to file..."
    score_file.write("\nStart >>> " + str(initial_bank) + "; Final >>> " + str(player_bank) + "; Ratio >>> " + str(player_bank/initial_bank))
def print_scores():
    print score_file.read()
"""
print "\n\tBlackjack\n"
#prompt for starting value for bank
while (player_bank % 500) != 0 or player_bank == 0:
    player_bank = int(raw_input("How much would you like to start with in the bank? (multiples of 500) >>> "))
    initial_bank = player_bank
#shuffle before start
shuffle(deck)
print_help()

while response != 'quit':
    if player_bank != 0:
        response = raw_input("What would you like to do?  >>> ")
    else:
        response = "quit"
    winning = 0
#developer functions
    if response == 'shuffle': #shuffle
        shuffle(deck)
    elif response == "winning":
        print determine_winner(hand, dealer)
    elif response == "print":
        print 'Deck >>> ' , deck, '\nGarbage Pile >>> ' , garbage_pile , '\nHand >>> ' , hand , '\nDealer >>> ' , dealer
    elif response == "printscore":
        print "Printing scores file...\n"
        print_scores()
#deals cards to both user and 'dealer'
    elif response == 'deal':
        if len(hand) == 0:
            deal_card(hand)
            deal_card(dealer)
            deal_card(hand)
            deal_card(dealer)
            print hand
        else:
            print "You've already dealt, enter 'new' to start a new game, 'hit' to add another card to your hand, or 'stand' to hold your current hand."
#adds new card to user hand
    elif response == 'hit':
        if len(hand) != 0:
            deal_card(hand)
            print hand
            hand_value = count_score(hand)
            if hand_value > 21:
                print "You broke."
                print hand_value
                winning = 0
                if bet_value > 0:
                    player_bank = determine_bet_result(bet_value, player_bank, winning)
                    print "You have >>>", player_bank
                    bet_value = 0
                print "\nNext turn...\n"
                setup_next_turn(deck, hand, dealer, garbage_pile)
                print "Deck >>> " , len(deck)
        else:
            print "You haven't dealt yet."
#stand on hand, transfers cards to garbage_pile
    elif response == 'stand':
        hand_value = count_score(hand)
        print "Score = %s" % (str(hand_value))
        dealer_break = False
        dealer_value = count_score(dealer)
        while dealer_value <= 16:
            deal_card(dealer)
            if count_score(dealer) > 21:
                print "\nDealer broke\n"
                dealer_break = True
                dealer_value = count_score(dealer)
                winning = 1
                if bet_value > 0:
                    player_bank = determine_bet_result(bet_value, player_bank, winning)
                    print "You have >>>", player_bank
                    bet_value = 0
                print "\nNext turn...\n"
                setup_next_turn(deck, hand, dealer, garbage_pile)
                print "Deck >>> " , len(deck)
                break
            dealer_value = count_score(dealer)
        print "Dealer score >>> ", str(dealer_value)
        if not dealer_break:
            winning = determine_winner(hand, dealer)
            if bet_value > 0:
                player_bank = determine_bet_result(bet_value, player_bank, winning)
                print "You have >>>", player_bank
                bet_value = 0
            print_result(winning)
            print "\nNext turn...\n"
            setup_next_turn(deck, hand, dealer, garbage_pile)
            print "Deck >>> " , len(deck)

#moves all cards to deck and restarts
    elif 'new' in response or 'New' in response:
        restart(deck, hand, dealer)
        print "Deck >>> " , len(deck)

#sets bet
    elif response == 'bet':
        if len(hand) != 0:
            print "You already dealt. Wait until the next hand to place a bet."
        else:
            bet_value = set_bet_value(bet_value, player_bank)
            print "You have >>>", player_bank
            print "You bet >>>" , bet_value

#help menu
    elif response == '?':
        print_help()

#quit signal
    elif response == 'quit':
        raw_input("Program ending, press enter to continue.")
        #write_score_to_file(initial_bank, player_bank)
        break
    else:
        print "Command not recognized, enter '?' for a list of options."

score_file.close()
