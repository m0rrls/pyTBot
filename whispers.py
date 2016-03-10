import socket, string
from duelists import *
from time import *

class Whisper:

    def __init__(self):
        self.plik = open("pasy.txt", "r")
		# Set all the variables necessary to connect to Twitch IRC
        self.HOST = "199.9.253.58"
        self.NICK = "botherrington"
        self.PORT = 443
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
        self.s.send("JOIN #yarakii\r\n") #_m0rrls_1457634425342
        self.Send_whisper("yarakii","Inicjuje bota MrDestructoid")
        print "inicjacja"
        sleep(2)
        self.Send_whisper("m0rrls","Inicjuje bota MrDestructoid")

    def Send_whisper(self, rec, message):
        messageS = "PRIVMSG #yarakii :.w " + rec + " " + message + "\r\n"
        #messageS = "m0rrls!m0rrls@m0rrls.tmi.twitch.tv WHISPER botherrington: HeyGuys"
        #messageS = "botherrington!botherrington@botherrington.tmi.twich.tv WHISPER m0rrls: HeyGuys"
        self.s.send(messageS)
        #self.s.send("WHISPER m0rrls: Keepo /\r\n")
        #self.s.send("PRIVMSG #yarakii : Kappa /\r\n")
        print "wyslalem"

    def mainLoop(self):
        while True:
            self.readbuffer = self.readbuffer + self.s.recv(1024)
            temp = string.split(self.readbuffer, "\n")
            self.readbuffer = temp.pop()
            for line in temp:
                print "Wiadomosc z serwera szeptow: " + line
				# Checks whether the message is PING because its a method of Twitch to check if you're afk
                if (line[0] == "PING"):
                    print "PONG"
                    self.s.send("PONG %s\r\n" % line[1])
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
                            if message == "!test":
                                sleep(1)
                                self.Send_whisper(username,"HeyGuys")
                            if message == "!quit" and username == "m0rrls": #moznaby zrobic tutaj ze jezeli user jest w tabeli "admini" i kazdy z nas moze to zrobic
                                self.Send_whisper("m0rrls", "BYE BibleThump 7")
                                self.s.send("PART #yarakii")
                        for l in parts :
                            if "End of /NAMES list" in l:
                                self.MODT = True

obj = Whisper()
obj.mainLoop()
