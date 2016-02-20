import socket, string
from databaseControl import *
from random import randint
from time import *
from multiprocessing import Pool

class bot:
    def __init__(self):
        self.plik = open("pasy.txt", "r")
        # Set all the variables necessary to connect to Twitch IRC
        self.HOST = "irc.twitch.tv"
        self.NICK = "botherrington"
        self.PORT = 6667
        self.PASS = self.plik.read()
        self.readbuffer = ""
        self.MODT = False
        # Connecting to Twitch IRC by passing credentials and joining a certain channel
        self.s = socket.socket()
        self.s.connect((self.HOST, self.PORT))
        self.s.send("PASS " + self.PASS + "\r\n")
        self.s.send("NICK " + self.NICK + "\r\n")
        self.s.send("JOIN #yarakii \r\n")
        self.db = databaseControl()
        """oddsy na przegrana"""
        self.rouletteOdds = 50

    # Method for sending a message
    def Send_message(self, message):
        self.s.send("PRIVMSG #yarakii :" + message + "\r\n")

    def Send_whisper(self, message):
    	message = "PRIVMSG #jtv /w erroreq AAA"
    	self.s.send(message)

    def getUserPoints(self, user):
    	points = self.db.getUserPoints(user)
    	return points

    def ruinedChat(self):
    	self.Send_message("AM I RUINING YOUR CHAT EXPERIENCE? EleGiggle")
    	self.Send_whisper("aa")

    def roulette(self, user, points):
    	points = int(points)
    	userPoints = int(self.getUserPoints(user))
    	if userPoints >= points:
    		rand = randint(0,99)
    		if rand>self.rouletteOdds:
    			self.db.addPointsToUser(user, points)
    			return user + " just won " + str(points) + " points FeelsGoodMan"
    		else:
    			self.db.addPointsToUser(user, points*-1)
    			return user + " just lost " + str(points) + " points FeelsBadMan"
    	else:
    		return user + " You don't have enough points FailFish"

    def odds(self):
    	currentOdds = 100-self.rouletteOdds
    	message = "Current odds to win roulette: " + str(currentOdds)
    	self.Send_message(message)

    def mainLoop(self):
        while True:
        	self.readbuffer = self.readbuffer + self.s.recv(1024)
        	temp = string.split(self.readbuffer, "\n")
        	self.readbuffer = temp.pop()
        	for line in temp:
        		print "Wiadomosc z serwera: " + line
        	    # Checks whether the message is PING because its a method of Twitch to check if you're afk
        		if (line[0] == "PING"):
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
        				if self.MODT:
        					print username + ": " + message
        					command = string.split(message, " ")
        	                # You can add all your plain commands here
        					if message == "!points":
        						points = self.getUserPoints(username)
        						message = ""
        						message = username + " points = " + str(points)
        						self.Send_message(message)
        						print "wysylam wiadomosc " + message
        					if command[0] == "!roulette":
        						self.Send_message(self.roulette(username, command[1]))
        					if command[0] == "!chat":
         						self.ruinedChat()
        					if command[0] == "!odds":
         						self.odds()
        				for l in parts:
        					if "End of /NAMES list" in l:
        						self.MODT = True
        	sleep(1 / 20/float(30))
