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

def sequenceClassificationDataSet(subject='a1', db=None):
	"""Don't know if this is set up right or how to use it"""
	if not db:
		db = gyroWalkingData()

	raw = db.data[subject][:,2:]
	segs = db.segments[subject]
	DS = SequenceClassificationDataSet(21, 1)

	for i in range(0,len(raw),10):
		DS.newSequence()
		isSeg = 0
		for j in range(10):
			if i+j in segs:
				isSeg = 1
			else:
				isSeg = 0
			DS.appendLinked(raw[i+j],[isSeg])
	DS._convertToOneOfMany()
	return DS

def classificationDataSet(subject='a1', db=None):
	if not db:
		db = gyroWalkingData()

	raw = db.data[subject][:,2:]
	segs = db.segments[subject]
	DS = ClassificationDataSet(21, nb_classes=2)

	for i in range(0,len(raw),5):
		hasSeg = 0
		for j in range(5):
			if i+j in segs:
				hasSeg = 1
		for j in range(5):
			if i+j < len(raw):
				DS.appendLinked(raw[i+j],[hasSeg])
	DS._convertToOneOfMany()
	return DS

def classificationTrainingSet(holdouts=['a1'], db=None):
	if not db:
		db = gyroWalkingData()

	DS = ClassificationDataSet(21, nb_classes=2)
	
	for subject in db.data:
		if subject not in holdouts:
			raw = db.data[subject][:,2:]
			segs = db.segments[subject]

			seg_width = 2
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

def networkAndTrainer(db, holdouts=['a1']):
	trainingData = classificationTrainingSet(holdouts=holdouts, db=db)
	net = buildNetwork( trainingData.indim, 30, 30, trainingData.outdim, outclass=SoftmaxLayer, fast=True)
	trainer = BackpropTrainer( net, dataset=trainingData, momentum=0.1, verbose=True, weightdecay=0.01)
	return (net, trainer)

def train(trainer, epochs=10):
	trainer.trainEpochs(epochs)
	#trainer.trainUntilConvergence()

def test(db, trainer, test_subject='a1'):
	testingData = classificationDataSet(subject=test_subject, db=db)
	trainingData = classificationTrainingSet(holdout=[test_subject], db=db)
	trnresult = percentError( trainer.testOnClassData(), testingData['class'] )
	tstresult = percentError( trainer.testOnClassData(dataset=testingData), testingData['class'] )
	print "epoch: %4d" % trainer.totalepochs, "  train error: %f%%" % trnresult, "  test error: %f%%" % tstresult

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

def demo(subject='a1', plot_stages=True):
	db = gyroWalkingData()
	print "Building neural network"
	net,trainer=networkAndTrainer(db, holdouts=[subject])
	print "Training network..."
	train(trainer, epochs=25)
	print "Finding segments"
	testingData = classificationDataSet(subject=subject, db=db)
	top_segments, likelihoods = getSegments(net, db, testingData, subject=subject, n_segments=140, plot=plot_stages)
	print "Clustering segments"
	clusters = getClusters(top_segments, db, subject=subject, plot=plot_stages)
	print "Showing most likely segment from each cluster"
	segments = mostLikelySegsInClusters(top_segments, clusters, likelihoods)
	db.plotSegments(db.data[subject], segments)