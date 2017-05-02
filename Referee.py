from Player import Player
from GameActions import *
from random import shuffle
from itertools import *

class Referee:
    def __init__(self):

        # initialize the game state
        self.deck = createDeck()
        self.flipCard
        self.board = []
        self.crib = []
        self.players = []

    def playRound(self,dealer):
        self.dealHands()
        self.requestCrib()
        self.flipCard()
        self.playHands()
        self.scoreHands()

    def endGame(self):
        print "Game over!"
        for player in self.players:
            print "%s score: %s" % (player, self.players[0].score)

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
        if self.flipCard.rank==11:
            # score His Heels for the dealer
            self.players[0].addPoints(2)
        print "Flip card: %s" %(self.flipCard)

    def playHands(self):
        print "\nStarting play..."

        # non-dealer plays first
        leader = self.players[1]

        # if anyone has cards left, keep playing
        while (self.players[0].hand or self.players[1].hand):
            leader = self.playRoundTo31(leader)

        # put cards back in hands
        for player in self.players:
            player.hand = player.played

        print "Finished play"

    def playRoundTo31(self, leader):
        print "Starting round to 31"

        self.players[0].canPlay = True
        self.players[1].canPlay = True

        while (self.players[0].canPlay or self.players[1].canPlay):
            card = leader.requestCard(self.board)
            if(card):
                print card
                self.board.append(card)
                score = scoreTheBoard(self.board)
                leader.addPoints(score)

            # update who should lead
            if leader==self.players[0]:
                leader = self.players[1]
            else:
                leader = self.players[0]

        # score one for last
        if leader==self.players[0]:
            self.players[1].addPoints(1)
        else:
            self.players[0].addPoints(1)
        print "scoring 1 for last"
        self.board = []
        return leader

    def scoreHands(self):
        print "\nScoring hands..."
        for player in self.players:
            print "%s score is %s" % (player, scoreHand(player.hand, False,
                self.flipCard))
        print "Crib: %s score is %s" % (self.crib, scoreHand(self.crib, True, self.flipCard))

    def getPublicState(self):
        publicGameState = {}
        publicGameState["cards in play"] = self.board
        publicGameState["board total"] = totalTheBoard(self.board)
        publicGameState["flip card"] = self.flipCard
        return publicGameState

    def __repr__(self):
        return "Players: %s" %(self.players)
