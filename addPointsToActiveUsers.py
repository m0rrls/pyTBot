import requests
import string
import sqlite3
from databaseControl import *
from time import *

class addPointsToActiveUsers:
	def addPoints(self, db):
		control = 0
		while control == 0:
			page = requests.get("https://tmi.twitch.tv/group/user/yarakii/chatters")
			page = page.content
			lines = string.split(page, "\n")
			control = 0
			for item in lines:
				if control == 0 and item.find("chatters")!=-1:
					control = 1
					print "Zaczynamy"
				elif control == 1 and "[" not in item and "]" not in item and "{" not in item and "}" not in item:
					nick = ""
					for i in item:
						tmp = ord(i)
						if (tmp>96 and tmp<123) or (tmp>47 and tmp<58) or tmp == 95:
							nick+=i
					db.addPointsToUser(str(nick), 5)
			if control == 1:
				print ("===================================")
				print ("dodano punkty aktywnym uzytkownikom")
				print ("===================================")
				return 1
