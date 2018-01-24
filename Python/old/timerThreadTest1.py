#Experimenting with timers & threads

from threading import Timer,Thread,Event
from time import sleep

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

def timerEvent():
	print('ipsem lorem')

t = commTimer(0.1, timerEvent)
t.start()

#"Main":
print('\nTimers & Threads - Test Code')
print('=============================\n')

#Demo code - Multiple Read, Rigid:
#===============================


x = 0
try:
	while True:
		print(x)
		x = x+1
		if(x > 999):
			x = 0
		sleep(0.001)
except KeyboardInterrupt:
	pass

t.cancel()
#Closing:
sleep(0.1)
print('\nDone.\n')
