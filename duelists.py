import datetime
import numpy as np
from time import *

class Duelists:
	def __init__(self):
		self.records = np.arange(4,)
		#print self.records
	#Adds new duel
	def addNewRow(self, user1, user2, pkt):
		y = np.array([(str(user1),str(user2), datetime.datetime.now(), int(pkt))])
		self.records = np.vstack((self.records,y))
		#print self.records

	#Removes duel
	def delRow(self, nr):
		#print self.getRecords()[nr]
		self.records = np.delete(self.records, nr, 0)

	def getRecords(self):
		return self.records

	def getChallengers(self):
		x = self.records[...,0]
		return x[1:]

	def getTargets(self):
		x = self.records[...,1]
		return x[1:]

	def getSize(self):
		return np.size(self.records)

	def findRow(self, name):
		nb = -1
		for x in self.records:
			if name in x:
				nr = np.where(self.records==x)
				nb = nr[0][0]
		return nb

	def delUserRec(self, user1, user2):
		for x in self.records:
			if user1 in x and user2 in x:
				nr = np.where(self.records==x)
				#print nr
				self.delRow(nr[0][0])

	#deletes any duel that is in table longer than M minutes
	def refresh(self, M):
		if self.getSize() > 4:
			for x in self.records:
				if(x[0] != 0):
					time = (datetime.datetime.now() - x[2]).seconds
					#print time
					if time > M*60:
						nr = np.where(self.records==x)
						self.delRow(nr[0][0])
