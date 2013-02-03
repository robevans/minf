__author__ = 'Robert'

from comms import *

def handleData(self,data):
	print wooo,data

c = CaptureThread(handleData)
c.start()
sleep(10)
c.stop=True;