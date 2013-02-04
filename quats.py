__author__ = 'Robert Evans'

import OrientSocket
import numpy
import pylab
import pca

def pcaQuats(input_filename, euler=False, n_components=1):
	quats = rawDataFileToQuats(input_filename)
	highDim = rearrangeQuatsForLatentSpaceAlgorithm(quats, euler)
	lowDim = pca.pca(highDim,n_components)
	return lowDim

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

def rearrangeQuatsForLatentSpaceAlgorithm(labelledQuats, euler=False):
	sensors = sorted(list(set([s for (s,q) in labelledQuats])))
	separateSensorsQuats = []
	for sensor in sensors:
		separateSensorsQuats.append([q for (s,q) in labelledQuats if s == sensor])

	if euler:
		return numpy.array([numpy.concatenate((a.toEuler(),b.toEuler(),c.toEuler())) for (a,b,c) in zip(*separateSensorsQuats)])
	else:
		return numpy.array([list(a.components + b.components + c.components) for (a,b,c) in zip(*separateSensorsQuats)])

def plotQuats(Quats, title='Quaternions'):
	X = numpy.zeros((len(Quats),4))
	for i in range(len(Quats)):
		X[i] = numpy.array(Quats[i].components)

	pylab.figure()
	pylab.plot(X)
	pylab.xlabel('Time (frames)')
	pylab.ylabel('Quaternion components')
	pylab.title(title)
	#pylab.legend((''))
	#pylab.tight_layout()
	#pylab.savefig('/Users/robertevans/Desktop/quats.pdf', format='pdf')
	pylab.show()

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
	#pylab.savefig('/Users/robertevans/Desktop/quats.pdf', format='pdf')
	pylab.show()

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
	#pylab.savefig('/Users/robertevans/Desktop/quats.pdf', format='pdf')
	pylab.show()