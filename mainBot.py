import os
from addPointsToActiveUsers import *
from bot import *
import cmd, sys, signal

"""db = databaseControl()
newpid = os.fork()
if newpid == 0:
    dodawanie punktow do uzytkownikow na chacie
    addPoints = addPointsToActiveUsers()
    while True:
    	addPoints.addPoints(db)
    	sleep(60)
    sleep(1)
else:
    sam bot
    bot = bot()
    bot.mainLoop()"""

class customConsole(cmd.Cmd):
    pid=0
    pid2=0
    pid3=0
    db = databaseControl()
    def do_start(self, args):
        newpid = os.fork()
        if newpid == 0:
            self.pid = os.getpid()
            self.bot = bot()
            self.bot.mainLoop()
        else:
            self.pid2 = os.getpid()
            newpid = os.fork()
            if newpid == 0:
                self.pid3 = os.getpid()
                addPoints = addPointsToActiveUsers()
                while True:
                	addPoints.addPoints(self.db)
                	sleep(60)

    def do_end(self, args):
        os.kill(self.pid, signal.SIGKILL)
        os.kill(self.pid2, signal.SIGKILL)
        os.kill(self.pid3, signal.SIGKILL)
if __name__ == '__main__':
    customConsole().cmdloop()
