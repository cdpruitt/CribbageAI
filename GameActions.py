from Card import Card
from itertools import *

# Define gameplay constants
deck_size = 52
hand_size = 6
crib_size = 4

# Create a new deck at the start of a hand
def createDeck():
    SUITS = ["spades","hearts","diamonds","clubs"]
    RANKS = [1,2,3,4,5,6,7,8,9,10,11,12,13]

    return list(Card(rank, suit) for rank, suit in product(RANKS,
    SUITS))

# Score a given hand, provided the identity of the flip card and whether the
# hand is a crib or not
def scoreHand(hand,isCrib,flipCard):

    score = 0

    # check for His Nobs
    for card in hand:
        if (card.rank=="11")&(card.suit==flipCard.suit):
            score += 1

    # check for flush
    if all(card.suit==flipCard.suit for card in hand):
        score += 5
    elif all(card.suit==hand[0].suit for card in hand):
        score += 4

    hand.append(flipCard)
    hand = sorted(hand)

    # check for pairs
    for cardPair in combinations(hand,2):
        if cardPair[0].rank==cardPair[1].rank:
            score += 2

    # check for 15s
    for i in range(1,len(hand)+1):
        for subHand in combinations(hand,i):
            sum = 0
            for card in subHand:
                sum += card.value
            if sum==15:
                score += 2

    # check for runs
    foundRuns = False
    for i in range(len(hand),2,-1): 
        if foundRuns == False:
            for subHand in combinations(hand,i):
                it = (card.rank for card in subHand)
                first = next(it)
                if all(a==b for a, b in enumerate(it, first+1)):
                    score += i
                    foundRuns = True

    return score

