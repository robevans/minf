__author__ = 'Robert Evans'

import numpy as np
from rpy2.robjects.packages import importr
from rpy2 import robjects
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
R = rpy2.robjects.r
DTW = importr('dtw')

def getDTWdist2DweightedSum(queryDims,referenceDims,weights):
	if (np.shape(queryDims)[1] == np.shape(referenceDims)[1] == np.shape(weights)[0]):
		dist = 0
		for i in range(np.shape(queryDims)[1]):
			alignment = R.dtw(queryDims[:,i],referenceDims[:,i], keep=True)
			dist += weights[i] * alignment.rx('distance')[0][0]
		return dist
	else:
		import sys
		sys.exit("Bad input shapes for Dynamic Time Warp")

def drawGraphs(query, reference, fromFile=True):
	if fromFile:
		with open(query,'r') as fquery:
			query = np.loadtxt(fquery,delimiter=",")
		with open(reference,'r') as freference:
			reference = np.loadtxt(freference,delimiter=",")

	alignment = R.dtw(query, reference, keep=True)

	dist = alignment.rx('distance')[0][0]

	R.X11()
	R.dtwPlotTwoWay(alignment)
	#R.title(main = "DTW distance: %s for %s vs %s" % (dist,query,reference))
	R.title(main = "DTW distance: %s for Horizontal spin vs Vertical spin" % (dist))

	R.X11()
	R.dtwPlotThreeWay(alignment,main="")
	#R.title(main = "DTW distance: %s for %s vs %s" % (dist,query,reference))
	R.title(main = "Warping function for Horizontal spin vs Vertical spin")

	from enableInteractivity import enableInteractivity
	enableInteractivity()

def getDTWdist(queryFile,referenceFile):
	with open(queryFile,'r') as fquery:
		query = np.loadtxt(fquery,delimiter=",")
	with open(referenceFile,'r') as freference:
		reference = np.loadtxt(freference,delimiter=",")
	return dist(query,reference)

def dist(query,reference):
	alignment = R.dtw(query, reference, keep=True)
	dist = alignment.rx('distance')[0][0]
	return dist

if __name__=='__main__':
	import sys
	if (len(sys.argv)!=3):
		print "Usage: dtw <query_filename.csv> <reference_filename.csv>"
		sys.exit(0)
	sys.exit(drawGraphs(sys.argv[1],sys.argv[2]))