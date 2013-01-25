__author__ = 'Robert Evans'

import numpy
import pylab
import smooth

def plotCSV(input_filename):
	with open(input_filename,'r') as fin:
			X = numpy.loadtxt(fin,delimiter=",")

	pylab.figure()
	pylab.plot(X)
	pylab.xlabel('Time (frames)')
	pylab.ylabel('Latent co-ordinate')
	pylab.title('Horizontal Arm Spins - Post PCA')
	#pylab.legend((''))

	pylab.tight_layout()
	pylab.show()
	#pylab.savefig('/Users/robertevans/Desktop/postPCA.pdf', format='pdf')

if __name__=='__main__':
	import sys
	if (len(sys.argv)==2):
		sys.exit(plotCSV(sys.argv[1]))
	print "Usage: plotCSV <file.csv>"