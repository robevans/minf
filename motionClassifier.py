__author__ = 'Robert Evans'
import armExercisesDatabase
import progressbar
import master as m
import dtw
import random

class KNNclassifier:
	def __init__(self, database, k=3):
			self.data = database
			self.k = k

	def classify(self, query, HDorLD='HD'):
		l=[]
		if HDorLD == 'HD':
			for key,value in self.data.HDtraining.iteritems():
				for reference in value:
					l.append((key,dtw.dist(query,reference))) # Get HD distances to neighbours
		if HDorLD == 'LD':
			for key,value in self.data.LDtraining.iteritems():
				for reference in value:
					#l.append((key,dtw.getDTWdist2DweightedSum(query,reference,self.data.averageWeights))) # Slow, weighted multi-dim DTW
					l.append((key,dtw.dist(query,reference))) # faster multi-dim distance without weights

		sl = sorted(l,key=lambda x:x[1]) # Sort neighbours by distance
		L = sl[:self.k] # Take the nearest k neighbours
		
		# Count the number of instances of each class among the k nearest neighbours
		classCountsWithSums = {}
		for (cl,dist) in L:
			if cl not in classCountsWithSums:
				classCountsWithSums[cl] = (1,dist,cl)
			else:
				classCountsWithSums[cl] = (classCountsWithSums[cl][0] + 1, classCountsWithSums[cl][1] + dist, cl)

		sizeOfLargestGroup = max([c for (c,_,_) in classCountsWithSums.values()]) # There may be a tie

		# Break any tie by using the group which is closer on average
		largestGroupWithSmallestDistance = min( [(d,cl) for (c,d,cl) in classCountsWithSums.values() if c == sizeOfLargestGroup] )

		return largestGroupWithSmallestDistance[1] # Return the name of the most common neighbour

def testKNNClassifier(dataClass, classifierClass, split=0.5, k=3, HDorLD='HD'):
	db = dataClass(split)
	cl = classifierClass(db, k)
	print "Classifying test data..."

	if HDorLD == 'HD':
		bar = progressbar.ProgressBar(maxval=sum(map(len,cl.data.HDtest.values())), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		bar.start()
		progress = 0
		correct = 0
		for k,i in cl.data.HDtest.iteritems():
				for r in i:
						classification = cl.classify(r, HDorLD='HD')
						print k,classification
						progress += 1
						bar.update(progress)
						if k == classification:
							correct+=1
		bar.finish()
		print "%.1f%% correct"%(float(correct)/sum(map(len,cl.data.HDtest.values()))*100)

	if HDorLD == 'LD':
		bar = progressbar.ProgressBar(maxval=sum(map(len,cl.data.LDtest.values())), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		bar.start()
		progress = 0
		correct = 0
		for k,i in cl.data.LDtest.iteritems():
				for r in i:
						classification = cl.classify(r, HDorLD='LD')
						print k,classification
						progress += 1
						bar.update(progress)
						if k == classification:
							correct+=1
		bar.finish()
		print "%.1f%% correct"%(float(correct)/sum(map(len,cl.data.LDtest.values()))*100)

class armExercisesData:
	def __init__(self, split=0.5):
		data = armExercisesDatabase.db(True)

		# High dimensional data
		LRclasses = {key:value for (key,value) in zip(data.HDsegs.keys(),[sum(l,[]) for l in data.HDsegs.values()])}
		classes = {}
		for key,value in LRclasses.iteritems():
			for segment in value:
				classes.setdefault(key[:-1], []).append(segment)
		for segments in classes.values():
			random.shuffle(segments)
		self.HDtraining = {'10 degrees':classes['10'][:(int(len(classes['10'])*split))],
						   '20 degrees':classes['20'][:(int(len(classes['20'])*split))],
						   '30 degrees':classes['30'][:(int(len(classes['30'])*split))],
						   '40 degrees':classes['40'][:(int(len(classes['40'])*split))],
						   '50 degrees':classes['50'][:(int(len(classes['50'])*split))],
						   '60 degrees':classes['60'][:(int(len(classes['60'])*split))],
						   '70 degrees':classes['70'][:(int(len(classes['70'])*split))],
						   '80 degrees':classes['80'][:(int(len(classes['80'])*split))],
						   '90 degrees':classes['90'][:(int(len(classes['90'])*split))]}
		self.HDtest = {'10 degrees':classes['10'][(int(len(classes['10'])*split)):],
					   '20 degrees':classes['20'][(int(len(classes['20'])*split)):],
					   '30 degrees':classes['30'][(int(len(classes['30'])*split)):],
					   '40 degrees':classes['40'][(int(len(classes['40'])*split)):],
					   '50 degrees':classes['50'][(int(len(classes['50'])*split)):],
					   '60 degrees':classes['60'][(int(len(classes['60'])*split)):],
					   '70 degrees':classes['70'][(int(len(classes['70'])*split)):],
					   '80 degrees':classes['80'][(int(len(classes['80'])*split)):],
					   '90 degrees':classes['90'][(int(len(classes['90'])*split)):]}

		# Low dimensional data
		LRclasses = {key:value for (key,value) in zip(data.LDsegs.keys(),[sum(l,[]) for l in data.LDsegs.values()])}
		classes = {}
		for key,value in LRclasses.iteritems():
			for segment in value:
				classes.setdefault(key[:-1], []).append(segment)
		for segments in classes.values():
			random.shuffle(segments)
		self.LDtraining = {'10 degrees':classes['10'][:(int(len(classes['10'])*split))],
						   '20 degrees':classes['20'][:(int(len(classes['20'])*split))],
						   '30 degrees':classes['30'][:(int(len(classes['30'])*split))],
						   '40 degrees':classes['40'][:(int(len(classes['40'])*split))],
						   '50 degrees':classes['50'][:(int(len(classes['50'])*split))],
						   '60 degrees':classes['60'][:(int(len(classes['60'])*split))],
						   '70 degrees':classes['70'][:(int(len(classes['70'])*split))],
						   '80 degrees':classes['80'][:(int(len(classes['80'])*split))],
						   '90 degrees':classes['90'][:(int(len(classes['90'])*split))]}
		self.LDtest = {'10 degrees':classes['10'][(int(len(classes['10'])*split)):],
					   '20 degrees':classes['20'][(int(len(classes['20'])*split)):],
					   '30 degrees':classes['30'][(int(len(classes['30'])*split)):],
					   '40 degrees':classes['40'][(int(len(classes['40'])*split)):],
					   '50 degrees':classes['50'][(int(len(classes['50'])*split)):],
					   '60 degrees':classes['60'][(int(len(classes['60'])*split)):],
					   '70 degrees':classes['70'][(int(len(classes['70'])*split)):],
					   '80 degrees':classes['80'][(int(len(classes['80'])*split)):],
					   '90 degrees':classes['90'][(int(len(classes['90'])*split)):]}
		self.averageWeights = data.averageExplainedVariance

class circlesData:
	def __init__(self, split=0.5):
		print "Initialising reference data..."
		bar = progressbar.ProgressBar(maxval=14, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		bar.start(); progress = 0
		self.data0a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius0cmHorizontal.txt")[26:,4:]
		self.data5a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius5cmHorizontal.txt")[26:,4:]
		self.data10a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius10cmHorizontal.txt")[26:,4:]
		self.data15a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius15cmHorizontal.txt")[26:,4:]
		self.data20a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius20cmHorizontal.txt")[26:,4:]
		self.data25a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius25cmHorizontal.txt")[26:,4:]
		self.data0c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius0cmHorizontal.txt")[26:,4:]
		self.data5c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius5cmHorizontal.txt")[26:,4:]
		self.data10c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius10cmHorizontal.txt")[26:,4:]
		self.data15c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius15cmHorizontal.txt")[26:,4:]
		self.data20c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius20cmHorizontal.txt")[26:,4:]
		self.data25c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius25cmHorizontal.txt")[26:,4:]
		progress += 1; bar.update(progress)

		(self.HDsegs0a,self.LDsegs0a,self.w0a) = m.getHighAndLowDimSegments(self.data0a, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs5a,self.LDsegs5a,self.w5a) = m.getHighAndLowDimSegments(self.data5a, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs10a,self.LDsegs10a,self.w10a) = m.getHighAndLowDimSegments(self.data10a, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs15a,self.LDsegs15a,self.w15a) = m.getHighAndLowDimSegments(self.data15a, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs20a,self.LDsegs20a,self.w20a) = m.getHighAndLowDimSegments(self.data20a, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs25a,self.LDsegs25a,self.w25a) = m.getHighAndLowDimSegments(self.data25a, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs0c,self.LDsegs0c,self.w0c) = m.getHighAndLowDimSegments(self.data0c, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs5c,self.LDsegs5c,self.w5c) = m.getHighAndLowDimSegments(self.data5c, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs10c,self.LDsegs10c,self.w10c) = m.getHighAndLowDimSegments(self.data10c, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs15c,self.LDsegs15c,self.w15c) = m.getHighAndLowDimSegments(self.data15c, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs20c,self.LDsegs20c,self.w20c) = m.getHighAndLowDimSegments(self.data20c, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs25c,self.LDsegs25c,self.w25c) = m.getHighAndLowDimSegments(self.data25c, n_components=9); progress += 1; bar.update(progress)
		
		self.averageWeights = [float(sum(t))/float(len(t)) for t in zip(self.w0a,self.w5a,self.w10a,self.w15a,self.w20a,self.w25a,self.w0c,self.w5c,self.w10c,self.w15c,self.w20c,self.w25c)]

		self.HDsegs20a=self.HDsegs20a[:-1]
		self.HDsegs25a=self.HDsegs25a[1:]
		self.HDsegs0c=self.HDsegs0c[1:-1]
		self.HDsegs5c=self.HDsegs5c[1:]
		self.HDsegs10c=self.HDsegs10c[:-1]
		self.HDsegs15c=self.HDsegs15c[1:-1]
		self.HDsegs20c=self.HDsegs20c[1:-1]
		self.HDsegs25c=self.HDsegs25c[1:-1]
		self.LDsegs20a=self.LDsegs20a[:-1]
		self.LDsegs25a=self.LDsegs25a[1:]
		self.LDsegs0c=self.LDsegs0c[1:-1]
		self.LDsegs5c=self.LDsegs5c[1:]
		self.LDsegs10c=self.LDsegs10c[:-1]
		self.LDsegs15c=self.LDsegs15c[1:-1]
		self.LDsegs20c=self.LDsegs20c[1:-1]
		self.LDsegs25c=self.LDsegs25c[1:-1]

		self.HDtraining = {'Anticlockwise radius=0cm':self.HDsegs0a[:(int(len(self.HDsegs0a)*split))],
							'Anticlockwise radius=5cm':self.HDsegs5a[:(int(len(self.HDsegs5a)*split))],
							'Anticlockwise radius=10cm':self.HDsegs10a[:(int(len(self.HDsegs10a)*split))],
							'Anticlockwise radius=15cm':self.HDsegs15a[:(int(len(self.HDsegs15a)*split))],
							'Anticlockwise radius=20cm':self.HDsegs20a[:(int(len(self.HDsegs20a)*split))],
							'Anticlockwise radius=25cm':self.HDsegs25a[:(int(len(self.HDsegs25a)*split))],
							'Anticlockwise radius=0cm':self.HDsegs0a[:(int(len(self.HDsegs0a)*split))],
							'Clockwise radius=5cm':self.HDsegs5c[:(int(len(self.HDsegs5c)*split))],
							'Clockwise radius=10cm':self.HDsegs10c[:(int(len(self.HDsegs10c)*split))],
							'Clockwise radius=15cm':self.HDsegs15c[:(int(len(self.HDsegs15c)*split))],
							'Clockwise radius=20cm':self.HDsegs20c[:(int(len(self.HDsegs20c)*split))],
							'Clockwise radius=25cm':self.HDsegs25c[:(int(len(self.HDsegs25c)*split))]}
		self.LDtraining = {'Anticlockwise radius=0cm':self.LDsegs0a[:(int(len(self.LDsegs0a)*split))],
							'Anticlockwise radius=5cm':self.LDsegs5a[:(int(len(self.LDsegs5a)*split))],
							'Anticlockwise radius=10cm':self.LDsegs10a[:(int(len(self.LDsegs10a)*split))],
							'Anticlockwise radius=15cm':self.LDsegs15a[:(int(len(self.LDsegs15a)*split))],
							'Anticlockwise radius=20cm':self.LDsegs20a[:(int(len(self.LDsegs20a)*split))],
							'Anticlockwise radius=25cm':self.LDsegs25a[:(int(len(self.LDsegs25a)*split))],
							'Anticlockwise radius=0cm':self.LDsegs0a[:(int(len(self.LDsegs0a)*split))],
							'Clockwise radius=5cm':self.LDsegs5c[:(int(len(self.LDsegs5c)*split))],
							'Clockwise radius=10cm':self.LDsegs10c[:(int(len(self.LDsegs10c)*split))],
							'Clockwise radius=15cm':self.LDsegs15c[:(int(len(self.LDsegs15c)*split))],
							'Clockwise radius=20cm':self.LDsegs20c[:(int(len(self.LDsegs20c)*split))],
							'Clockwise radius=25cm':self.LDsegs25c[:(int(len(self.LDsegs25c)*split))]}

		self.HDtest = {'Anticlockwise radius=0cm':self.HDsegs0a[(int(len(self.HDsegs0a)*split)):],
							'Anticlockwise radius=5cm':self.HDsegs5a[(int(len(self.HDsegs5a)*split)):],
							'Anticlockwise radius=10cm':self.HDsegs10a[(int(len(self.HDsegs10a)*split)):],
							'Anticlockwise radius=15cm':self.HDsegs15a[(int(len(self.HDsegs15a)*split)):],
							'Anticlockwise radius=20cm':self.HDsegs20a[(int(len(self.HDsegs20a)*split)):],
							'Anticlockwise radius=25cm':self.HDsegs25a[(int(len(self.HDsegs25a)*split)):],
							'Anticlockwise radius=0cm':self.HDsegs0a[(int(len(self.HDsegs0a)*split)):],
							'Clockwise radius=5cm':self.HDsegs5c[(int(len(self.HDsegs5c)*split)):],
							'Clockwise radius=10cm':self.HDsegs10c[(int(len(self.HDsegs10c)*split)):],
							'Clockwise radius=15cm':self.HDsegs15c[(int(len(self.HDsegs15c)*split)):],
							'Clockwise radius=20cm':self.HDsegs20c[(int(len(self.HDsegs20c)*split)):],
							'Clockwise radius=25cm':self.HDsegs25c[(int(len(self.HDsegs25c)*split)):]}
		self.LDtest = {'Anticlockwise radius=0cm':self.LDsegs0a[(int(len(self.LDsegs0a)*split)):],
							'Anticlockwise radius=5cm':self.LDsegs5a[(int(len(self.LDsegs5a)*split)):],
							'Anticlockwise radius=10cm':self.LDsegs10a[(int(len(self.LDsegs10a)*split)):],
							'Anticlockwise radius=15cm':self.LDsegs15a[(int(len(self.LDsegs15a)*split)):],
							'Anticlockwise radius=20cm':self.LDsegs20a[(int(len(self.LDsegs20a)*split)):],
							'Anticlockwise radius=25cm':self.LDsegs25a[(int(len(self.LDsegs25a)*split)):],
							'Anticlockwise radius=0cm':self.LDsegs0a[(int(len(self.LDsegs0a)*split)):],
							'Clockwise radius=5cm':self.LDsegs5c[(int(len(self.LDsegs5c)*split)):],
							'Clockwise radius=10cm':self.LDsegs10c[(int(len(self.LDsegs10c)*split)):],
							'Clockwise radius=15cm':self.LDsegs15c[(int(len(self.LDsegs15c)*split)):],
							'Clockwise radius=20cm':self.LDsegs20c[(int(len(self.LDsegs20c)*split)):],
							'Clockwise radius=25cm':self.LDsegs25c[(int(len(self.LDsegs25c)*split)):]}

		progress += 1; bar.update(progress)
		bar.finish()

class armCirclesData:
	def __init__(self, split=0.5, pca_dims=3):
		print "Initialising reference data..."
		bar = progressbar.ProgressBar(maxval=7, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		bar.start(); progress = 0

		self.__data_V0=m.readCSVfile("captures/VerticalArmSpin-Dan.csv")
		self.__data_V1=m.readCSVfile("captures/VerticalArmSpin-Jibran.csv")
		self.__data_H0=m.readCSVfile("captures/HorizontalArmSpin-Dan.csv")
		self.__data_H1=m.readCSVfile("captures/HorizontalArmSpin-Jibran.csv")
		self.__data_H2=m.readCSVfile("captures/HorizontalArmSpinLittleCircles-Jibran.csv")
		progress += 1; bar.update(progress)

		(self.__HDsegs_V0,self.__LDsegs_V0,_) = m.getHighAndLowDimSegments(self.__data_V0, n_components=pca_dims, smoothingWindow=15); progress += 1; bar.update(progress)
		(self.__HDsegs_V1,self.__LDsegs_V1,_) = m.getHighAndLowDimSegments(self.__data_V1, n_components=pca_dims, smoothingWindow=25); progress += 1; bar.update(progress)
		(self.__HDsegs_H0,self.__LDsegs_H0,_) = m.getHighAndLowDimSegments(self.__data_H0, n_components=pca_dims, smoothingWindow=20); progress += 1; bar.update(progress)
		(self.__HDsegs_H1,self.__LDsegs_H1,_) = m.getHighAndLowDimSegments(self.__data_H1, n_components=pca_dims, smoothingWindow=20); progress += 1; bar.update(progress)
		(self.__HDsegs_H2,self.__LDsegs_H2,_) = m.getHighAndLowDimSegments(self.__data_H2, n_components=pca_dims, smoothingWindow=15); progress += 1; bar.update(progress)

		self.HDtraining = {'VerticalArmSpin - Dan':self.__HDsegs_V0[:(int(len(self.__HDsegs_V0)*split))],
							'VerticalArmSpin - Jibran':self.__HDsegs_V1[:(int(len(self.__HDsegs_V1)*split))],
							'HorizontalArmSpin - Dan':self.__HDsegs_H0[:(int(len(self.__HDsegs_H0)*split))],
							'HorizontalArmSpin - Jibran':self.__HDsegs_H1[:(int(len(self.__HDsegs_H1)*split))],
							'HorizontalArmSpin - Small - Jibran':self.__HDsegs_H2[:(int(len(self.__HDsegs_H2)*split))]}
		self.LDtraining = {'VerticalArmSpin - Dan':self.__LDsegs_V0[:(int(len(self.__LDsegs_V0)*split))],
							'VerticalArmSpin - Jibran':self.__LDsegs_V1[:(int(len(self.__LDsegs_V1)*split))],
							'HorizontalArmSpin - Dan':self.__LDsegs_H0[:(int(len(self.__LDsegs_H0)*split))],
							'HorizontalArmSpin - Jibran':self.__LDsegs_H1[:(int(len(self.__LDsegs_H1)*split))],
							'HorizontalArmSpin - Small - Jibran':self.__LDsegs_H2[:(int(len(self.__LDsegs_H2)*split))]}

		self.HDtest = {'VerticalArmSpin - Dan':self.__HDsegs_V0[(int(len(self.__HDsegs_V0)*split)):],
							'VerticalArmSpin - Jibran':self.__HDsegs_V1[(int(len(self.__HDsegs_V1)*split)):],
							'HorizontalArmSpin - Dan':self.__HDsegs_H0[(int(len(self.__HDsegs_H0)*split)):],
							'HorizontalArmSpin - Jibran':self.__HDsegs_H1[(int(len(self.__HDsegs_H1)*split)):],
							'HorizontalArmSpin - Small - Jibran':self.__HDsegs_H2[(int(len(self.__HDsegs_H2)*split)):]}
		self.LDtest = {'VerticalArmSpin - Dan':self.__LDsegs_V0[(int(len(self.__LDsegs_V0)*split)):],
							'VerticalArmSpin - Jibran':self.__LDsegs_V1[(int(len(self.__LDsegs_V1)*split)):],
							'HorizontalArmSpin - Dan':self.__LDsegs_H0[(int(len(self.__LDsegs_H0)*split)):],
							'HorizontalArmSpin - Jibran':self.__LDsegs_H1[(int(len(self.__LDsegs_H1)*split)):],
							'HorizontalArmSpin - Small - Jibran':self.__LDsegs_H2[(int(len(self.__LDsegs_H2)*split)):]}

		progress += 1; bar.update(progress)
		bar.finish()