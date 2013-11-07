from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules import SoftmaxLayer
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.utilities import percentError
from pybrain.datasets import SequenceClassificationDataSet, ClassificationDataSet
from database_gyroGaits import gyroWalkingData
from scipy.cluster.hierarchy import fclusterdata
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def classificationDataSet(subjects=['a2','b','c1','c2'], segClass=0, db=None, seg_width=10):
	if not db:
		db = gyroWalkingData()

	DS = ClassificationDataSet(21, nb_classes=2)
	
	for subject in subjects:
		# Initialise data and segments
		raw = db.data[subject][:,2:]
		if 0 <= segClass < 4:
			segs = [s for s,c in db.manual_gait_segments[subject] if c == segClass]
		else:
			segs = db.segments[subject]

		# Add data
		for i in range(0,len(raw),seg_width):
			hasSeg = 0
			for j in range(seg_width):
				if i+j in segs:
					hasSeg = 1
			for j in range(seg_width):
				if i+j < len(raw):
					DS.appendLinked(raw[i+j],[hasSeg])
	
	DS._convertToOneOfMany()
	return DS

def getSummaryStatistics(data, std_window=10):
	gradients = []
	for col in range(np.shape(data)[1]):
		gradients.append(np.gradient(data[:,col]))
	gradients = np.column_stack(gradients)

	standardDeviations = []
	for col in range(np.shape(data)[1]):
		stdev = []
		for i in range(len(data)):
			stdev.append(np.std(data[:,col][i-(std_window/2):i+(std_window/2)]))
		standardDeviations.append(stdev)
	standardDeviations = np.column_stack(standardDeviations)

def networkAndTrainer(db, subjects=['a2','b','c1','c2'], segClass=0, windowSize=10):
	trainingData = classificationDataSet(subjects=subjects, segClass=segClass, db=db, seg_width=windowSize)
	net = buildNetwork( trainingData.indim, 30, 30, trainingData.outdim, outclass=SoftmaxLayer, fast=True)
	trainer = BackpropTrainer( net, dataset=trainingData, momentum=0.1, verbose=True, weightdecay=0.01)
	return (net, trainer)

def train(trainer, epochs=10):
	if epochs > 0:
		trainer.trainEpochs(epochs)
	else:
		trainer.trainUntilConvergence()

def getSegments(net, db, neural_dataset, subject='a1', n_segments=100, plot=True):
	# Most likely segments
	mostLikelySegs = sorted(zip(net.activateOnDataset(neural_dataset)[:,1],range(len(neural_dataset))))[-n_segments:]

	if plot:
		db.plotSegments(db.data[subject], [s for v,s in mostLikelySegs])
	segs = [s for _,s in mostLikelySegs]
	likelihoods = [l for l,_ in mostLikelySegs]
	return (segs,likelihoods)

def getClusters(segs, db, subject='a1', thresh=20.0, plot=True):
	clusters = fclusterdata([[s] for s in segs], thresh, criterion="distance")
	if plot:
		rawData = db.data[subject]
		plt.figure(figsize=(11,9))
		plt.plot(rawData[:,0],rawData[:,2:])
		colours = cm.rainbow(np.linspace(0, 1, len(set(clusters))))
		for i,s in enumerate(segs):
			plt.axvline(rawData[:,0][s],color=colours[clusters[i]-1],linewidth=2)
		plt.title("Clustered Neural Network Segments")
		plt.xlabel("Time (Seconds)")
		plt.ylabel("Rotation (Degrees per second)")
		#savefig('/Users/robertevans/Desktop/Gait analysis graphs/Segment clustering/'+name+'.pdf', format='pdf')
		plt.show()
	return clusters

def mostLikelySegsInClusters(segs, clusters, likelihoods):
	mostLikely = {}
	for c in set(clusters):
		mostLikely[c] = (0,0)
	for s,c,l in zip(segs,clusters,likelihoods):
		if l > mostLikely[c][1]:
			mostLikely[c] = (s,l)
	return [s for s,l in mostLikely.values()]

def demo(subject='a1', segClass=0, plot_stages=True, saveGraph=False, n_most_likely=100, windowSize=10, clusterThresh=40):
	db = gyroWalkingData()
	print "Building neural network"
	net,trainer=networkAndTrainer(db, segClass=segClass, subjects=list( set(db.segments) - set([subject])), windowSize=windowSize)
	print "Training network..."
	train(trainer, epochs=25)
	print "Finding segments"
	testingData = classificationDataSet(subjects=[subject], segClass=segClass, seg_width=windowSize, db=db)
	top_segments, likelihoods = getSegments(net, db, testingData, subject=subject, n_segments=n_most_likely, plot=plot_stages)
	print "Clustering segments"
	clusters = getClusters(top_segments, db, subject=subject, thresh=clusterThresh, plot=plot_stages)
	print "Showing most likely segment from each cluster"
	segments = mostLikelySegsInClusters(top_segments, clusters, likelihoods)
	db.plotSegments(db.data[subject], segments, name=("%s - segClass %i"%(subject, segClass)), save=saveGraph)

def saveGraphs():
	for s in ['a1','a2','b','c1','c2']:
		for c in range(4):
			demo(subject=s, segClass=c, plot_stages=False, saveGraph=True)