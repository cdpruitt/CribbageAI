from Card import *
from itertools import *

class History():
    def __init__(self, playerToLead):
        self.rounds = [RoundTo31(playerToLead)]

    def isTerminal(self):
        totalCardsPlayed = 0
        for roundTo31 in self.rounds:
            for play in roundTo31.board:
                if(play=="PASS"):
                    break
                else:
                    totalCardsPlayed += 1
    
        if(totalCardsPlayed==8):
            return True
        else:
            return False

    def __repr__(self):
        historyRepr = "Rounds:"
        for roundTo31 in self.rounds:
            historyRepr += " " + str(roundTo31)
        return historyRepr

class RoundTo31():
    def __init__(self, playerToLead):
        self.playerToLead = playerToLead
        self.board = []
    def __repr__(self):
        roundTo31Repr = "Cards played:"
        for card in self.board:
            roundTo31Repr += " " + str(card)
        return roundTo31Repr

# Create a new deck at the start of the game
def createDeck():
    RANKS = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    SUITS = ["spades","hearts","diamonds","clubs"]

    return list(Card(rank, suit) for rank, suit in product(RANKS,
    SUITS))

# Create a new deck at the start of a hand
def createSuitlessDeck():
    RANKS = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    SUITS = ["spades","hearts","diamonds","clubs"]

    deck = list(SuitlessCard(rank) for rank, suit in product(RANKS, SUITS))
    return deck


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

def score(roundTo31, newCard):
    currentBoard = roundTo31.board
    if(roundTo31.playerToLead==0):
        # first player's turn
        total = scoreTheBoard(currentBoard, newCard)

    else:
        # second player's turn
        total = -scoreTheBoard(currentBoard, newCard)

    #print "For " + str(currentBoard) + " " + str(newCard) + ", total = " + str(total)

    return total

def consecutive(runCards):
    sortedCards = runCards[:]
    sortedCards.sort(key=lambda x: x.rank)
    for i, card in enumerate(sortedCards):
        if(card.rank==(sortedCards[0].rank+i)):
            continue
        else:
            return False

    return True

# Compute the play points if newCard is played on the current board
def scoreTheBoard(b, newCard):
    board = b[:]
    board.append(newCard)

    #print board

    score = 0

    # check for 31s and 15s
    boardValue = totalTheBoard(board)
    if (boardValue==15 or boardValue==31):
        #print "31 or 15 for 2"
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
        #print "pairs for 2"
        score += 2

    # check for runs
    runs = 0
    while(len(reversedBoard)>2):
        #print reversedBoard
        if(consecutive(reversedBoard)):
            runs = len(reversedBoard)
            #print "runs for " + str(runs)
            break
        reversedBoard.pop()

    score += runs

    #if(score>0):
    #    print score
    return score

def evaluateTerminalState(cards, roundTo31):
    total = 0
    playerToLead = roundTo31.playerToLead

    if(playerToLead==0):
        total += score(roundTo31,cards[playerToLead][0]) 
    else:
        total -= score(roundTo31,cards[playerToLead][0]) 

    roundTo31.board.append(cards[playerToLead][0])
    roundTo31.playerToLead = 1-playerToLead

    if(len(cards[1-playerToLead])>0):
        if(1-playerToLead==0):
            total -= score(roundTo31,cards[1-playerToLead][0])
        else:
            total += score(roundTo31,cards[1-playerToLead][0])

    return total
