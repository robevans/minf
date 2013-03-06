__author__ = 'Robert Evans'

import pca
import plot
import segment
import pylab as pl

def readJointPositions(input_filename):  #TODO: make this function work with any number of orients
	with open(input_filename,'r') as f:
			lines = f.readlines()
	
	#d4 = []
	#d5 = []
	d8 = []
	for l in lines:
		l= map(float,filter(lambda x: x!='' ,l.translate(None,'(),/n')[:-1].split(' ')))
		id = l[0]
		xyz = l[1:]
		#if id == 4: d4.append(xyz)
		#if id == 5: d5.append(xyz)
		if id == 8: d8.append(xyz)

	#z=zip(*[d4,d5,d8])
	#z=zip(d4,d5,d8) #see if this works also 
	#data = [[a,b,c,d,e,f,g,h,i] for ([a,b,c],[d,e,f],[g,h,i]) in z]
	return d8
	#return data

def plotHighDim(input_filename):
	data=readJointPositions(input_filename)
	pl.plot(data)
	pl.show()

def plotLowDim(input_filename):
	data=readJointPositions(input_filename)
	latent=pca.pca(data,1)[0]
	pl.plot(latent)
	pl.show()
	return latent

def plotLowDim3D(input_filename):
	data=readJointPositions(input_filename)
	latent=pca.pca(data,2)[0]
	plot.plotPCA3D(latent)

def plotSegments(input_filename):
	data=readJointPositions(input_filename)
	latent=pca.pca(data,2)[0]
	segment.segmentAndPlot(latent[:,0])