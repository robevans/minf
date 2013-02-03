__author__ = 'Robert Evans'

import OrientSocket
import numpy
import pylab

def rawDataFileToQuats(input_filename):
	with open(input_filename) as f:
		lines = f.readlines()

	data = []
	for l in lines:
		numbers = map(float,filter(lambda x: x!='' ,l.translate(None,'[](),ary').split(' ')))
		nodeID = int(numbers[0])
		accelRTC = int(numbers[1])
		gyroRTC = int(numbers[2])
		magRTC = int(numbers[3])
		accel = numpy.array(numbers[4:7])
		gyro =  numpy.array(numbers[7:10])
		mag = numpy.array(numbers[10:13])
		data.append((nodeID, accelRTC, gyroRTC, magRTC, accel, gyro, mag))

	panda = OrientSocket.Panda(live=False)

	quats = []
	for d in data:
		q=panda.handleData(d, returnQuat=True)
		if q != None:
			quats.append((d[0],q.copy()))

	return quats

def plotQuats(Quats):
	X = numpy.zeros((len(Quats),4))
	for i in range(len(Quats)):
		X[i] = numpy.array(Quats[i].components)

	pylab.figure()
	pylab.plot(X)
	pylab.xlabel('Time (frames)')
	pylab.ylabel('Quaternion components')
	pylab.title('Quaternions')
	#pylab.legend((''))
	#pylab.tight_layout()
	pylab.show()
	#pylab.savefig('/Users/robertevans/Desktop/quats.pdf', format='pdf')

def plotQuatsAsEuler(Quats):
	X = numpy.zeros((len(Quats),3))
	for i in range(len(Quats)):
		X[i] = numpy.array(Quats[i].toEuler())

	pylab.figure()
	pylab.plot(X)
	pylab.xlabel('Time (frames)')
	pylab.ylabel('Euler angle')
	pylab.title('Euler angles')
	#pylab.legend((''))
	#pylab.tight_layout()
	pylab.show()
	#pylab.savefig('/Users/robertevans/Desktop/quats.pdf', format='pdf')

def plotQuatsFromFile(input_filename):
	with open(input_filename,'r') as f:
		lines = f.readlines()
	
	X = numpy.zeros((len(lines),4))
	for i in range(len(lines)):
		X[i] = numpy.array(map(float,lines[i][10:].translate(None,'( )').split(',')))

	pylab.figure()
	pylab.plot(X)
	pylab.xlabel('Time (frames)')
	pylab.ylabel('Quaternion components')
	pylab.title('Quaternions')
	#pylab.legend(('')) 
	#pylab.tight_layout()
	pylab.show()
	#pylab.savefig('/Users/robertevans/Desktop/quats.pdf', format='pdf')