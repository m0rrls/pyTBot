import os
from addPointsToActiveUsers import *
from bot import *
import cmd, sys, signal
from databaseControl import *
from whispers import *
from duelMan import *
import threading

fromChall = Queue()
toTargets = Queue()
response = Queue()
allow = Queue()

class CustomConsole(cmd.Cmd):




    whispers = Whisper(toTargets, response)
    bot = Bot(whispers, allow, fromChall)
    addPoints = AddPointsToActiveUsers()
    duelMan = DuelMan(5, whispers, fromChall, toTargets, allow, response)


    def do_start(self, args):

        botThread = threading.Thread(target=self.bot.mainLoop, name='BotThread')
        botThread.daemon = True
        botThread.start()

        pointsThread = threading.Thread(target=self.addPoints.addPoints,  name='PointsThread')
        pointsThread.daemon = True
        pointsThread.start()

        #linksThread = threading.Thread(target=self.bot.infosEvery5Minutes, name='LinksThread')
        #linksThread.daemon = True
        #linksThread.start()

        whisperThread = threading.Thread(target=self.whispers.mainLoop, name='WhisperThread')
        whisperThread.daemon = True
        whisperThread.start()

        duelsThread = threading.Thread(target=self.duelMan.mainLoop, name="DuelsThread")
        duelsThread.daemon = True
        duelsThread.start()


if __name__ == '__main__':
    CustomConsole().cmdloop()
