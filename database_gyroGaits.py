import csv
import math
import numpy as np
from pca import pca
from sklearn.decomposition import PCA
from smooth import smooth
from scipy.signal import argrelmax, argrelmin
from matplotlib.pyplot import plot, show, figure, axvline, title, xlabel, ylabel, savefig, legend
from sklearn import svm, preprocessing, cluster
from random import shuffle
import matplotlib.cm as cm
import matplotlib

from rpy2.robjects.packages import importr
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
DTW = importr('dtw')

class gyroWalkingData:
	def __init__(self, sourceDir="captures/Gait data"):
		self.__gl4east1_data, _ = self.parse(sourceDir+'/gl4east1.csv')
		self.__gl4west1_data, _ = self.parse(sourceDir+'/gl4west1.csv')
		self.__gl6east1_data, _ = self.parse(sourceDir+'/gl6east1.csv')
		self.__gl7east1_data, _ = self.parse(sourceDir+'/gl7east1.csv')
		self.__gl7west1_data, _ = self.parse(sourceDir+'/gl7west1.csv')
		self.__gl7east2_data, _ = self.parse(sourceDir+'/gl7east2.csv')

		self.accel = self.__gl7east2_data

		# Crop data
		self.__gl4east1_data = self.__gl4east1_data[160:700]
		self.__gl4west1_data = self.__gl4west1_data[:590]

		self.data = {"a1":self.__gl4east1_data, "a2":self.__gl4west1_data, "b":self.__gl6east1_data, "c1":self.__gl7east1_data, "c2":self.__gl7west1_data}
		
		self.__fullKey = ['Time', 'Frame', 'Pelvis_X', 'Pelvis_Y', 'Pelvis_Z', 'RFEP_X', 'RFEP_Y', 'RFEP_Z', 'RFEO_X', 'RFEO_Y', 'RFEO_Z', 'RTIO_X', 'RTIO_Y', 'RTIO_Z', 'LFEP_X', 'LFEP_Y', 'LFEP_Z', 'LFEO_X', 'LFEO_Y', 'LFEO_Z', 'LTIO_X', 'LTIO_Y', 'LTIO_Z']
		self.__sensorKey = {'Time':(0,1),'Pelvis':(2,5),'RFEP':(5,8),'RFEO':(8,11),'RTIO':(11,14),'LFEP':(14,17),'LFEO':(17,20),'LTIO':(20,23)}
		self.keys = {"full":self.__fullKey, "sensor":self.__sensorKey}

		self.__sensors_gl4east1 = self.dataBySensor(self.__gl4east1_data)
		self.__sensors_gl4west1 = self.dataBySensor(self.__gl4west1_data)
		self.__sensors_gl6east1 = self.dataBySensor(self.__gl6east1_data)
		self.__sensors_gl7east1 = self.dataBySensor(self.__gl7east1_data)
		self.__sensors_gl7west1 = self.dataBySensor(self.__gl7west1_data)
		self.sensorData = {"a1":self.__sensors_gl4east1, "a2":self.__sensors_gl4west1, "b":self.__sensors_gl6east1, "c1":self.__sensors_gl7east1, "c2":self.__sensors_gl7west1}

		self.__segments_gl4east1 = self.findSegments(self.__gl4east1_data, minSegSize=40, peakFunc=argrelmin)
		self.__segments_gl4west1 = self.findSegments(self.__gl4west1_data, minSegSize=40, peakFunc=argrelmax)
		self.__segments_gl6east1 = self.findSegments(self.__gl6east1_data, minSegSize=40, peakFunc=argrelmax, smoothData=True)[1:-1]
		self.__segments_gl7east1 = self.findSegments(self.__gl7east1_data, minSegSize=40, peakFunc=argrelmin)
		self.__segments_gl7west1 = self.findSegments(self.__gl7west1_data, minSegSize=40, peakFunc=argrelmin)[:-1]
		self.segments = {"a1":self.__segments_gl4east1, "a2":self.__segments_gl4west1, "b":self.__segments_gl6east1, "c1":self.__segments_gl7east1, "c2":self.__segments_gl7west1}

		# Manual segmentation of gait cycle
		# segment key:
		# Left toe off:		0
		# Left heel strike:	1
		# Right toe off:	2
		# Right heel strike:3
		self.__manual_a1 = [(30,0),(55,1),(66,2),(95,3),(102,0),(129,1),(137,2),(158,3),(169,0),(192,1),(201,2),(224,3),(230,0),(257,1),(264,2),(286,3),(294,0),(322,1),(330,2),(354,3),(361,0),(386,1),(395,2),(421,3),(430,0),(454,1),(463,2),(484,3),(499,0)]
		self.__manual_a2 = [(14,1),(23,2),(52,3),(57,0),(83,1),(89,2),(114,3),(119,0),(143,1),(150,2),(174,3),(182,0),(206,1),(214,2),(238,3),(247,0),(270,1),(281,2),(306,3),(314,0),(339,1),(348,2),(373,3),(385,0),(401,1)]
		self.__manual_b  = [(48,0),(75,1),(92,2),(125,3),(146,0),(181,1),(194,2),(231,3),(251,0),(287,1),(301,2),(341,3),(365,0),(398,1),(410,2),(449,3),(465,0),(502,1),(514,2),(550,3),(570,0),(606,1),(619,2),(658,3),(678,0),(713,1),(725,2),(760,3),(782,0),(814,1),(828,2),(864,3),(889,0),(918,1),(933,2),(969,3),(995,0),(1031,1),(1046,2),(1086,3),(1110,0),(1157,1),(1186,2)]
		self.__manual_c1 = [(18,0),(49,1),(56,2),(90,3),(100,0),(130,1),(138,2),(171,3),(180,0),(212,1),(220,2),(253,3),(262,0),(292,1),(300,2),(331,3),(341,0),(373,1),(381,2),(414,3),(424,0),(453,1),(462,2)]
		self.__manual_c2 = [(9,0),(33,1),(44,2),(80,3),(93,0),(122,1),(131,2),(164,3),(174,0),(207,1),(214,2),(247,3),(258,0),(287,1),(294,2),(328,3),(337,0),(368,1),(378,2),(412,3),(422,0),(450,1),(460,2),(493,3),(502,0),(535,1),(545,2),(579,3),(589,0)]
		self.manual_gait_segments = {"a1":self.__manual_a1, "a2":self.__manual_a2, "b":self.__manual_b, "c1":self.__manual_c1, "c2":self.__manual_c2}

	def findSegments(self, rawData, minSegSize=40, smoothData=False, window_len=5, window='blackman', peakFunc=argrelmax):
		principal_component_of_left_foot = self.PCABySensor(rawData)['LTIO'][:,0]

		if smoothData:
			principal_component_of_left_foot = smooth(principal_component_of_left_foot, window_len=window_len,window=window)

		segPoints = peakFunc(principal_component_of_left_foot,order=minSegSize)[0]
		return segPoints

	def plotGaitCycle(self, subject='a1'):
		figure(figsize=(11,9))
		plot(self.data[subject][:,0],self.data[subject][:,2:])
		colours = cm.rainbow(np.linspace(0, 1, 4))
		legendHelpers = [0,0,0,0]
		for (seg,seg_class) in self.manual_gait_segments[subject]:
			legendHelpers[seg_class] = axvline(self.data[subject][:,0][seg],color=colours[seg_class],linewidth=2)
		title("Manual gait segmentation")
		xlabel("Time (Seconds)")
		ylabel("Rotation (Degrees per second)")
		legend(legendHelpers,['Left Toe Off','Left Heel Strike','Right Toe Off','Right Heel Strike'])
		#savefig('/Users/robertevans/Desktop/Gait analysis graphs/Segment clustering/'+name+'.pdf', format='pdf')
		show()

	def plotSegments(self, rawData, segPoints, name=None, save=False):
		figure(figsize=(11,9))
		plot(rawData[:,0],rawData[:,2:])
		for s in segPoints:
			if s <= len(rawData):
				axvline(rawData[:,0][s],color='black',linewidth=2)
		title("Neural Network Based Gait Segmentation")
		xlabel("Time (Seconds)")
		ylabel("Rotation (Degrees per second)")
		if save:
			savefig('/Users/robertevans/Desktop/Gait analysis graphs/Full cycle segmentation/'+name+'.pdf', format='pdf')
		else:
			show()

	def plotSegment(self, rawData, segment, half=None):
		""" Set half to 'left' or 'right' to plot only the data from one leg"""
		figure(figsize=(11,9))
		key = self.__fullKey[2:]
		if half=="right":
			rawData = rawData[:,[0,1,5,6,7,8,9,10,11,12,13]]
			key = key[3:12]
		if half=="left":
			rawData = rawData[:,[0,1,14,15,16,17,18,19,20,21,22]]
			key = key[12:]
		ColourSeqOriginal = matplotlib.rcParams['axes.color_cycle']
		matplotlib.rcParams['axes.color_cycle'] = cm.spectral( np.linspace( 0, 1, np.shape(rawData)[1] ) ).tolist()
		plot(rawData[segment[0]:segment[1],0],rawData[segment[0]:segment[1],2:])
		title("Gait Segment")
		xlabel("Time (Seconds)")
		ylabel("Rotation (Degrees per second)")
		leg = legend(key)
		for legobj in leg.legendHandles:
			legobj.set_linewidth(10.0)
		matplotlib.rcParams['axes.color_cycle'] = ColourSeqOriginal
		show()

	def plotSegmentGrid(self, rawData, segments, subject=None):
		if subject:
			rawData = self.data[subject]
			segments = self.segments[subject]
		f = figure()
		for i in range(len(segments)-1):
			sqrt = int(math.ceil(math.sqrt(len(segments)-1)))
			ax = f.add_subplot(sqrt,sqrt,i+1)
			ax.plot(rawData[segments[i]:segments[i+1],0],rawData[segments[i]:segments[i+1],2:])
			
			last_row = (len(segments)-1)/sqrt
			if i/sqrt == last_row:
				xlabel("Time (Seconds)")
			if i/sqrt == last_row-1 and i%sqrt >= sqrt - (sqrt**2 - len(segments)+1):
				xlabel("Time (Seconds)")
			if i%sqrt == 0:
				ylabel("Rotation (Degrees per second)")
			if i == 0:
				title("Automatic Gait Segmentation")
		show()

	def parse(self, filepath, headerLines=9):
		with open(filepath,'rb') as csvfile:
			dialect = csv.Sniffer().sniff(csvfile.read())
			csvfile.seek(0)
			reader = csv.reader(csvfile,dialect)
			lines = 0
			data =[]
			for l in reader:
				lines += 1
				if lines <= headerLines:
					if lines == headerLines:
						key = l
				else:
					data.append([float(x) for x in l])
			return (np.array(data),key)

	def dataBySensor(self, data):
		return {k:data[:,range(*v)] for k,v in self.__sensorKey.items()}

	def PCABySensor(self, data, n_components=3):
		dataBySensor = self.dataBySensor(data)
		pcaDict = {}
		for k,v in dataBySensor.items():
			pcaDict[k] = pca(v,n_components)[0]
		pcaDict['Time'] = dataBySensor['Time']
		return pcaDict

	def pca_dict(self, n_components=3, whiten=True):
		dimReducer = PCA(n_components=n_components, whiten=whiten)
		alldata = np.concatenate(self.data.values())[:,2:]
		dimReducer.fit(alldata)
		return {k:dimReducer.transform(v[:,2:]) for k,v in self.data.items()}


class PCAclusteringSegmenter:
	def __init__(self, db=None):
		if not db:
			self.db = gyroWalkingData()
		else:
			self.db = db

	def findSegments(self, rawData, minSegSize=20):
		PCs = pca(rawData, n_components=2)[0]
		minSegs = argrelmin(PCs[:,0],order=minSegSize)[0]
		maxSegs = argrelmax(PCs[:,0],order=minSegSize)[0]
		minSegs_secondComponentValues = [[PCs[:,1][s]] for s in minSegs]
		maxSegs_secondComponentValues = [[PCs[:,1][s]] for s in maxSegs]

		clf=cluster.KMeans(2)
		min_clusters = clf.fit_predict(minSegs_secondComponentValues)
		max_clusters = clf.fit_predict(maxSegs_secondComponentValues)

		indexes_min_cluster0 = [s for (s,c) in zip(minSegs,min_clusters) if c == 0]
		indexes_min_cluster1 = [s for (s,c) in zip(minSegs,min_clusters) if c == 1]
		indexes_max_cluster0 = [s for (s,c) in zip(maxSegs,max_clusters) if c == 0]
		indexes_max_cluster1 = [s for (s,c) in zip(maxSegs,max_clusters) if c == 1]

		values_min_cluster0 = map(lambda x: PCs[:,0][x], indexes_min_cluster0)
		values_min_cluster1 = map(lambda x: PCs[:,0][x], indexes_min_cluster1)
		values_max_cluster0 = map(lambda x: PCs[:,0][x], indexes_max_cluster0)
		values_max_cluster1 = map(lambda x: PCs[:,0][x], indexes_max_cluster1)

		average_min_cluster0 = abs(sum(values_min_cluster0)/float(len(values_min_cluster0)))
		average_min_cluster1 = abs(sum(values_min_cluster1)/float(len(values_min_cluster1)))
		average_max_cluster0 = abs(sum(values_max_cluster0)/float(len(values_max_cluster0)))
		average_max_cluster1 = abs(sum(values_max_cluster1)/float(len(values_max_cluster1)))

		max_average = max(average_min_cluster0, average_min_cluster1, average_max_cluster0, average_max_cluster1)

		if max_average == abs(average_min_cluster0):
			return indexes_min_cluster0
		if max_average == abs(average_min_cluster1):
			return indexes_min_cluster1
		if max_average == abs(average_max_cluster0):
			return indexes_max_cluster0
		if max_average == abs(average_max_cluster1):
			return indexes_max_cluster1

class SVM:
	def __init__(self, db=None):
		if not db:
			self.db = gyroWalkingData()
		else:
			self.db = db

	def trainingDataForOneSubject(self, subject='a1', window=5):
		data = self.db.PCABySensor(preprocessing.scale(self.db.data[subject]), n_components=2)
		#data = self.db.PCABySensor(self.db.data[subject], n_components=1)
		#data = {k:preprocessing.scale(v) for k,v in data.items()}
		derivatives={k:np.gradient(np.array([x[0] for x in v])) for k,v in data.items()}
		trueSegments = self.db.segments[subject]

		X,Y = [],[]
		for i in range(0,len(data['Time']),window):

			raw = list(sum(data['Pelvis'][i:i+window])/window) + list(sum(data['RFEP'][i:i+window])/window) + list(sum(data['RFEO'][i:i+window])/window) + list(sum(data['RTIO'][i:i+window])/window) + list(sum(data['LFEP'][i:i+window])/window) + list(sum(data['LFEO'][i:i+window])/window) + list(sum(data['LTIO'][i:i+window])/window)
			#principal_components = [(sum(data['Pelvis'][i:i+window])/window)[0], (sum(data['RFEP'][i:i+window])/window)[0], (sum(data['RFEO'][i:i+window])/window)[0], (sum(data['RTIO'][i:i+window])/window)[0], (sum(data['LFEP'][i:i+window])/window)[0], (sum(data['LFEO'][i:i+window])/window)[0], (sum(data['LTIO'][i:i+window])/window)[0]]
			#gradient = [(sum(derivatives['Pelvis'][i:i+window])/window), (sum(derivatives['RFEP'][i:i+window])/window), (sum(derivatives['RFEO'][i:i+window])/window), (sum(derivatives['RTIO'][i:i+window])/window), (sum(derivatives['LFEP'][i:i+window])/window), (sum(derivatives['LFEO'][i:i+window])/window), (sum(derivatives['LTIO'][i:i+window])/window)]
			X.append(raw)

			containsSegment=False
			for j in range(i,i+window):
				if j in trueSegments:
					containsSegment = True
			if containsSegment:
				Y.append(1)
			else:
				Y.append(0)

		return X, Y

	def testClassifier(self, test_subject='a1', window=5):
		train,test=self.splitData(test_subject=test_subject, window=window)
		clf = svm.SVC()
		clf.fit(*train)
		result = zip(clf.predict(test[0]),test[1])
		
		trueNegatives = len(filter(lambda t:t==(0,0),result))
		falseNegatives = len(filter(lambda t:t==(0,1),result))
		falsePositives = len(filter(lambda t:t==(1,0),result))
		truePositives = len(filter(lambda t:t==(1,1),result))

		sensitivity = truePositives/float(truePositives+falseNegatives)
		specificity = trueNegatives/float(trueNegatives+falsePositives)

		print "%s:"%test_subject
		print "Sensitivity: %.02f%%"%(sensitivity*100)
		print "Specificity: %.02f%%"%(specificity*100)
		return self.reconstructSegments(clf.predict(test[0]), window)

	def splitData(self, test_subject='a1', window=5):
		test_X, test_Y = self.trainingDataForOneSubject(test_subject, window=window)
		trainingData = map(lambda x:self.trainingDataForOneSubject(x, window), [k for k in self.db.data if k != test_subject])
		X,Y=[],[]
		for x,y in trainingData:
		    X = X + x
		    Y = Y + y
		training_X, training_Y = X,Y
		return [(training_X, training_Y), (test_X, test_Y)]

	def splitAndShuffleData(self, split=0.5):
		trainingData = map(self.trainingDataForOneSubject, self.db.data)
		X,Y=[],[]
		for x,y in trainingData:
		    X = X + x
		    Y = Y + y
		merged = zip(X,Y)
		shuffle(merged)
		X,Y = [list(t) for t in zip(*merged)]
		training_X, training_Y = X[:int(len(X)*split)], Y[:int(len(Y)*split)]
		test_X, test_Y = X[int(len(X)*split):], Y[:int(len(Y)*split):]
		return [(training_X, training_Y), (test_X, test_Y)]

	def reconstructSegments(self, svmPrediction, window):
		windowSegments = [i for i,v in enumerate(svmPrediction) if v == 1]
		expandedSegments = map(lambda x: x*window-round(window/2.0),windowSegments)
		return expandedSegments

class gaitMeasures:
	def __init__(self, db=None):
		if not db:
			self.db = gyroWalkingData()
		else:
			self.db = db

	def timeDependentVelocityOfMovement(self):
		"""Measuring change in velocity throughout stride"""
		pass

	def numberOfStepsPerMinute(self, subject='a1'):
		stridesPerMinute = 60.0 / self.gaitCycleTime(subject)
		stepsPerMinute = float(stridesPerMinute)*2
		return stepsPerMinute

	def gaitCycleTime(self, subject='a1'):
		time = self.db.dataBySensor(self.db.data[subject])['Time']
		strides = self.db.segments[subject]
		duration = time[strides[-1]] - time[strides[0]]
		timePerStride = duration / (len(strides)-1)
		return float(timePerStride)		

	def dutyCycleOfSwing(self, subject='a1'):
		"""Percentage of time in swing phase"""
		left_cycles = self.__completeCyclesForOneLeg(subject=subject, side='left')
		right_cycles = self.__completeCyclesForOneLeg(subject=subject, side='right')

		for l in left_cycles:
			swingTime = l[1] - l[0] # Heel strike minus preceeding toe off
			cycleTime = l[2] - l[0] # Toe off minus preceeding toe off
			leftDuty = swingTime/float(cycleTime)*100
		for r in right_cycles:
			swingTime = r[1] - r[0] # Heel strike minus preceeding toe off
			cycleTime = r[2] - r[0] # Toe off minus preceeding toe off
			rightDuty = swingTime/float(cycleTime)*100

		return (leftDuty, rightDuty)

	def dutyCycleOfStance(self, subject='a1'):
		"""Percentage of time in stance phase"""
		left_cycles = self.__completeCyclesForOneLeg(subject=subject, side='left')
		right_cycles = self.__completeCyclesForOneLeg(subject=subject, side='right')

		for l in left_cycles:
			stanceTime = l[2] - l[1] # Toe off minus preceeding heel strike
			cycleTime = l[2] - l[0] # Toe off minus preceeding toe off
			leftDuty = stanceTime/float(cycleTime)*100
		for r in right_cycles:
			stanceTime = r[2] - r[1] # Toe off minus preceeding heel strike
			cycleTime = r[2] - r[0] # Toe off minus preceeding toe off
			rightDuty = stanceTime/float(cycleTime)*100

		return (leftDuty, rightDuty)

	def evennessOfSteps(self):
		pass

	def strideLength(self):
		pass

	def shankRangeOfMotion(self):
		pass

	def trunkRangeOfMotion(self):
		pass

	def strideVelocityAsymmetry(self):
		pass

	def swingAsymmetry(self):
		pass

	def stanceAsymmetry(self):
		pass

	def footAttitudeDuringSwing(self):
		pass

	def chestAttitudeDuringSwing(self):
		pass

	def chestAttitudeDuringStance(self):
		pass

	def __completeCyclesForOneLeg(self, subject='a1', side='left'):
		if side == 'left':
			segmentsFromLeg = [(s,c,c) for s,c in self.db.manual_gait_segments[subject] if c == 0 or c == 1]
		if side == 'right':
			segmentsFromLeg = [(s,c-2,c) for s,c in self.db.manual_gait_segments[subject] if c == 2 or c == 3]


		cycles = []
		cycle = []
		nextClassInCycle = 0

		for seg, segClass, origSegClass in segmentsFromLeg:
			if segClass == nextClassInCycle:
				cycle.append(seg)
				if len(cycle) == 3:
					cycles.append(cycle)
					cycle = [seg]
				nextClassInCycle = (nextClassInCycle + 1) % 2
			else:
				nextClassInCycle = 0
				cycle = []

		return cycles
