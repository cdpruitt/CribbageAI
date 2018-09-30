import copy
from random import shuffle
from GameActions import *
from Card import *
import time

NodeDict = {}

class InfoSet:
    def __init__(self, c, h):
        self.hand = sorted(c, key=lambda x: x.rank)
        self.history = h
    #def concise(self):
    #    hand = "%s %s" %(self.hand[0].rank, self.hand[1].rank)

    def __repr__(self):
        hand = "%s %s" %(self.hand[0].rank, self.hand[1].rank)
        history = ""
        for card in self.history.rounds[-1].board:
            history += " %s" %(card.rank)
        return hand + history

class Node:
    def __init__(self, infoSet):
        self.infoSet = infoSet
        self.regretSum = {}
        self.strategy = {}
        self.strategySum = {}

    def __repr__(self):
        return "Info set: " + str(self.infoSet) + ". Average strategy profile" + str(self.getAverageStrategy())

    def getStrategy(self, hand, realizationWeight):
        normalizingSum = 0.;
        for card in hand:
            if(card not in self.regretSum):
                self.regretSum[card] = 0

            if(card not in self.strategy):
                self.strategy[card] = 0

            if(self.regretSum[card]>0):
                self.strategy[card] = self.regretSum[card]
            else:
                self.strategy[card] = 0
            normalizingSum += self.strategy[card]

        for card in hand:
            if(normalizingSum > 0):
                self.strategy[card] /= float(normalizingSum)
            else:
                self.strategy[card] = 1/float(len(hand))

            if(card not in self.strategySum):
                self.strategySum[card] = 0

            self.strategySum[card] += realizationWeight * self.strategy[card]

        return self.strategy

    def getAverageStrategy(self):
        avgStrategy = []
        normalizingSum = 0
        for card in self.infoSet.hand:
            normalizingSum += self.strategySum[card]

        for card in self.infoSet.hand:
            if(normalizingSum > 0):
                avgStrategy.append(self.strategySum[card]/float(normalizingSum))
            else:
                avgStrategy.append(1.0/float(len(self.infoSet.hand)))

        return avgStrategy

def cfr(cards, history, realizationWeights):

    # given the public board, determine whose turn it is to play
    player = history.rounds[-1].playerToLead
    opponent = 1-player

    if(len(cards[0])<2 and len(cards[1])<2):
        # no more decision points - play the round out and return utility
        return evaluateTerminalState(cards, history.rounds[-1])
        
    infoSet = InfoSet(cards[player], history)

    if str(infoSet) not in NodeDict:
        NodeDict[str(infoSet)] = Node(infoSet)

    node = NodeDict[str(infoSet)]

    strategy = node.getStrategy(cards[player], realizationWeights[player])

    util = {}
    nodeUtil = 0

    for card in cards[player]:
        nextHand = cards[player][:]
        nextHand.remove(card)

        nextHistory = copy.deepcopy(history)
        nextHistory.rounds[-1].board.append(card)
        nextHistory.rounds[-1].playerToLead = opponent

        if(player==0):
            nextCards = [nextHand,cards[1]]
        else:
            nextCards = [cards[0],nextHand]

        if(player==0):
            util[card] = -cfr(nextCards, nextHistory,\
                    [realizationWeights[0]*strategy[card], realizationWeights[1]])
        else:
            util[card] = -cfr(nextCards, nextHistory,\
                    [realizationWeights[0], realizationWeights[1]*strategy[card]])

        #print "card util from cfr = " + str(util[card])

        if(len(history.rounds[-1].board)>0):
            util[card] -= score(history.rounds[-1], card)

        nodeUtil += strategy[card]*util[card]

    for card in cards[player]:
        regret = util[card] - nodeUtil
        node.regretSum[card] += regret*realizationWeights[opponent]

    return nodeUtil

def train(iterations):
    #deck = createDeck()
    deck = createSuitlessDeck()
    #cards = [[SuitlessCard(5),SuitlessCard(10)],[SuitlessCard(9),SuitlessCard(11)]]
    utility = 0
    for i in range(iterations):
        shuffle(deck)
        cards = [[deck[0], deck[1]], [deck[2], deck[3]]]
        utility += cfr(cards, History(0), [1, 1])
    print("Average game value: " + str(float(utility)/iterations))

    results = []
    for key, value in NodeDict.items():
        if(len(value.infoSet.history.rounds[-1].board)==0):
            results.append([key, value.getAverageStrategy()])

    results.sort()

    f = open('results.txt', 'w')

    for result in results:
        f.write('%s %f %f\n' %(result[0], result[1][0], result[1][1]))

def main():
    iterations = 10000
    startTime = int(round(time.time()))
    train(iterations)
    endTime = int(round(time.time()))

    print "Total training time: %f" %(endTime-startTime)

main()
