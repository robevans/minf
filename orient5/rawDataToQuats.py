__author__ = 'Robert Evans'

import OrientSocket
import numpy

def readRawData(input_filename):
	with open(input_filename) as f:
		lines = f.readlines()

	data = []
	for l in lines:
		numbers = map(float,filter(lambda x: x!='' ,l.translate(None,'[]()ary').split(' ')))
		print numbers
		nodeID = numbers[0]
		accelRTC = numbers[1]
		gyroRTC = numbers[2]
		magRTC = numbers[3]
		accel = numpy.array(numbers[4:7])
		gyro =  numpy.array(numbers[7:10])
		mag = numpy.array(numbers[10:13])
		data.append((nodeID, accelRTC, gyroRTC, magRTC, accel, gyro, mag))

	panda = OrientSocket.Panda(live=False)

	quats = []
	for d in data:
		quats.append(panda.handleData(d, returnQuat=True))

	return quats

if __name__=='__main__':
	import sys
	if (len(sys.argv)!=2):
		print "Usage: rawDataToQuats <filename>"
		sys.exit(0)
	sys.exit(readRawData(sys.argv[1]))