from Referee import Referee
from Player import Player

def main():
    referee = Referee()
    players = [Player(referee), Player(referee)]

    referee.players = players

    # play a game
    referee.playRound(players[0])

main()
