from Player import Player
from GameActions import *
from random import shuffle
from itertools import *

class Referee:
    def __init__(self):

        # initialize the game state
        self.deck = createDeck()
        self.flipCard
        self.crib = []
        self.players = []

    def __repr__(self):
        return "Players: %s" %(self.players)

    def playGame(self,dealer):
        self.dealHands()
        self.requestCrib()
        self.flipCard()
        self.playHands()
        self.scoreHands()

    def dealHands(self):
        print "Dealing hands to players...\n"
        shuffle(self.deck)
        for player in self.players:
            for i in range(0,hand_size):
                player.hand.append(self.deck.pop(0))
            player.hand = sorted(player.hand)
            print "Player hand: %s" % (player.hand)

    def requestCrib(self):
        print "\nRequesting crib from players..."
        for player in self.players:
            for i in range(crib_size/len(self.players)):
                self.crib.append(player.requestCrib())

        print "Crib is: %s" %(self.crib)
        for player in self.players:
            print "Player hand: %s" % (player.hand)

    def flipCard(self):
        print "\nFlipping card..."
        self.flipCard = self.deck.pop(0)
        print "Flip card: %s" %(self.flipCard)

    def playHands(self):
        print "\nStarting play..."

        # non-dealer plays first
        leader = self.players[1]

        # if anyone has cards left, keep playing
        while True:
            leader = self.playRoundTo31(leader)
            if (not self.players[0].hand) & (not self.players[1].hand):
                break

        for player in self.players:
            player.hand = player.played

        print "Finished play"

    def playRoundTo31(self, leader):
        print "Starting round to 31"
        board = []

        while True:
            card = leader.requestCard()
            if(card):
                board.append(card)
            print board

            if leader==self.players[0]:
                leader = self.players[1]
            else:
                leader = self.players[0]

            if (not self.players[0].hand) & (not self.players[1].hand):
                break

        return leader


    def scoreHands(self):
        print "\nScoring hands..."
        for player in self.players:
            print "%s score is %s" % (player, scoreHand(player.hand, False,
                self.flipCard))
        print "Crib: %s score is %s" % (self.crib, scoreHand(self.crib, True, self.flipCard))

    def getPublicState(self):
        publicGameState = {}
        #publicGameState["cards in play"] = self.cardsInPlay
        #publicGameState["flip card"] = self.flipCard
        #publicGameState["scoreboard"] = self.scoreboard
        return publicGameState


