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
	
	def __init__(self, port, baudRate, varsToStream, printingRate = 10, labels = None, updateFreq = 100, shouldLog = False, shouldAuto = 1):
		""" Intializes stream and printer """
		#init printer settings
		self.counter = 0
		self.prev_data = None
		self.labels = labels
		self.data = None
		self.rate = printingRate
		self.shouldAuto = shouldAuto
		self.updateFreq = updateFreq
		self.shouldLog = shouldLog
		self.prevReadTime = time.time()

		# load stream data
		self.devId = None
		self.varsToStream = varsToStream
		self.port = Stream.CURRENT_PORT_ID
		self.baudRate = baudRate
		self.devId = self._connectToDevice(port)
		#global CURRENT_PORT_ID
		Stream.CURRENT_PORT_ID += 1

		# Start stream
		fxSetStreamVariables(self.devId,self.varsToStream)
		# TODO: evaluate whether we want this embedded in plan stack to carry over for C++
		# scripts but for now this makes connections much more reliable
		sleep(0.1)
		if not fxStartStreaming(self.devId,self.updateFreq,self.shouldLog,self.shouldAuto):
			raise Exception('Streaming failed')
		else:
			sleep(0.4)

	def _connectToDevice(self,port):
		fxOpen(port, self.port, self.baudRate)
		timeElapsed = 0
		TIMEOUT_LIMIT = 10
		while(timeElapsed <= TIMEOUT_LIMIT and not fxIsOpen(self.port)):
			# There is certainly a better way to do this
			sleep(0.2)
			timeElapsed += 0.2

		if(not fxIsOpen(self.port)):
			raise Exception("Couldn't connect to port {}".format(port))
		
		sleep(0.1)
		MAX_DEVICE_ID_ATTEMPTS = 10
		num_attempts = 0
		devIds = fxGetDeviceIds()
		while(num_attempts < MAX_DEVICE_ID_ATTEMPTS and len(devIds) == 0):
			sleep(0.2)
			devIds = fxGetDeviceIds()
		
		if len(devIds) == 0:
			raise Exception('Failed to get device Id')
		devId = devIds[self.port]
		print("Devid is: ", devId)
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
		if self.devId:
			Stream.CURRENT_PORT_ID -= 1
			fxStopStreaming(self.devId)
			closePort(self.port)
