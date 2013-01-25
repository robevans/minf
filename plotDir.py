__author__ = 'Robert Evans'

import glob
import math
import numpy
import pylab
import matplotlib.pyplot as plt

def plotDir(input_directory):

	inputFiles = glob.glob("%s/*.csv"%input_directory)

	data = []
	names = []
	for f in inputFiles:
		with open(f,'r') as fin:
			data.append(numpy.loadtxt(fin,delimiter=","))
			names.append(f.split('/')[-1].split('.')[0])

	n = int(math.ceil(math.sqrt(len(data))))
	figure,axes = plt.subplots(n, n, sharex=True, sharey=True)

	i = 0
	for r in range(n):
		for c in range(n):
			if i >= len(data):
				axes[r,c].axis('off')
			else:
				axes[r,c].plot(data[i])
				axes[r,c].set_title(names[i])
			i+=1

	if len(data)-(n*n) != 0:
		plt.setp([a.get_xticklabels() for a in axes[-2, len(data)-(n*n):]], visible=True)

	pylab.tight_layout()
	#pylab.savefig('/Users/robertevans/Desktop/VHsegments.pdf', format='pdf')
	plt.show()

if __name__=='__main__':
	import sys
	if (len(sys.argv)==2):
		sys.exit(plotDir(sys.argv[1]))
	print "Usage: plotDir <directoryWithCSVfiles>"