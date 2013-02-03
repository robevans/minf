__author__ = 'Robert Evans'

import numpy
import pylab

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


if __name__=='__main__':
	import sys
	if (len(sys.argv)==2):
		sys.exit(plotQuats(sys.argv[1]))
	print "Usage: plotQuatsFromFile <file.csv>"