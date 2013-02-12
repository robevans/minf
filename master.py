__author__ = 'Robert Evans'

import pca
import dtw
import plot
import quats
import segment
import pylab as pl

def compareTwoFiles(f1,f2,n_components=3):
	data1 = readCSVfile(f1)
	data2 = readCSVfile(f2)
	(ls1,w1) = getLowDimensionalSegments(data1,n_components)
	(ls2,w2) = getLowDimensionalSegments(data2,n_components)
	averageWeights = [(a+b)/2.0 for (a,b) in zip(w1,w2)]
	names = []
	for i in range(len(ls1)):
		names.append('1')
	for i in range(len(ls2)):
		names.append('2')

	similarityMatrix(ls1+ls2,names,averageWeights)

def similarityMatrix(segments,segmentNames,weights,title):
	distances = []
	for i in range(len(segments)):
		distances.append([])
		for j in range(len(segments)):
			distances[i].append(dtw.getDTWdist2DweightedSum(segments[i],segments[j],weights))
	plot.plotSimilarityMatrix(distances,segmentNames,title)

def getQuaternionSegmentsByRawData(highDimensionalData,quaternionData):
	(lowDimensionalData,explainedVariance) = pca.pca(highDimensionalData,n_components=1)
	(mins,maxs) = segment.segmentationPoints(lowDimensionalData[:,0])
	segments = pl.split(quaternionData,maxs)[1:-1]
	return segments

def getLowDimensionalSegments(highDimensionalData,n_components=2,plt=False,title="Latent space segments"):
	(lowDimensionalData,explainedVariance) = pca.pca(highDimensionalData,n_components)
	(mins,maxs) = segment.segmentationPoints(lowDimensionalData[:,0])
	segments = pl.split(lowDimensionalData,maxs)[1:-1]
	if plt:
		plot.plotGridOf2Ds(segments,title)
	return (segments,explainedVariance)

def getHighDimensionalSegments(highDimensionalData):
	(lowDimensionalData,explainedVariance) = pca.pca(highDimensionalData,n_components=1)
	(mins,maxs) = segment.segmentationPoints(lowDimensionalData[:,0])
	segments = pl.split(highDimensionalData,maxs)[1:-1]
	return segments

def readCSVfile(input_filename):
	with open(input_filename,'r') as fin:
			data = pl.loadtxt(fin,delimiter=",")
	return data