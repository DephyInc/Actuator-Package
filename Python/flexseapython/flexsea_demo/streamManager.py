import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from pyFlexsea import *
from pyFlexsea_def import *
from fxUtil import *


class StreamManager():
	def __init__(self,devId, rate = 1,labels = None,vars_to_stream = None,update_freq = 100 ):
                #init printer settings
		self.counter = 0
		self.prev_data = None
		self.labels = labels
		self.data = None

                # load stream data
		self.rate = rate
		self.vars_to_stream = vars_to_stream
		self.devId = devId
		self.update_freq = update_freq

                # Start stream
                fxSetStreamVariables(self.devId,self.vars_to_stream)
		if not fxStartStreaming(self.devId,self.update_freq,False,0):
			print("Streaming failed...")
			sys.exit(-1)

	def resetPrinter(self):
		self.counter = 0
		self.labels = None
		self.prev_data = None
	
	def __call__(self):
		self.data = fxReadDevice(self.devId,self.vars_to_stream)
                return self.data

	def printData(self, clear_terminal = True, message = None):
		self.prev_data = self.data
		if clear_terminal:
			clearTerminal()
                if message != None:
                    print(message)

		if(self.counter % self.rate == 0):
			printData(self.labels,self.data)
		else:
			printData(self.labels,self.prev_data)
		self.counter += 1
	
	def __del__(self): 
		fxStopStreaming(self.devId)
