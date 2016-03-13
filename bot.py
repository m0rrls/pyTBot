import socket, string, threading
from databaseControl import *
from random import randint
from time import *
from multiprocessing import Pool

class Bot:
	def __init__(self, whbot, inQ, outQ):
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
		self.rouletteOdds = 50
		self.duelOdds = 45
		self.wbot = whbot
		self.inQ = inQ
		self.outQ = outQ

		"""oddsy na przegrana"""


	# Method for sending a message
	def Send_message(self, message):
		self.s.send("PRIVMSG #yarakii :" + message + "\r\n")

	def Send_whisper(self, rec, message):
		self.wbot.Send_whisper(rec, message)

	def getUserPoints(self, user):
		points = self.db.getUserPoints(user)
		return points

	def ruinedChat(self):
		self.Send_message("SUPERLONGMESSAGE NaM SUPERLONGMESSAGE NaM SUPERLONGMESSAGE NaM SUPERLONGMESSAGE NaM SUPERLONGMESSAGE NaM SUPERLONGMESSAGE NaM SUPERLONGMESSAGE NaM SUPERLONGMESSAGE NaM SUPERLONGMESSAGE NaM SUPERLONGMESSAGE NaM SUPERLONGMESSAGE NaM")

	def infosEvery5Minutes(self):
		while(True):
			self.Send_message("g2a.com")
			sleep(300)

	def legend(self):
		self.Send_message("HE DID IT PogChamp //")
		self.Send_message("HE DID IT PogChamp //")
		self.Send_message("HE DID IT PogChamp //")
		self.Send_message("HE DID IT PogChamp //")
		self.Send_message("HE DID IT PogChamp //")
		self.Send_message("HE DID IT PogChamp //")
		self.Send_message("HE DID IT PogChamp //")
		self.Send_message("HE DID IT PogChamp //")
		self.Send_message("HE DID IT PogChamp //")
		self.Send_message("HE DID IT PogChamp //")
		self.Send_message("HE DID IT PogChamp //")
		self.Send_message("HE DID IT PogChamp //")
		self.Send_message("HE DID IT PogChamp //")

	def addMisplay(self):
		self.db.addPointsToUser("misplay", 1)
		self.Send_message("One more? FailFish")

	def checkMisplays(self):
		points = self.getUserPoints("misplay")
		self.Send_message("Current misplay counter: " + str(points))

	def roulette(self, user, points):
		points = int(points)
		userPoints = int(self.getUserPoints(user))
		if userPoints >= points and points>0:
			rand = randint(0,99)
			if rand>self.rouletteOdds:
				self.db.addPointsToUser(user, points)
				return user + " just won " + str(points) + " points FeelsGoodMan"
			else:
				self.db.addPointsToUser(user, points*-1)
				return user + " just lost " + str(points) + " points FeelsBadMan"
		else:
			return user + " You don't have enough points FailFish"

	def printCommands(self):
		message = "Current commands: !points, !roulette <amount>, !duel <username> <amount>, !odds, !userpoints <user>, !chat, !misplay. Have fun! FeelsGoodMan"
		self.Send_message(message)

	def duel(self, player1, player2, amount):
		if int(self.db.getUserPoints(player1)) >= int(amount) and int(self.db.getUserPoints(player2)) >= int(amount):
			rand = randint(0,99)
			if rand<int(self.duelOdds):
				self.db.addPointsToUser(player1, int(amount))
				self.db.addPointsToUser(player2, int(amount)*-1)
				message = str(player1) + " just won duel vs " + str(player2) + " for " + str(amount) + " points! SeemsGood"
				return message
			else:
				self.db.addPointsToUser(player2, int(amount))
				self.db.addPointsToUser(player1, int(amount)*-1)
				message = str(player2) + " just won duel vs " + str(player1) + " for " + str(amount) + " points! SeemsGood"
				return message
		else:
			message = "One of the players dont have enough points for this duel FeelsBadMan"
			return message

#zrobic by sie nie zawiesal na duelu

	def duelWh(self, p1, p2, amount):
		pl1 = p1.lower()
		pl2 = p2.lower()
		if int(self.db.getUserPoints(pl1)) >= int(amount):
			if int(self.db.getUserPoints(pl2)) >= int(amount):
				self.outQ.put([str(pl1), str(pl2), int(amount)])
				dTh = threading.Thread(name=str([pl1, pl2, amount]), target=self.duelWait, args=([pl1, pl2, amount]))
				dTh.daemon = True
				dTh.start()
				return ""
			else:
				message = "Przeciwnik nie ma wystarczajaco pktow"
				self.Send_whisper(pl1, message)
				return ""
		else:
			message = "Masz za malo pkt!"
			self.Send_whisper(pl1, message)
			return ""

	def duelWait(self, pl1, pl2, amount):
		datab = DatabaseControl()
		check = []
		cond = True
		while (cond):
			if(len(check) > 0):
				self.inQ.put(check)
				check = []
			check = self.inQ.get()
			#print check
			if check == [str(pl1), str(pl2), int(amount)]:
				cond = False

		rand = randint(0,99)
		if rand<int(self.duelOdds):
			datab.addPointsToUser(pl1, int(amount))
			datab.addPointsToUser(pl2, int(amount)*-1)
			message = str(pl1) + " just won duel vs " + str(pl2) + " for " + str(amount) + " points! SeemsGood"
		else:
			datab.addPointsToUser(pl2, int(amount))
			datab.addPointsToUser(pl1, int(amount)*-1)
			message = str(pl2) + " just won duel vs " + str(pl1) + " for " + str(amount) + " points! SeemsGood"
		self.Send_message(message)




	def userPoints(self, user):
		tmp = self.getUserPoints(user)
		message = "User " + str(user) + " has " + str(tmp) + " points."
		self.Send_message(message)

	def points(self, user):

		p = self.getUserPoints(user)
		message = "Masz %s pktow Keepo" % str(p)
		#message = username + " points = " + str(points)
		self.Send_whisper(user, message)

	def odds(self):
		currentOdds = 100-self.rouletteOdds
		message = "Current odds to win roulette: " + str(currentOdds) + ". Odds for winning duel if you are calling it is "+str(self.duelOdds)
		self.Send_message(message)

	def mainLoop(self):
		self.db = DatabaseControl()
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
								#points = self.getUserPoints(username)
								#message = ""
								#message = username + " points = " + str(points)
								#self.Send_message(message)
								self.points(username)
							if command[0] == "!roulette":
								self.Send_message(self.roulette(username, command[1]))
							if command[0] == "!chat":
		 						self.ruinedChat()
							if command[0] == "!odds":
		 						self.odds()
							if command[0] == "!duel" and len(command)>2 and command[2].isdigit():
		 						self.Send_message(self.duel(username, command[1], command[2]))
							if command[0] == "!duelwh" and len(command)>2 and command[2].isdigit():
								self.Send_message(self.duelWh(username, command[1], command[2]))
							if command[0] == "!userpoints" and len(command)>1:
								self.userPoints(command[1])
							if command[0] == "!commands":
								self.printCommands()
							if command[0] == "!legend":
								self.legend()
							if command[0] == "!addmisplay" and username == "yarakii":
								self.addMisplay()
							if command[0] == "!misplay":
								self.checkMisplays()
							if command[0] == "!mariusz":
								self.Send_whisper("m0rrls", "Kappa //")
							if command[0] == "!gibemoni" and username == "m0rrls":
								self.db.addPointsToUser(command[1], int(command[2]))
								#self.points(command[1])
						for l in parts:
							if "End of /NAMES list" in l:
								self.MODT = True
