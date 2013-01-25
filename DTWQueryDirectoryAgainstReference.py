__author__ = "Robert Evans"

import Rdtw
import pylab
from os import listdir
from os.path import isfile, join
from matplotlib import pyplot as plt
import numpy as np
import glob

def dtwDirectoryAgainstReference(input_directory,reference_file):
	inputFiles = [ f for f in glob.glob("%s/*.csv"%input_directory) if f != "./"+reference_file]

	distList = []
	for f in inputFiles:
		distList = distList + [(Rdtw.getDTWdist(f,reference_file),f.split('/')[-1].split('.')[0])]

	distList.sort()

	files = [f for (d,f) in distList]
	dists = [d for (d,f) in distList]

	fig = plt.figure()
	ind = np.arange(len(files))
	plt.bar(ind, dists)
	plt.xticks(ind+0.81, files)
	fig.autofmt_xdate()
	plt.title("DTW distances with %s as reference"%reference_file.split('/')[-1].split('.')[0])
	plt.ylabel("Distance")
	
	pylab.rcParams.update({'font.size': 12})
	plt.show()
	pylab.tight_layout()
	#pylab.savefig('/Users/robertevans/Desktop/V1RefDTW.pdf', format='pdf')

if __name__=='__main__':
	import sys
	if (len(sys.argv)==3):
		sys.exit(dtwDirectoryAgainstReference(sys.argv[1],sys.argv[2]))
	print "Usage: DWTQueryDirectoryAgainstReference <input_directory> <reference_file>"