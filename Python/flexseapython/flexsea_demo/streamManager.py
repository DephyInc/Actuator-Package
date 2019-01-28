import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from pyFlexsea import *
from pyFlexsea_def import *
from fxUtil import *

class StreamManager():
	def __init__(self,devId, varsToStream, printingRate = 10,labels = None,updateFreq = 100):
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
		self.updateFreq = updateFreq

		# Start stream
	    	fxSetStreamVariables(self.devId,self.varsToStream)
		if not fxStartStreaming(self.devId,self.updateFreq,False,0):
			print("Streaming failed...")
			sys.exit(-1)
	
	def __call__(self):
		""" Allows the object to be updated by calling it as a function"""
		self.data = fxReadDevice(self.devId,self.varsToStream)
		return self.data

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
