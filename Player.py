class Player:
    def __init__(self, referee):
        self.hand = []
        self.played = []
        self.score = 0
        self.referee = referee

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

    def requestCard(self):
        publicState = self.referee.getPublicState()
        if(len(self.hand)>0):
            cardToPlay = self.hand.pop(0)
            self.played.append(cardToPlay)
            return cardToPlay
        else:
            return False

    def addPoints(self, points):
        self.score += 2
        if self.score>121:
            self.referee.endGame()

