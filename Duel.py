from databaseControl import *
from random import randint

class databaseControl:
    def __init__(self, odds):
        """odds oznacza P(gracz wyzywajacy wygrywa)"""
        self.odds = int(odds)
        self.db = DatabaseControl()

    def duelPlayers(self, player1, player2, amount):
        if int(self.db.getUserPoints(player1)) >= int(amount) and int(self.db.getUserPoints(player2)) >= int(amount):
            rand = randint(0,99)
            if rand<int(self.odds):
                self.db.addPointsToUser(player1, amount)
                self.db.addPointsToUser(player2, int(amount)*-1)
                message = str(player1) + " just won duel vs " + str(player2) + " for " + str(amount) + " points! SeemsGood"
                return message
            else:
                self.db.addPointsToUser(player2, amount)
                self.db.addPointsToUser(player1, int(amount)*-1)
                message = str(player2) + " just won duel vs " + str(player1) + " for " + str(amount) + " points! SeemsGood"
                return message
        else:
            message = "One of the players dont have enough points for this duel FeelsBadMan"
            return message
