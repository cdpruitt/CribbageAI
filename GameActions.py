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

    # check for 15s
    for i in range(1,len(hand)+1):
        for subHand in combinations(hand,i):
            sum = 0
            for card in subHand:
                sum += card.value
            if sum==15:
                score += 2

    # check for pairs
    for cardPair in combinations(hand,2):
        if cardPair[0].rank==cardPair[1].rank:
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

# Count up the total points showing on the board
def totalTheBoard(board):
    boardValue = 0
    for card in board:
        boardValue += card.value
    return boardValue

# Compute the play points of the most recently played card
def scoreTheBoard(board):
    score = 0
    print ""

    # check for 31s and 15s
    boardValue = totalTheBoard(board)
    if (boardValue==15 or boardValue==31):
        print "31 or 15 for 2"
        score += 2

    reversedBoard = board[::-1]

    # check for pairs
    pairCards = []
    for card in reversedBoard:
        if reversedBoard[0].rank==card.rank:
            pairCards.append(card)
        else:
            break

    for x in combinations(pairCards,2):
        print "pairs for 2"
        score += 2

    # check for runs
    runs = 0
    for i, card in enumerate(board):
        if (card.rank-board[0].rank)==i:
            runs += 1
        else:
            break
    if runs>3:
        score += runs

    print board
    print score
    return score
