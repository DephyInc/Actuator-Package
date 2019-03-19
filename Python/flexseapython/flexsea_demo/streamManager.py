import os, sys
import time
from time import sleep
import csv
pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from pyFlexsea import *
from pyFlexsea_def import *
from fxUtil import *

class StreamManager():
	def __init__(self,devId, varsToStream, printingRate = 10,labels = None,updateFreq = 100, shouldLog = False, shouldAuto = 1):
		""" Intializes stream and printer """
		#init printer settings
		self.counter = 0
		self.prev_data = None
		self.labels = labels
		self.data = None
		self.rate = printingRate

		# load stream data
		self.varsToStream = varsToStream
		self.devId = devId
		self.shouldAuto = shouldAuto
		self.updateFreq = updateFreq
		self.shouldLog = shouldLog
		self.prevReadTime = time.time()

		# Start stream
		fxSetStreamVariables(self.devId,self.varsToStream)
		if not fxStartStreaming(self.devId,self.updateFreq,self.shouldLog,self.shouldAuto):
			print("Streaming failed...")
			sys.exit(-1)
		else:
			sleep(0.4)
		
	def writeToCSV(self):		
		with open(self.fileName,'a') as fd:
			writer = csv.writer(fd)
			writer.writerow(self.data)

	def InitCSV(self,fileName):
		self.fileName = fileName 
		with open(self.fileName,'w') as fd:
			writer = csv.writer(fd)
			writer.writerow(self.labels)

	def __call__(self,data_labels = None):
		""" Allows the object to be updated by calling it as a function"""
		data = None
		currentTime = time.time()
		if abs(currentTime - self.prevReadTime) >= (1/self.updateFreq):
			tempData = fxReadDevice(self.devId,self.varsToStream)
			if tempData != None:
				self.data = tempData
			else:
				print("Read None value")
				
		self.prevReadTime = currentTime
		if data_labels != None:
			data_index =[]
			for label in data_labels:
				data_index.append(self.varsToStream.index(label))
			data = [self.data[index] for index in data_index]
		else:
			data = self.data

		return data

	def printData(self, clear_terminal = True, message = None):
		""" Prints data with a predetermined delay, data must be updated before calling this function """
		if clear_terminal:
			clearTerminal()
		if message != None:
			print(message)
		if(self.counter% self.rate == 0):
			printData(self.labels,self.data)
			self.prev_data = self.data
		else:
			printData(self.labels,self.prev_data)
		self.counter += 1
	
	def __del__(self):
		""" Closes stream properly """
		fxStopStreaming(self.devId)
