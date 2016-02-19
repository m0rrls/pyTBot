import requests
import string
import sqlite3
from databaseControl import *
from bs4 import BeautifulSoup
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
						if (tmp>96 and tmp<123) or (tmp>48 and tmp<58):
							nick+=i
					print "Dodaje punkt " + nick
					db.addPointsToUser(str(nick), 5)
			if control == 1:
				return 1

db = databaseControl()

addPoints = addPointsToActiveUsers()
while True:
	addPoints.addPoints(db)
	sleep(60)