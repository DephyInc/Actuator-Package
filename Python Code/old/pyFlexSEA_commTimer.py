from threading import Timer,Thread,Event

class commTimer():

	def __init__(self,t,hFunction):
		self.t=t
		self.hFunction = hFunction
		self.thread = Timer(self.t,self.handle_function)
	
	def handle_function(self):
		self.hFunction()
		self.thread = Timer(self.t,self.handle_function)
		self.thread.start()
	
	def start(self):
		self.thread.start()

	def cancel(self):
		self.thread.cancel()

#Interface:
#t = commTimer(0.1, timerEvent) #TimerEvent is your function
#t.start()	#To Start it
#t.cancel()	#To Stop it
