import os
from addPointsToActiveUsers import *
from bot import *
import cmd, sys, signal
from databaseControl import *

class CustomConsole(cmd.Cmd):
    pid=0
    pid2=0
    pid3=0
    db = DatabaseControl()
    def do_start(self, args):
        newpid = os.fork()
        if newpid == 0:
            self.pid = os.getpid()
            self.bot = Bot(self.db)
            self.bot.mainLoop()
        else:
            self.pid2 = os.getpid()
            newpid = os.fork()
            if newpid == 0:
                self.pid3 = os.getpid()
                addPoints = AddPointsToActiveUsers()
                while True:
                	addPoints.addPoints(self.db)
                	sleep(60)

    def do_end(self, args):
        os.kill(self.pid, signal.SIGKILL)
        os.kill(self.pid2, signal.SIGKILL)
        os.kill(self.pid3, signal.SIGKILL)
if __name__ == '__main__':
    CustomConsole().cmdloop()
