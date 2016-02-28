import requests
import string
import sqlite3
from databaseControl import *
from time import *

class AddPointsToActiveUsers:
	def addPoints(self, db):
		control = 0
		allUsers = 0
		while control == 0:
			page = requests.get("https://tmi.twitch.tv/group/user/yarakii/chatters")
			page = page.content
			lines = string.split(page, "\n")
			control = 0
			for item in lines:
				if control == 0 and item.find("chatters")!=-1:
					control = 1
				elif control == 1 and "[" not in item and "]" not in item and "{" not in item and "}" not in item:
					nick = ""
					for i in item:
						tmp = ord(i)
						if (tmp>96 and tmp<123) or (tmp>47 and tmp<58) or tmp == 95:
							nick+=i
					db.addPointsToUser(str(nick), 5)
					allUsers += 1
			if control == 1:
				print ("========================================================")
				print ("dodano punkty aktywnym uzytkownikom, jest ich: " + str(allUsers))
				print ("========================================================")
				return 1
