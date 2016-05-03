import sqlite3
import string

class DatabaseControl:

	def __init__(self):
		self.db = sqlite3.connect("sqlite.db")
		self.cursor = self.db.cursor()

	def getUserPoints(self, user):
		command = 'SELECT POINTS FROM POINTS WHERE NICK = \'' + user + '\';'
		self.cursor.execute(command)
		result = str(self.cursor.fetchone())
		if result == "None":
			return -1
		resultOnlyNumbers = ""
		for i in result:
			tmp = ord(str(i))
			if tmp>47 and tmp<58:
				resultOnlyNumbers = resultOnlyNumbers + i
		return resultOnlyNumbers

	def addUser(self, user):
		command = 'INSERT INTO POINTS VALUES (\'' + user + '\', 0);'
		self.cursor.execute(command)
		self.db.commit()

	def addPoints(self, user, points):
		command = 'UPDATE POINTS SET POINTS = ' + str(points) + ' WHERE NICK = \'' + user + '\';'
		self.cursor.execute(command)
		self.db.commit()

	def addPointsToUser(self, user, points):
		if len(user)>2:
			userPoints = self.getUserPoints(user)
			if userPoints == -1:
				self.addUser(user)
				print "dodano do bazy"
				userPoints = 0
			userPoints = int(userPoints)
			userPoints += points
			self.addPoints(user, userPoints)
			return "done"

class CustomDbCtrl:
	def __init__(self, plik):
		self.db = sqlite3.connect(plik)
		self.cursor = self.db.cursor()

	def createTab(self, table):
		command = 'CREATE TABLE ' + table + '(name VARCHAR(20) NOT NULL, data_dolacz DATE NOT NULL);'
		self.cursor.execute(command)
		self.db.commit()

	def addUser(self, user, table):
		tmp = self.getUsers(table)
		taken = 0
		for x in tmp:
			if user in x:
				print "ktos dodaje sie mimo, ze juz jest"
				taken = 1
				break
		if taken == 0:
			command = 'INSERT INTO ' + table + ' VALUES ( \'' + user + '\', CURRENT_TIMESTAMP);'
			self.cursor.execute(command)
			self.db.commit()
		return taken

	def delUser(self, user, table):
		command = 'DELETE FROM ' + table + ' WHERE name = \'' + user + '\';'
		self.cursor.execute(command)
		self.db.commit()

	def getUsers(self, table):
		command = 'SELECT name FROM '+ table +';'
		self.cursor.execute(command)
		result = self.cursor.fetchall()
		if result != "None":
			tab = []
			for x in result:
				tab.append(x[0])
			return tab

	def getSubInfo(self, table):
		command = 'SELECT name, julianday(\'now\') - julianday(data_dolacz) AS \'sub_time\' FROM '+ table +' ORDER BY sub_time DESC;'
		self.cursor.execute(command)
		result = self.cursor.fetchall()
		if result != "None":
			return result
