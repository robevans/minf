__author__ = 'Robert Evans'

import pca
import dtw
import plot
import quats
import segment
import pylab as pl

def compareTwoFiles(f1,f2):
	data1 = readCSVfile(f1)
	data2 = readCSVfile(f2)
	ls1 = getLowDimensionalSegments(data1)[1:-1]
	ls2 = getLowDimensionalSegments(data2)[1:-1]
	
	names = []
	for i in range(len(ls1)):
		names.append('1')
	for i in range(len(ls2)):
		names.append('2')
		
	similarityMatrix(ls1+ls2,names)

def similarityMatrix(segments,segmentNames):
	distances = []
	for i in range(len(segments)):
		distances.append([])
		for j in range(len(segments)):
			distances[i].append(dtw.getDTWdist2D(segments[i],segments[j]))
	plot.plotSimilarityMatrix(distances,segmentNames)

def getLowDimensionalSegments(highDimensionalData):
	(lowDimensionalData,explainedVariance) = pca.pca(highDimensionalData,n_components=2)
	(mins,maxs) = segment.segmentationPoints(lowDimensionalData[:,0])
	segments = pl.split(lowDimensionalData,maxs)
	return segments

def getHighDimensionalSegments(highDimensionalData):
	(lowDimensionalData,explainedVariance) = pca.pca(highDimensionalData,n_components=1)
	(mins,maxs) = segment.segmentationPoints(lowDimensionalData[:,0])
	segments = pl.split(highDimensionalData,maxs)
	return segments

def readCSVfile(input_filename):
	with open(input_filename,'r') as fin:
			data = pl.loadtxt(fin,delimiter=",")
	return data