__author__ = 'Robert Evans'

import pca
import dtw
import plot
import quats
import numpy
import segment
import pylab as pl
import progressbar

def similarityMatrix(segments,segmentNames,weights,title,savePlot=False):
	print "Constructing similarity matrix"
	bar = progressbar.ProgressBar(maxval=len(segments)**2, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()
	progressCount = 0
	distances = []
	for i,k in zip(range(len(segments)),reversed(range(len(segments)))):
		distances.append([])
		for j in range(len(segments)):
			distances[i].append(dtw.getDTWdist2DweightedSum(segments[k],segments[j],weights))
			progressCount+=1
			bar.update(progressCount)
	bar.finish()
	plot.plotSimilarityMatrix(distances,segmentNames,title,savePlot)

def averageSimilarityMatrix(dictOfClasses, dictOfWeights,title,savePlot=False):
	print "Constructing similarity matrix"
	if sorted(dictOfClasses.keys()) != sorted(dictOfWeights.keys()):
		import sys
		sys.exit("Mismatching keys between weights and classes to compute average similarity matrix")
	bar = progressbar.ProgressBar(maxval=len(dictOfClasses.keys())**2, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()
	progressCount = 0
	distances = []

	for i,k in zip(range(len(dictOfClasses.keys())),reversed(sorted(dictOfClasses.keys()))):
		distances.append([])
		for j in sorted(dictOfClasses.keys()):
			distances[i].append(interClassDistance(dictOfClasses[k],dictOfClasses[j],dictOfWeights[k],dictOfWeights[j]))
			progressCount+=1
			bar.update(progressCount)
	bar.finish()

	plot.plotSimilarityMatrix(distances,sorted(dictOfClasses.keys()),title,savePlot)

def interClassDistance(classA,classB,classAweights,classBweights):
	summedDistances = 0
	for a,aw in zip(classA,classAweights):
		for b,bw in zip(classB,classBweights):
			weights = [float(sum(t))/float(len(t)) for t in zip(aw,bw)]
			summedDistances += dtw.getDTWdist2DweightedSum(a,b,weights)
	averageDistance = summedDistances / (len(classA)*len(classB))
	return averageDistance

def compareTwoFiles(f1,f2,n_components=3, raw=False, title="similarityMatrix"):
	if raw:
		data1 = readRaw(f1)[26:,4:]
		data2 = readRaw(f2)[26:,4:]
	else:
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

	similarityMatrix(ls1+ls2,names,averageWeights,title)

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

def getHighAndLowDimSegments(highDimensionalData, n_components=3):
	(lowDimensionalData,explainedVariance) = pca.pca(highDimensionalData,n_components)
	(mins,maxs) = segment.segmentationPoints(lowDimensionalData[:,0])
	HDsegments = pl.split(highDimensionalData,maxs)[1:-1]
	LDsegments = pl.split(lowDimensionalData,maxs)[1:-1]
	return (HDsegments,LDsegments,explainedVariance)

def readCSVfile(input_filename):
	with open(input_filename,'r') as fin:
			data = pl.loadtxt(fin,delimiter=",")
	return data

def readRaw(input_filename):
	with open(input_filename,'r') as f:
		lines = f.readlines()
	data = []
	for l in lines:
		l= map(float,filter(lambda x: x!='' ,l.translate(None,',ary()[]/n')[:-1].split(' ')))
		data.append(l)
	return numpy.array(data)