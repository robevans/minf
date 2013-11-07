import pybrain as pb
import pybrain.tools.shortcuts as pb_shortcuts
import pybrain.structure.modules as pb_modules
import pybrain.supervised.trainers as pb_trainers
from database_gyroGaits import gyroWalkingData
import numpy as np
import scipy.cluster.hierarchy as hcluster
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class SubjectData:
	def __init__(self, training_subjects=['a1','a2','c1','c2'], test_subjects=['b'], db=None, sliding_window_size=3):
		if not db:
			db = gyroWalkingData()
		self.db = db

		self.trainingSet = self.datasetFromSubjects(training_subjects, sliding_window_size=sliding_window_size)
		self.testingSet = self.datasetFromSubjects(test_subjects, sliding_window_size=sliding_window_size)

	def datasetFromSubjects(self, subjects, sliding_window_size=5):
		DS = pb.datasets.ClassificationDataSet(21*sliding_window_size, 1, nb_classes=5, class_labels=["Left Toe Off", "Left Heel Strike", "Right Toe Off", "Right Heel Strike","None"])
		for subject in subjects:
			raw = self.db.data[subject][:,2:]
			segs, classes = zip(*self.db.manual_gait_segments[subject])
			# Slide a window over the data, and class each sequence as the class of the middle frame inside it.
			for i in range(0, len(raw)-sliding_window_size):

				# Find the class of middle frame in the window
				if i+(sliding_window_size/2) in segs:
					segmentClass = classes[segs.index(i+(sliding_window_size/2))]
				else:
					segmentClass = 4

				""" Set class as first segment in window, else None
				for j in range(sliding_window_size):
					if i+j in segs:
						segmentClass = classes[segs.index(i+j)]
						break
					else:
						segmentClass = 4
				"""

				# Label the whole window sequence with that class
				window = []
				for j in range(sliding_window_size):
					window = np.append(window, raw[i+j])
				DS.appendLinked(window,[segmentClass])

		DS._convertToOneOfMany()
		return DS


class NeuralNetworkSegmenter:
	def __init__(self, training_subjects=['a1','a2','c1','c2'], test_subject='b'):
		self.data = SubjectData( training_subjects=training_subjects, test_subjects=[test_subject] )
		self.net = pb_shortcuts.buildNetwork( self.data.trainingSet.indim, self.data.trainingSet.indim, self.data.trainingSet.indim, self.data.trainingSet.outdim, outclass=pb_modules.SoftmaxLayer, bias=True, fast=True )
		self.trainer = pb_trainers.BackpropTrainer( self.net, dataset=self.data.trainingSet, momentum=0.1, verbose=True, weightdecay=0.01)
		self.subjects = {"train":training_subjects, "test":test_subject}

	def train(self, epochs=0):
		if epochs > 0:
			self.trainer.trainEpochs(epochs)
		else:
			self.trainer.trainUntilConvergence()

	def test(self):
		mostLikelyByClass = self.mostLikelySegmentsInEachClass(n_most_probable=100)
		mostLikelyByCluster = self.mostLikelySegmentOfEachClusterInEachClass(mostLikelyByClass)

		taggedSegments = np.concatenate( map(lambda pair: [(s,pair[0]) for s in pair[1]], mostLikelyByCluster.items()) )

		subject = self.subjects['test']
		raw = self.data.db.data[subject]
		plt.figure(figsize=(11,9))
		plt.plot(raw[:,0],raw[:,2:])
		colours = cm.rainbow(np.linspace(0, 1, 4))
		legendHelpers = [0,0,0,0]
		for (seg,seg_class) in taggedSegments:
			legendHelpers[seg_class] = plt.axvline(raw[:,0][seg],color=colours[seg_class],linewidth=2)
		plt.title("Neural Network gait segmentation")
		plt.xlabel("Time (Seconds)")
		plt.ylabel("Rotation (Degrees per second)")
		plt.legend(legendHelpers,['Left Toe Off','Left Heel Strike','Right Toe Off','Right Heel Strike'])
		#plt.savefig('/Users/robertevans/Desktop/Gait analysis graphs/Segment clustering/'+name+'.pdf', format='pdf')
		plt.show()

	def mostLikelySegmentsInEachClass(self, n_most_probable=100, plot=False):
		outputs = self.net.activateOnDataset(self.data.testingSet)
		mostProbables = dict.fromkeys( range(self.data.testingSet.outdim-1) )
		for segClass in mostProbables.keys():
			mostProbables[segClass] = sorted( zip( outputs[:,segClass], range(len(outputs)) ) ) [-n_most_probable:]

		# TODO: deduplication

		if plot:
			for segClass in mostProbables.keys():
				print "Plotting class: %s" % self.data.testingSet.class_labels[segClass]
				self.data.db.plotSegments(self.data.db.data[self.subjects["test"][0]], [s for p,s in mostProbables[segClass]])

		return mostProbables

	def mostLikelySegmentOfEachClusterInEachClass(self, mostProbables, clusterThresh=20, plot=False):
		mostProbablePerClassCluster = dict.fromkeys( range(self.data.testingSet.outdim-1) )
		for segClass in mostProbables.keys():
			probabilities, segments = zip( *mostProbables.values()[segClass] )
			clusters = self.__getClusters(segments, thresh=clusterThresh, plot=plot)
			mostProbablePerClassCluster[segClass] = self.__mostLikelySegsInClusters(segments, clusters, probabilities)
		return mostProbablePerClassCluster

	def __getClusters(self, segments, thresh=20.0, plot=True):
		clusters = hcluster.fclusterdata([[s] for s in segments], thresh, criterion="distance")
		if plot:
			rawData = self.data.db.data[self.subjects["test"][0]]
			plt.figure(figsize=(11,9))
			plt.plot(rawData[:,0],rawData[:,2:])
			colours = cm.rainbow(np.linspace(0, 1, len(set(clusters))))
			for i,s in enumerate(segments):
				plt.axvline(rawData[:,0][s],color=colours[clusters[i]-1],linewidth=2)
			plt.title("Clustered Neural Network Segments")
			plt.xlabel("Time (Seconds)")
			plt.ylabel("Rotation (Degrees per second)")
			#savefig('/Users/robertevans/Desktop/Gait analysis graphs/Segment clustering/'+name+'.pdf', format='pdf')
			plt.show()
		return clusters

	def __mostLikelySegsInClusters(self, segs, clusters, likelihoods):
		mostLikely = {}
		for c in set(clusters):
			mostLikely[c] = (0,0)
		for s,c,l in zip(segs,clusters,likelihoods):
			if l > mostLikely[c][1]:
				mostLikely[c] = (s,l)
		return [s for s,l in mostLikely.values()]

def demoScript(test_subject='a1', plot_stages=True):
	training_subjects = set(['a1','a2','b','c1','c2']).difference([test_subject])
	nns=NeuralNetworkSegmenter()
	nns.train(epochs=100)
	nns.test()
	return nns


"""
class SequentialSubjectData:
	def __init__(self, training_subjects=['a1','a2','c1','c2'], test_subjects=['b'], db=None, sliding_window_size=5):
		if not db:
			db = gyroWalkingData()
		self.db = db

		self.trainingSet = self.datasetFromSubjects(training_subjects, sliding_window_size=sliding_window_size)
		self.testingSet = self.datasetFromSubjects(test_subjects, sliding_window_size=sliding_window_size)

	def datasetFromSubjects(self, subjects, sliding_window_size=5):
		DS = pb.datasets.SequenceClassificationDataSet(21, 1, nb_classes=5, class_labels=["Left Toe Off", "Left Heel Strike", "Right Toe Off", "Right Heel Strike","None"])
		for subject in subjects:
			raw = self.db.data[subject][:,2:]
			segs, classes = zip(*self.db.manual_gait_segments[subject])
			# Slide a window over the data, and class each sequence as the class of the first segment inside it.
			for i in range(0, len(raw)-sliding_window_size):
				DS.newSequence()
				# Find the class of first segment in the window
				for j in range(sliding_window_size):
					if i+j in segs:
						segmentClass = classes[segs.index(i+j)]
						break
					else:
						segmentClass = 4

				# Label the whole window sequence with that class
				for j in range(sliding_window_size):
					DS.appendLinked(raw[i+j],[segmentClass])

		DS._convertToOneOfMany()
		return DS
"""




