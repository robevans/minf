__author__ = 'Robert Evans'

import numpy
import pylab

def plot_mins_and_maxs(X):
	pylab.figure()
	if X[0].size == 1:
		(mins,maxs) = find_mins_and_maxs1D(X)
		plot_mins_and_maxs1D(X,mins,maxs)
	if X[0].size > 1:
		for i in range(0,X[0].size):
			(mins,maxs) = find_mins_and_maxs1D(X[:,i])
			plot_mins_and_maxs1D(X[:,i],mins,maxs)

	pylab.plot(X)
	pylab.show()

def find_mins_and_maxs1D(timeseries):
	a = len(timeseries)
	mins = []
	maxs = []

	for i in range(1,a-1):
		if timeseries[i] > timeseries[i-1] and timeseries[i] > timeseries[i+1]:
			maxs = maxs + [i]
		if timeseries[i] < timeseries[i-1] and timeseries[i] < timeseries[i+1]:
			mins = mins +[i]

	return (mins,maxs)

def plot_mins_and_maxs1D(timeseries,mins,maxs):
	for x in mins:
		pylab.plot(x,timeseries[x],'ob')
	for x in maxs:
		pylab.plot(x,timeseries[x],'or')

if __name__=='__main__':
	import sys
	if (len(sys.argv)==2):
		with open(sys.argv[1],'r') as fin:
			X = numpy.loadtxt(sys.argv[1],delimiter=",")
		plot_mins_and_maxs(X)
		sys.exit(0)
	print "Usage: mins_and_maxs <file.csv>"