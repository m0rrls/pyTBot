import datetime
import numpy as np

class Date:
	def __init__(self):
		a = np.array(["test"])
		b = np.array(["test2"])
		c = np.array([datetime.datetime.now()])
		self.records = np.rec.fromarrays((a, b, c), names = ('nick1', 'nick2', 'date'))
		print str(self.records)

	def addNewRow(self):
		a = np.array(["test"])
		b = np.array(["test2"])
		c = np.array([datetime.datetime.now()])
		array = np.rec.fromarrays((a, b, c), names = ('nick1', 'nick2', 'date'))
		self.records += array

	def returnRecords(self):
		return self.records

obj = Date()
print obj.returnRecords()
