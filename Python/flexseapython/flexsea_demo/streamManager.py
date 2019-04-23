import os, sys
import time
from time import sleep
import csv
pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from pyFlexsea import *
from pyFlexsea_def import *
from fxUtil import *

class Stream:
	# Class variable that keeps track of the number of connections
	CURRENT_PORT_ID = 0
	
	def __init__(self,port, varsToStream, printingRate = 10,labels = None,updateFreq = 100, shouldLog = False, shouldAuto = 1):
		""" Intializes stream and printer """
		#init printer settings
		self.counter = 0
		self.prev_data = None
		self.labels = labels
		self.data = None
		self.rate = printingRate

		# load stream data
		self.varsToStream = varsToStream
		#global CURRENT_PORT_ID
		self.port = Stream.CURRENT_PORT_ID
		Stream.CURRENT_PORT_ID += 1
		self.devId = self._connectToDevice(port)
		self.shouldAuto = shouldAuto
		self.updateFreq = updateFreq
		self.shouldLog = shouldLog
		self.prevReadTime = time.time()

		# Start stream
		print("Starting stream", self.devId)
		fxSetStreamVariables(self.devId,self.varsToStream)
		print("Streaming vars")
		if not fxStartStreaming(self.devId,self.updateFreq,self.shouldLog,self.shouldAuto):
			raise Exception('Streaming failed')
		else:
			sleep(0.4)

	def _connectToDevice(self,port):
		print("connecting")
		fxOpen(port[0], 0)
		timeElapsed = 0
		TIMEOUT_LIMIT = 5
		print("here")
		while(timeElapsed <= TIMEOUT_LIMIT and not fxIsOpen(0)):
			# There is certainly a better way to do this
			sleep(0.2)
			timeElapsed += 0.2
			
		print("there")
		if(not fxIsOpen(0)):
			raise Exception("Couldn't connect to port {}".format(port))
		
		sleep(0.1)
		print("Leave")
		devId = fxGetDeviceIds()[0]
		return devId


	def writeToCSV(self):
		with open(self.fileName,'a') as fd:
			writer = csv.writer(fd)
			writer.writerow(self.data)

	def InitCSV(self,fileName):
		self.fileName = fileName 
		with open(self.fileName,'w') as fd:
			writer = csv.writer(fd)
			writer.writerow(self.labels)

	# TODO: Add protection from None type here rather than in all the scripts
	def __call__(self,data_labels = None):
		""" Allows the object to be updated by calling it as a function"""
		data = None
		currentTime = time.time()
		if abs(currentTime - self.prevReadTime) >= (1/self.updateFreq):
			self.data = fxReadDevice(self.devId,self.varsToStream)
		self.prevReadTime = currentTime
		if data_labels != None:
			data_index =[]
			for label in data_labels:
				data_index.append(self.varsToStream.index(label))
			data = [self.data[index] for index in data_index]	
		else:
			data = self.data

		return data

	def printData(self, clear_terminal = True, message = ""):
		""" Prints data with a predetermined delay, data must be updated before calling this function """
		if clear_terminal:
			clearTerminal()
		if message != "":
			print(message)
		if(self.counter% self.rate == 0):
			printData(self.labels,self.data)
			self.prev_data = self.data
		else:
			printData(self.labels,self.prev_data)
		self.counter += 1
	
	def __del__(self):
		""" Closes stream properly """
		Stream.CURRENT_PORT_ID -= 1
		fxStopStreaming(self.devId)
		closePort(self.port)
		cleanUpStream()
