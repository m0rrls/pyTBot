import os
from addPointsToActiveUsers import *
from bot import *
import cmd, sys, signal
from databaseControl import *
import threading

class CustomConsole(cmd.Cmd):
    bot = Bot()
    addPoints = AddPointsToActiveUsers()
    def do_start(self, args):
        botThread = threading.Thread(target=self.bot.mainLoop, name='BotThread')
        botThread.daemon = True
        botThread.start()
        pointsThread = threading.Thread(target=self.addPoints.addPoints,  name='PointsThread')
        pointsThread.daemon = True
        pointsThread.start()


if __name__ == '__main__':
    CustomConsole().cmdloop()
