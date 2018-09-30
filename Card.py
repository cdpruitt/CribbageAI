class SuitlessCard:
    def __init__(self, rank):
        self.rank = rank
        if rank<10:
            self.value = rank
        else:
            self.value = 10
    def __repr__(self):
        letters = {1:'A', 11:'J', 12:'Q', 13:'K'}
        letter = letters.get(self.rank, str(self.rank))
        return "%s" %(letter)

class Card(SuitlessCard):
    def __init__(self, rank, suit):
        SuitlessCard.__init__(self, rank)
        self.suit = suit

    def __repr__(self):
        letters = {1:'A', 11:'J', 12:'Q', 13:'K'}
        letter = letters.get(self.rank, str(self.rank))

        suits = {}
        suits["spades"] = u'\u2664'
        suits["hearts"] = u'\u2665'
        suits["diamonds"] = u'\u2666'
        suits["clubs"] = u'\u2667'

        suit = suits.get(self.suit, self.suit)
        suit = suit.encode('utf-8')

        return "%s%s" %(letter, suit)

