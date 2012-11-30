"""
simple game of blackjack
"""
#! /usr/bin/python

from random import shuffle
deck = ["AS","2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS",
        "AC","2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC",
        "AH","2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH",
        "AD","2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD"]
hand = []
dealer = []
response = ''
hand_value = 0
dealer_value = 0
over = False

def restart(deck, hand, dealer):
    while len(hand) > 0:
        deck.append(hand.pop())
    while len(dealer) > 0:
        deck.append(dealer.pop())
    shuffle(deck)

def pop_card(hand):
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

def winning(hand, dealer):
    if count_score(hand) > count_score(dealer):
        print "\n\tYou won!\n"
    elif count_score(hand) == count_score(dealer):
        if "JS" in hand:
            print "\n\tYou win!\n"
        elif "JS" in dealer:
            print "\n\tDealer wins!\n"
        elif "JS" not in hand and "JS" not in dealer:
            print "\n\tTie\n"
    else:
        print "\n\tDealer wins!\n"

#shuffle before start
shuffle(deck)

print "Options >>> \n 'deal' \n 'hit' \n 'stand' \n 'new game' \n 'quit'"
while response != 'quit':

    response = raw_input("What would you like to do?  >>> ")

    if 'sh' in response or 'Sh' in response: #shuffle
        shuffle(deck)

    elif 'de' in response or 'De' in response:

        if len(hand) == 0:
            pop_card(hand)
            pop_card(dealer)
            pop_card(hand)
            pop_card(dealer)
            print hand
        else:
            print "You've already dealt, enter 'n' if you want to start a new game"
    elif 'hi' in response or 'Hi' in response:
        pop_card(hand)
        print hand
        hand_value = count_score(hand)
        if hand_value > 21:
            print "You broke!"
            print hand_value
            print "Restarting game..."
            restart(deck, hand, dealer)


    elif 'st' in response or 'St' in response:
        hand_value = count_score(hand)
        print "Score = " + str(hand_value)

	dealer_break = False

        dealer_value = count_score(dealer)
        while dealer_value <= 16:
            pop_card(dealer)
            if count_score(dealer) > 21:
                print "\n\tDealer broke, you win!\n"
                dealer_value = count_score(dealer)
                restart(deck, hand, dealer)
		dealer_break = True                
		break
            dealer_value = count_score(dealer)
        print "Dealer score = " + str(dealer_value)
        
	if not dealer_break:
		winning(hand, dealer)
        	print "Restarting game..."
        	restart(deck, hand, dealer)

    elif 'ne' in response or 'Ne' in response:
        restart(deck, hand, dealer)
        print hand

    elif response == 'quit':
        print "Program ending...\n"
        break

    else:
        print "Command not recognized"

print "Goodbye"
