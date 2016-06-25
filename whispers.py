import socket, string, urllib2, json, random
from duelists import *
from time import *
from databaseControl import CustomDbCtrl
import threading, errno
from Queue import Queue, Empty
from sgist import *
from quiz import *

class Whisper:

    def __init__(self, inQ, outQ):
        self.plik = open("pasy.txt", "r")
        self.inQ = inQ
        self.outQ = outQ
        #self.subsDb = CustomDbCtrl("subs.db")

        # Get random server address to connect to
        url = "http://tmi.twitch.tv/servers?cluster=group"
        response = urllib2.urlopen(url)
        jdata = json.load(response)
        chosenAdr = random.randrange(len(jdata['servers']))
        adr = string.split(jdata['servers'][chosenAdr],":")

		# Set all the variables necessary to connect to Twitch IRC
        print "connectin to %s %s" % (adr[0], adr[1])
        self.HOST = adr[0]
        self.NICK = "botherrington"
        self.PORT = int(adr[1], base=10)
        self.PASS = self.plik.read()
        self.readbuffer = ""
        self.MODT = False
		# Connecting to Twitch IRC by passing credentials and joining a certain channel
        self.s = socket.socket()
        self.s.connect((self.HOST, self.PORT))
        self.s.send("PASS " + self.PASS + "\r\n")
        self.s.send("NICK " + self.NICK + "\r\n")
        #self.s.send("USER botherrington empty bla :botherrington\r\n")
        self.s.send("CAP REQ :twitch.tv/commands\r\n")
        #self.s.send("CAP REQ :twitch.tv/tags\r\n")
        #self.s.send("CAP REQ :twitch.tv/membership\r\n")
        sleep(1)
        self.s.send("JOIN #yarakii\r\n")
        print "inicjacja"
        sleep(1)
        self.Send_whisper("m0rrls","Inicjuje bota MrDestructoid")
        sleep(1)
        #self.Send_whisper("yarakii","Inicjuje bota MrDestructoid")
        #self.s.settimeout(3)
        self.cmd = ""
        self.emote = ""
        self.emotePoints = 0

    def Send_whisper(self, rec, message):
        messageS = "PRIVMSG #yarakii :.w " + rec + " " + message + "\r\n"
        self.s.send(messageS)

    def multiWhisper(self, tab, mess):
        for x in tab:
            self.Send_whisper(x, mess)
            sleep(5)

    def getSubs(self):
        self.subsDb = CustomDbCtrl("subs.db")
        return self.subsDb.getUsers("subs")

    def getInfo(self):
        self.subsDb = CustomDbCtrl("subs.db")
        return self.subsDb.getSubInfo("subs")

	def emoteQuiz(self, amount):
		emote = emotes.rand()
		print emote
		self.emote = emote
		self.emotePoints = int(amount) + 1
		self.cmd = "Rozpoczynam EmoteQuiz! Do wygrania nawet " + amount + " pkt"


    def mainLoop(self):
        while True:
            try:
                challenge = self.inQ.get(False)
            except Empty:
                challenge = []
            if len(challenge) == 3:
                sleep(1)
                #print "odebralem"
                #print challenge
                mess = "Gracz %s wyzywa Cie na pojedynek o %s pkt! PogChamp \t\t\tWpisz TUTAJ !accept by zaakceptowac lub !deny by odrzucic wyzwanie" % (str(challenge[0]), str(challenge[2]))
                self.Send_whisper(str(challenge[1]), mess)
                #self.Send_whisper("hisechi", "TOP KEK BRO")
            self.s.settimeout(3)
            try:
                self.readbuffer = self.readbuffer + self.s.recv(1024)
                temp = string.split(self.readbuffer, "\n")
            except socket.timeout:
                    continue
            self.s.settimeout(None)
            self.readbuffer = temp.pop()
            for line in temp:
                #print "Wiadomosc z serwera szeptow: " + line
				# Checks whether the message is PING because its a method of Twitch to check if you're afk
                if ("PING" in line):
                    if (line == "PING :tmi.twitch.tv\r\n"):
                        print "PONG"
                    self.s.send("PONG :tmi.twitch.tv\r\n")
                else:
					# Splits the given string so we can work with it better
                    parts = string.split(line, ":")
                    if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                        try:
							# Sets the message variable to the actual message sent
                            message = parts[2][:len(parts[2]) - 1]
                        except:
                            message = ""
						# Sets the username variable to the actual username
                        usernamesplit = string.split(parts[1], "!")
                        username = usernamesplit[0]

						# Only works after twitch is done announcing stuff (MODT = Message of the day)
                        if self.MODT or True:
                            print username + ": " + message
                            command = string.split(message, " ")
							# You can add all your plain commands here
                            if message == "!accept":
                                self.outQ.put(username)

                            if message == "!deny":
                                temp = "___" + username
                                self.outQ.put(temp)

                            if message == "!test":
                                sleep(1)
                                self.Send_whisper(username,"HeyGuys")
                            if message == "!quit" and username == "m0rrls": #moznaby zrobic tutaj ze jezeli user jest w tabeli "admini" i kazdy z nas moze to zrobic
                                self.Send_whisper("m0rrls", "BYE BibleThump 7")
                                self.s.send("PART #yarakii")
                            if command[0] == "!emote" and username == "m0rrls":
                                self.Send_whisper(command[1], command[2])

                            if command[0] == "!live" and username in ("yarakii", "m0rrls"):
                                zbior = self.getSubs()
                                if message == command[0]:
                                    mess = "Yarakii rozpoczyna stream PogChamp Zapraszamy na https://twitch.tv/yarakii"
                                else:
                                    mess = " ".join(command[1:])

                                liveWhisperThread = threading.Thread(target=self.multiWhisper, args=(zbior, mess), name='LiveWhisperThread')
                                liveWhisperThread.daemon = True
                                liveWhisperThread.start()

                            if command[0] == "!subs":
                                zbior = "login | czas subowania (w dniach)\n----------------------------------\n"
                                zbior = zbior + resToStr(self.getInfo())
                                link = SGist().postAnon("yarakii subs","list.txt",zbior)
                                self.Send_whisper(username, "Link do listy subow: "+link)

                            if command[0] == "!cmd" and username == "m0rrls":
                                self.cmd = " ".join(command[1:])
                                #print "CMD: " + self.cmd

                            if command[0] == "!eq" and username == "m0rrls":
								#self.emoteQuiz(command[1])
                                emote = emotes.rand()
                                print str(emote)
                                self.emote = emote
                                self.emotePoints = int(command[1]) + 1
                                self.cmd = "Rozpoczynam EmoteQuiz! Do wygrania nawet " + command[1] + " pkt"

                        for l in parts :
                            if "End of /NAMES list" in l:
                                self.MODT = True
