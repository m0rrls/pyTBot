import datetime
import numpy as np
from time import *

class Duelists:
	def __init__(self):
		self.records = np.arange(3,)
		print self.records
	#Adds new duel	
	def addNewRow(self, user1, user2):
		y = np.array([(user1,user2, datetime.datetime.now())])
		self.records = np.vstack((self.records,y))
	
	#Removes duel
	def delRow(self, nr):
		self.records = np.delete(self.records, nr, 0)
		
	def getRecords(self):
		return self.records
		
	def getChallengers(self):
		x = self.records[...,0]
		return x[1:]
		
	def getTargets(self):
		x = self.records[...,1]
		return x[1:]
	
	#deletes any duel that is in table longer than M minutes
	def refresh(self, M):
		for x in self.records:
			if(x[0]!=0):
				time = (datetime.datetime.now() - x[2]).seconds
				print time
				if time > M*60:
					nr = np.where(self.records==x)
					self.delRow(nr[0][0])
