class Player:
    def __init__(self, referee):
        self.hand = []
        self.played = []
        self.score = 0
        self.referee = referee
        self.canPlay = True

    def __repr__(self):
        self.orderHand()
        return "Hand: %s, Score: %s" % (self.hand, self.score)

    def orderHand(self):
        self.hand = sorted(self.hand)

    def requestCrib(self):
        publicState = self.referee.getPublicState()
        if(len(self.hand)>0):
            return self.hand.pop(0)
        else:
            return False

    # Determines which card to play
    def selectCard(self, publicState):
        # for now, just choose the first possible card in the hand to play
        for card in self.hand:
            if publicState["board total"]+card.value<31:
                return card
        self.canPlay = False
        return False

    def requestCard(self, board):
        publicGameState = self.referee.getPublicState()
        cardToPlay = self.selectCard(publicGameState)
        if(cardToPlay):
            self.hand.remove(cardToPlay)
            self.played.append(cardToPlay)
        return cardToPlay

    def addPoints(self, points):
        self.score += 2
        if self.score>121:
            self.referee.endGame()

