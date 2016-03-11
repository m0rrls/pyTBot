import os
from addPointsToActiveUsers import *
from bot import *
import cmd, sys, signal
from databaseControl import *
from whispers import *
import threading

class CustomConsole(cmd.Cmd):

    whispers = Whisper()
    bot = Bot(whispers)
    addPoints = AddPointsToActiveUsers()


    def do_start(self, args):

        botThread = threading.Thread(target=self.bot.mainLoop, name='BotThread')
        botThread.daemon = True
        botThread.start()
        pointsThread = threading.Thread(target=self.addPoints.addPoints,  name='PointsThread')
        pointsThread.daemon = True
        pointsThread.start()
        linksThread = threading.Thread(target=self.bot.infosEvery5Minutes, name='LinksThread')
        linksThread.daemon = True
        linksThread.start()
        whisperThread = threading.Thread(target=self.whispers.mainLoop, name='WhisperThread')
        whisperThread.daemon = True
        whisperThread.start()

if __name__ == '__main__':
    CustomConsole().cmdloop()
