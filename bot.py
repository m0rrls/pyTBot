import socket, string, threading, requests, json, urlparse
from databaseControl import *
from random import randint
from time import *
from multiprocessing import Pool
from quiz import *

class Bot:
	def __init__(self, whbot, inQ, outQ):
		self.passFile = open("pasy.txt", "r")
		self.ytAPIFile = open('ytKey.txt', 'r')
		self.soundNames = open('soundNames', 'r')
		# Set all the variables necessary to connect to Twitch IRC
		self.HOST = "irc.twitch.tv"
		self.NICK = "botherrington"
		self.PORT = 6667
		self.PASS = self.passFile.read()
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
		self.emoteTries = 0
		self.youtubeAPIkey = self.ytAPIFile.read()
		self.soundBoard = self.soundNames.readlines();
		"""oddsy na przegrana"""


	# Method for sending a message
	def Send_message(self, message):
		try:
			self.s.send("PRIVMSG #yarakii :" + message + "\r\n")
		except UnicodeEncodeError:
			message = ''.join([i if ord(i) < 128 else ' ' for i in message])
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
			self.Send_message("Mozesz dodac utwor do playlisty z yt poprzez !songrequest \"link\"")
			#self.Send_message("https://dubtrack.fm/join/yaraki")
			sleep(180)
			self.Send_message("Jezeli chcesz byc powiadamiany o rozpoczeciu streama \"zasubuj\" wpisujac !sub Kappa")
			sleep(180)


	def emoteWin(self, user):
		self.Send_message(user + " trafil emotke -> "+ self.wbot.emote +" i otrzymuje " + str(self.wbot.emotePoints) + " pkt PogChamp")
		self.wbot.emote = ""
		self.db.addPointsToUser(user, self.wbot.emotePoints)
		self.emoteTries = 0
		self.wbot.emotePoints = 0

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
		userPoints = int(self.getUserPoints(user))
		if points == "all":
			points = userPoints
		else:
			try:
				points = int(points)
			except ValueError:
				points = 0
		if userPoints >= points and points>0:
			rand = randint(0,99)
			if rand>self.rouletteOdds:
				self.db.addPointsToUser(user, points)
				return user + " just won " + str(points) + " points FeelsGoodMan"
			else:
				self.db.addPointsToUser(user, points*-1)
				return user + " just lost " + str(points) + " points FeelsBadMan"
		elif points != 0:
			return user + " You don't have enough points FailFish"
		elif points == 0:
			return "Are u retarded, " + user + " ? MingLee"

	def printCommands(self):
		message = "Current commands: !points, !roulette <amount>, !duel <username> <amount>, !odds, !userpoints <user>, !chat, !misplay, !sub/!unsub Have fun! FeelsGoodMan"
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


	def addToSubList(self, user):
		message = "Dodano Cie do listy \"subow\" Kappa Teraz gdy rozpoczenie sie stream otrzymasz powiadomienie na whisperze! W kazdej chwili mozesz sie wypisac przez \"!unsub\""
		res = self.subsDb.addUser(user, "subs")
		if res == 0:
			self.Send_whisper(user, message)

	def delFromSubList(self, user):
		message = "Uzytkownik " + user + " zostal usuniety z bazy subskrybentow FeelsBadMan"
		self.subsDb.delUser(user, "subs")
		self.Send_whisper(user, message)

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

	def addSongToList(self, url, username):
		url_data = urlparse.urlparse(url)
		query = urlparse.parse_qs(url_data.query)
		try:
			vid_id = str(query['v'][0])
			print "adding song id: " + vid_id
			title = self.getVidDesc(vid_id)['title']
			if title != '':
				json_data = {"YTId":vid_id,'title':title,'requestor':username}
				cafile = 'cacert.pem' # http://curl.haxx.se/ca/cacert.pem
				r = requests.post("http://yarakitwitch.azurewebsites.net/Videos/Create", data = json_data, verify = cafile)
				if (r.status_code == 200):
					self.Send_message(username + " dodal utwor \""+title+"\" do playlisty")
			else:
				self.Send_message("nice link, bro BrokeBack")
		except KeyError:
			self.Send_message("NOT VALID VIDEO MrDestructoid")

	def getVidDesc(self,vid_id):
	    url = 'https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id='+vid_id+'&key='+self.youtubeAPIkey
	    r = requests.get(url)
	    data = r.json()
	    try:
	        title = data['items'][0]['snippet']['title']
	        author = data['items'][0]['snippet']['channelTitle']
	        return {'title':title, 'channel':author}
	    except KeyError:
	        return {'title':'','channel':''}
	    except IndexError:
	    	return {'title':'','channel':''}

	def getPlayingSong(self):
		print "pobieram aktualnie grana piosenke"
		url = 'http://yarakitwitch.azurewebsites.net/Videos/ActualId'
		r = requests.get(url)
		data = r.json()
		title = self.getVidDesc(data['vidId'])['title']
		title = ''.join([i if ord(i) < 128 else ' ' for i in title])
		self.Send_message("Aktualny utwor to \"{0}\" link: http://youtube.com/watch?v={1}".format(title, data['vidId']))

	def playSound(self, user, sound):
		print "playing sound " + sound
		if sound+'\n' in self.soundBoard:
			json_data = {"sound_id":self.soundBoard.index(sound+'\n')}
			r = requests.post("http://rest.learncode.academy/api/gachi/sounds", data = json_data)
			if r.status_code == 200:
				self.Send_whisper(user, "Odtworzono twoj dzwiek: " + sound)
		else:
			self.Send_whisper(user, "Dostepne dzwieki sa na http://tiny.cc/yarSounds")

	def mainLoop(self):
		self.db = DatabaseControl()
		self.subsDb = CustomDbCtrl("subs.db")
		while True:
			if self.wbot.cmd != "":
				self.Send_message(self.wbot.cmd)
				self.wbot.cmd = ""

			self.readbuffer = self.readbuffer + self.s.recv(1024)
			temp = string.split(self.readbuffer, "\n")
			self.readbuffer = temp.pop()
			for line in temp:
				#print "Wiadomosc z serwera: " + line
				# Checks whether the message is PING because its a method of Twitch to check if you're afk
				if (line[0] == "PING"):
					self.s.send("PONG %s\r\n" % line[1])
				else:
					# Splits the given string so we can work with it better
					parts = string.split(line, ":")
					if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
						try:
							# Sets the message variable to the actual message sent
							message = ":".join([str(parts[2]),":".join(parts[3:])])
						except:
							message = ""
						# Sets the username variable to the actual username
						usernamesplit = string.split(parts[1], "!")
						username = usernamesplit[0]

						# Only works after twitch is done announcing stuff (MODT = Message of the day)
						if self.MODT:
							print username + ": " + message

							command = string.split(message[:-2], " ")
							#print str(command)

							# You can add all your plain commands here
							if self.wbot.emote != "" and command[0] == self.wbot.emote:
								self.emoteWin(username)
							if command[0] == "!points":
								self.points(username)
							if command[0] == "!roulette":
								try:
									if command[1] > 0:
										self.Send_message(self.roulette(username, command[1]))
									else:
										self.Send_message(username+" nice idea BrokeBack")
								except IndexError:
									self.Send_message(username+" all in? PogChamp")
							if command[0] == "!chat":
		 						self.ruinedChat()
							if command[0] == "!odds":
		 						self.odds()
							if command[0] == "!duel" and len(command)>2 and command[2].isdigit():
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
							if command[0] == "!sub":
								self.addToSubList(username)
							if command[0] == "!unsub":
								self.delFromSubList(username)
							if command[0] == "!sr" or command[0] == "!songrequest" and len(command)>1:
								url = str(string.split(message[:-1], " ")[1])
								if url.find("youtube.com") >= 0:
									self.addSongToList(url,username)
								else:
									self.Send_message(username+" musisz podac link do youtube")
							if command[0] == "!song":
								self.getPlayingSong()
							if command[0] == "!playlist":
								self.Send_message("Playlista: http://tiny.cc/yarakii")
							if command[0] == "!$playsound" and len(command)>1:
								self.playSound(username, command[1])

							#points to win in emote quiz
							if self.wbot.emotePoints > 0:
								self.wbot.emotePoints = self.wbot.emotePoints - 1
								self.emoteTries = self.emoteTries + 1

								if self.emoteTries % 10 == 0:
									self.Send_message("Podpowiedz emotki: "+self.wbot.emote[:int(self.emoteTries/10)] + "...")

						for l in parts:
							if "End of /NAMES list" in l:
								self.MODT = True
