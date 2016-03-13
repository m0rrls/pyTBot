from duelists import *
from bot import *
from whispers import *
import threading, random
from Queue import Queue, Empty

class DuelMan:

    #class operates on table of duels, which are added by queues of bot and whbot
    #challenger is added by bot, and target by whbot after !accept
    def __init__(self, time, whbot,challQ, targQ, infoQ, respQ):
        self.list = Duelists()
        self.db = DatabaseControl()
        self.refTime = int(time) #time after kickout of queue
        self.chall = challQ #queue fro adding duels
        self.targ = targQ #queue to ask for acceptance
        self.info = infoQ #queue to allow bot run duel
        self.resp = respQ #queue to get acceptance from target
        self.whbot = whbot

    #procedure adds duel to the table and sends info to whisperbot to get acceptance
    def addDuel(self,p1, p2, points):
        if self.list.getSize() > 4:
            if p1 in self.list.getChallengers():
                mess = "Nie mozesz wyzwac tej osoby, bo czekasz juz na odpowiedz innej"
                self.whbot.Send_whisper(p1, mess)

            elif p1 in self.list.getTargets():
                mess = "Musisz najpierw odpowiedziec na poprzednie wyzwanie FailFish"
                self.whbot.Send_whisper(p1, mess)

            elif p2 in self.list.getTargets():
                mess = "Nie mozesz wyzwac tej osoby, bo ktos zrobil to przed Toba"
                self.whbot.Send_whisper(p1, mess)

            elif p2 in self.list.getChallengers():
                mess = "Wyzwana osoba czeka na odpowiedz inne osoby"
                self.whbot.Send_whisper(p1, mess)

            else:
                self.list.addNewRow(p1,p2,points)
                self.targ.put([p1,p2,points])

        else:
            self.list.addNewRow(p1,p2,points)
            self.targ.put([p1,p2,points])

    def exeDuel(self,target):
        nr = self.list.findRow(str(target))
        print "zaakceptowal " + str(target)
        if nr > 0:
            print "usuwam " + str(self.list.getRecords()[nr])
            pl1 = self.list.getRecords()[nr][0]
            amount = self.list.getRecords()[nr][3]
            self.info.put([str(pl1), str(target), int(amount)])
            self.list.delRow(nr)
        #self.list.delUserRec(str(pl1), str(target))

    def mainLoop(self):
        while True:
            try:
                challenge = self.chall.get(False)
            except Empty:
                challenge = []
            if len(challenge) == 3:
                print "challenge"
                print challenge
                self.addDuel(challenge[0], challenge[1], challenge[2])
                sleep(1)
                #print self.list.getRecords()
            try:
                acceptance = self.resp.get(False)
            except:
                acceptance = ""
            if len(acceptance) > 0 and acceptance in self.list.getTargets():
                #print "\t\t\taccept"
                self.exeDuel(acceptance)
                sleep(1)
                #print self.list.getRecords()
            self.list.refresh(self.refTime)
            sleep(1)
            #print self.list.getRecords()

"""
ch = Queue()
tar = Queue()
response = Queue()
info = Queue()

obj = DuelMan(1, ch, tar, info, response)
botThread = threading.Thread(target=obj.mainLoop, name='DuelMan')
botThread.daemon = True
botThread.start()

sleep(1)
tab = ["Kappa", "Keepo", 123]
ch.put(tab)
ch.put(["4Head", "WutFace", 69])
ch.put(["forsenPuke", "forsenWut", 120])
sleep(10)
response.put("Keepo")
sleep(5)
response.put("forsenWut")
sleep(70)
"""
