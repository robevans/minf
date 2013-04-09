__author__ = 'Robert Evans'

import master as m
import numpy as np
import quats
import pca
import plot
import progressbar
import random
import armExercisesDatabase
import parallelSimilarityMatrix

def armExercisesIndividualSimMatrix(db=None, subjectNumber=2):
	if db is None:
		db = armExercisesDatabase.db(True)
	LRclasses = {key:value for (key,value) in zip(db.LDsegs.keys(),[l[subjectNumber] for l in db.LDsegs.values()])}
	classes = {}
	for key,value in LRclasses.iteritems():
		for segment in value:
			classes.setdefault(key[:-1], []).append(segment) # Merge left and right hand motions together

	averageWeight = [float(sum(t))/len(t) for t in zip(*[[float(sum(t))/len(t) for t in zip(*l)] for l in db.explainedVariances.values()])]
	weights = {key:[averageWeight]*len(value) for key,value in classes.iteritems()}

	parallelSimilarityMatrix.averageSimilarityMatrix(classes, weights, "Subject C: PCA data distances", savePlot=True)

def armExercisesHDParallelsimMatrix(db=None):
	if db is None:
		db = armExercisesDatabase.db(True)
	LRclasses = {key:value for (key,value) in zip(db.HDsegs.keys(),[sum(l,[]) for l in db.HDsegs.values()])}
	classes = {}
	for key,value in LRclasses.iteritems():
		for segment in value:
			classes.setdefault(key[:-1], []).append(segment) # Merge left and right hand motions together
	weights = {key:[[1]*np.shape(segments[0])[1]]*len(segments) for (key,segments) in zip(classes.keys(),classes.values())}

	parallelSimilarityMatrix.averageSimilarityMatrix(classes, weights, "High Dimensional Arm Cluster Comparisons", savePlot=True)

def armExercisesLDParallelsimMatrix(db=None):
	if db is None:
		db = armExercisesDatabase.db(True)
	LRclasses = {key:value for (key,value) in zip(db.LDsegs.keys(),[sum(l,[]) for l in db.LDsegs.values()])}
	classes = {}
	for key,value in LRclasses.iteritems():
		for segment in value:
			classes.setdefault(key[:-1], []).append(segment) # Merge left and right hand motions together

	averageWeight = [float(sum(t))/len(t) for t in zip(*[[float(sum(t))/len(t) for t in zip(*l)] for l in db.explainedVariances.values()])]
	weights = {key:[averageWeight]*len(value) for key,value in classes.iteritems()}
	parallelSimilarityMatrix.averageSimilarityMatrix(classes, weights, "Arm Exercise Clusters - Low Dimensional Distances", savePlot=True)


def armExercisesHDsimMatrix(db=None):
	if db is None:
		db = armExercisesDatabase.db(True)
	LRclasses = {key:random.sample(value,1) for (key,value) in zip(db.HDsegs.keys(),[sum(l,[]) for l in db.HDsegs.values()])}
	classes = {}
	for key,value in LRclasses.iteritems():
		for segment in value:
			classes.setdefault(key[:-1], []).append(segment) # Merge left and right hand motions together
	weights = {key:[[1]*np.shape(segments[0])[1]]*len(segments) for (key,segments) in zip(classes.keys(),classes.values())}

	m.averageSimilarityMatrix(classes, weights, "Distances between clusters of exercises", savePlot=True)

def simMatrixAverageClassDistancesHighDimArmEx(db=None):
	if db is None:
		db = armExercisesDatabase.db(True)
	classes = {key:value[1] for (key,value) in zip(db.data,db.segs.values())}
	classes = {key[:-1]:classes[key] for key in classes.keys() if 'l' in key} # Left hand motions only
	weights = {key:[[1]*np.shape(segments[0])[1]]*len(segments) for (key,segments) in zip(classes.keys(),classes.values())}

	m.averageSimilarityMatrix(classes, weights, "Distances between clusters of exercises with left arm", savePlot=True)

def similarityMatrixForLowDimArmExercisesLeftHand(segmentsFromEach=1, database=None):
	if database is None:
		data=armExercisesDatabase.db(True)
	else:
		data = database

	segs10l=random.sample(data.segs['10l'][1],segmentsFromEach)
	segs20l=random.sample(data.segs['20l'][1],segmentsFromEach)
	segs30l=random.sample(data.segs['30l'][1],segmentsFromEach)
	segs40l=random.sample(data.segs['40l'][1],segmentsFromEach)
	segs50l=random.sample(data.segs['50l'][1],segmentsFromEach)
	segs60l=random.sample(data.segs['60l'][1],segmentsFromEach)
	segs70l=random.sample(data.segs['70l'][1],segmentsFromEach)
	segs80l=random.sample(data.segs['80l'][1],segmentsFromEach)
	segs90l=random.sample(data.segs['90l'][1],segmentsFromEach)

	names = ["10"]*segmentsFromEach+["20"]*segmentsFromEach+["30"]*segmentsFromEach+["40"]*segmentsFromEach+["50"]*segmentsFromEach+["60"]*segmentsFromEach+["70"]*segmentsFromEach+["80"]*segmentsFromEach+["90"]*segmentsFromEach
	weights = [float(sum(t))/float(len(t)) for t in zip(data.pca['10l'][1][1],data.pca['20l'][1][1],data.pca['30l'][1][1],data.pca['50l'][1][1],data.pca['60l'][1][1],data.pca['70l'][1][1],data.pca['80l'][1][1],data.pca['90l'][1][1])]

	print "Calculating similarities..."
	m.similarityMatrix(segs10l+segs20l+segs30l+segs40l+segs50l+segs60l+segs70l+segs80l+segs90l,names,weights,"Arm exercises, Low Dim",savePlot=True)

def similarityMatrixForExpandingCirclesHighDim():
	print "Reading data..."
	bar = progressbar.ProgressBar(maxval=12, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start(); progress = 0
	data0a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius0cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data5a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius5cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data10a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius10cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data15a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius15cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data20a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius20cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data25a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius25cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data0b=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius0cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data5b=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius5cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data10b=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius10cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data15b=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius15cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data20b=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius20cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data25b=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius25cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	bar.finish()

	print "Calculating segments..."
	bar = progressbar.ProgressBar(maxval=12, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start(); progress = 0
	segs0a=m.getHighDimensionalSegments(data0a); progress += 1; bar.update(progress)
	segs5a=m.getHighDimensionalSegments(data5a); progress += 1; bar.update(progress)
	segs10a=m.getHighDimensionalSegments(data10a); progress += 1; bar.update(progress)
	segs15a=m.getHighDimensionalSegments(data15a); progress += 1; bar.update(progress)
	segs20a=m.getHighDimensionalSegments(data20a)[:-1]; progress += 1; bar.update(progress)
	segs25a=m.getHighDimensionalSegments(data25a)[1:]; progress += 1; bar.update(progress)
	segs0b=m.getHighDimensionalSegments(data0b)[1:-1]; progress += 1; bar.update(progress)
	segs5b=m.getHighDimensionalSegments(data5b)[1:]; progress += 1; bar.update(progress)
	segs10b=m.getHighDimensionalSegments(data10b)[:-1]; progress += 1; bar.update(progress)
	segs15b=m.getHighDimensionalSegments(data15b)[1:-1]; progress += 1; bar.update(progress)
	segs20b=m.getHighDimensionalSegments(data20b)[1:-1]; progress += 1; bar.update(progress)
	segs25b=m.getHighDimensionalSegments(data25b)[1:-1]; progress += 1; bar.update(progress)
	bar.finish()

	names = ["0a"]*len(segs0a)+["5a"]*len(segs5a)+["10a"]*len(segs10a)+["15a"]*len(segs15a)+["20a"]*len(segs20a)+["25a"]*len(segs25a)+["0c"]*len(segs0b)+["5c"]*len(segs5b)+["10c"]*len(segs10b)+["15c"]*len(segs15b)+["20c"]*len(segs20b)+["25c"]*len(segs25b)
	#names = ["0a"]*len(segs0a)+["0c"]*len(segs0b)+["5a"]*len(segs5a)+["5c"]*len(segs5b)+["10a"]*len(segs10a)+["10c"]*len(segs10b)+["15a"]*len(segs15a)+["15c"]*len(segs15b)+["20a"]*len(segs20a)+["20c"]*len(segs20b)+["25a"]*len(segs25a)+["25c"]*len(segs25b)
	weights = [1]*np.shape((segs0a+segs0b+segs5a+segs5b+segs10a+segs10b+segs15a+segs15b+segs20a+segs20b+segs25a+segs25b)[0])[1]
	#names = [0]*len(segs0a)+[10]*len(segs10a)+[20]*len(segs20a)
	#weights = [1]*np.shape((segs0a+segs10a+segs20a)[0])[1]

	print "Calculating similarities..."
	m.similarityMatrix(segs0a+segs5a+segs10a+segs15a+segs20a+segs25a+segs0b+segs5b+segs10b+segs15b+segs20b+segs25b,names,weights,"Similarity Matrix using high dimensional raw sensor data",savePlot=True)
	#m.similarityMatrix(segs0a+segs0b+segs5a+segs5b+segs10a+segs10b+segs15a+segs15b+segs20a+segs20b+segs25a+segs25b,names,weights,"Similarity Matrix using high dimensional raw sensor data",savePlot=True)
	#m.similarityMatrix(segs0a+segs5a+segs10a+segs15a+segs20a+segs25a,names,weights,"Similarity Matrix using high dimensional raw sensor data",savePlot=True)
	#m.similarityMatrix(segs0a+segs10a+segs20a,names,weights,"Similarity Matrix using high dimensional raw sensor data",savePlot=True)

def similarityMatrixForExpandingCirclesLowDim():
	print "Reading data..."
	bar = progressbar.ProgressBar(maxval=12, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start(); progress = 0
	data0a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius0cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data5a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius5cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data10a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius10cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data15a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius15cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data20a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius20cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data25a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius25cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data0b=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius0cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data5b=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius5cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data10b=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius10cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data15b=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius15cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data20b=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius20cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	data25b=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius25cmHorizontal.txt")[26:,4:]; progress += 1; bar.update(progress)
	bar.finish()

	print "Calculating segments..."
	bar = progressbar.ProgressBar(maxval=12, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start(); progress = 0
	(segs0a,wa0)=m.getLowDimensionalSegments(data0a,n_components=2); progress += 1; bar.update(progress)
	(segs5a,wa5)=m.getLowDimensionalSegments(data5a,n_components=2); progress += 1; bar.update(progress)
	(segs10a,wa10)=m.getLowDimensionalSegments(data10a,n_components=2); progress += 1; bar.update(progress)
	(segs15a,wa15)=m.getLowDimensionalSegments(data15a,n_components=2); progress += 1; bar.update(progress)
	(segs20a,wa20)=m.getLowDimensionalSegments(data20a,n_components=2); progress += 1; bar.update(progress)
	(segs25a,wa25)=m.getLowDimensionalSegments(data25a,n_components=2); progress += 1; bar.update(progress)
	(segs0b,wb0)=m.getLowDimensionalSegments(data0b,n_components=2); progress += 1; bar.update(progress)
	(segs5b,wb5)=m.getLowDimensionalSegments(data5b,n_components=2); progress += 1; bar.update(progress)
	(segs10b,wb10)=m.getLowDimensionalSegments(data10b,n_components=2); progress += 1; bar.update(progress)
	(segs15b,wb15)=m.getLowDimensionalSegments(data15b,n_components=2); progress += 1; bar.update(progress)
	(segs20b,wb20)=m.getLowDimensionalSegments(data20b,n_components=2); progress += 1; bar.update(progress)
	(segs25b,wb25)=m.getLowDimensionalSegments(data25b,n_components=2); progress += 1; bar.update(progress)
	segs20a=segs20a[:-1]
	segs25a=segs25a[1:]
	segs0b=segs0b[1:-1]
	segs5b=segs5b[1:]
	segs10b=segs10b[:-1]
	segs15b=segs15b[1:-1]
	segs20b=segs20b[1:-1]
	segs25b=segs25b[1:-1]
	names = ["0a"]*len(segs0a)+["5a"]*len(segs5a)+["10a"]*len(segs10a)+["15a"]*len(segs15a)+["20a"]*len(segs20a)+["25a"]*len(segs25a)+["0c"]*len(segs0b)+["5c"]*len(segs5b)+["10c"]*len(segs10b)+["15c"]*len(segs15b)+["20c"]*len(segs20b)+["25c"]*len(segs25b)
	weights = [float(sum(t))/float(len(t)) for t in zip(wa0,wa5,wa10,wa15,wa20,wa25,wb0,wb5,wb10,wb15,wb20,wb25)]
	bar.finish()

	print "Calculating similarities..."
	m.similarityMatrix(segs0a+segs5a+segs10a+segs15a+segs20a+segs25a+segs0b+segs5b+segs10b+segs15b+segs20b+segs25b,names,weights,"Similarity Matrix using two principal components",savePlot=True)

def highDimRawSimilarity():
	raw_h_large=m.getHighDimensionalSegments(m.readCSVfile("captures/HorizontalArmSpin-Jibran.csv"))
	raw_h_small=m.getHighDimensionalSegments(m.readCSVfile("captures/HorizontalArmSpinLittleCircles-Jibran.csv"))
	names = ['Big','Big','Big','Big','Big','Big','Big','Small','Small','Small','Small','Small','Small','Small','Small','Small']
	weights = [1]*np.shape((raw_h_large+raw_h_small)[0])[1]
	m.similarityMatrix(raw_h_large+raw_h_small,names,weights,"Similarity Matrix using high dimensional raw sensor data")

def highDimQuaternionSimilarity(euler=False):
	quats_h_large=m.getQuaternionSegmentsByRawData(m.readCSVfile("captures/HorizontalArmSpin-Jibran.csv"),quats.rearrangeQuatsForLatentSpaceAlgorithm(quats.rawDataFileToQuats("captures/raw/HorizontalArmSpin-Jibran"),euler))
	quats_h_small=m.getQuaternionSegmentsByRawData(m.readCSVfile("captures/HorizontalArmSpinLittleCircles-Jibran.csv"),quats.rearrangeQuatsForLatentSpaceAlgorithm(quats.rawDataFileToQuats("captures/raw/HorizontalArmSpinLittleCircles-Jibran"),euler))
	names = ['Big','Big','Big','Big','Big','Big','Big','Small','Small','Small','Small','Small','Small','Small','Small','Small']
	weights = [1]*np.shape((quats_h_large+quats_h_small)[0])[1]
	if euler:
		title="Similarity Matrix using high dimensional euler angle data"
	else:
		title="Similarity Matrix using high dimensional quaternion data"
	m.similarityMatrix(quats_h_large+quats_h_small,names,weights,"Similarity Matrix using high dimensional euler angle data")

def lowDimQuaternionSimilarity(n_components=3,euler=False):
	(quats_h_large,weights_large)=quats.doPCAonQuats("captures/raw/HorizontalArmSpin-Jibran",euler,n_components=n_components)
	(quats_h_small,weights_small)=quats.doPCAonQuats("captures/raw/HorizontalArmSpinLittleCircles-Jibran",euler,n_components=n_components)
	segments_quats_h_large=m.getQuaternionSegmentsByRawData(m.readCSVfile("captures/HorizontalArmSpin-Jibran.csv"),quats_h_large)
	segments_quats_h_small=m.getQuaternionSegmentsByRawData(m.readCSVfile("captures/HorizontalArmSpinLittleCircles-Jibran.csv"),quats_h_small)
	names = ['Big','Big','Big','Big','Big','Big','Big','Small','Small','Small','Small','Small','Small','Small','Small','Small']
	weights = [1]*np.shape((segments_quats_h_large+segments_quats_h_small)[0])[1] #TODO:  AVERAGE THE WEIGHTS!!
	if euler:
		title="Similarity Matrix using low dimensional euler angle data"
	else:
		title="Similarity Matrix using low dimensional quaternion data"
	m.similarityMatrix(segments_quats_h_large+segments_quats_h_small,names,weights,title)

def lowDimRawSimilarity(n_components=3):
	(raw_h_large,weights_large)=m.getLowDimensionalSegments(m.readCSVfile("captures/HorizontalArmSpin-Jibran.csv"),n_components)
	(raw_h_small,weights_small)=m.getLowDimensionalSegments(m.readCSVfile("captures/HorizontalArmSpinLittleCircles-Jibran.csv"),n_components)
	names = ['Big','Big','Big','Big','Big','Big','Big','Small','Small','Small','Small','Small','Small','Small','Small','Small']
	averageWeights = [(a+b)/2.0 for (a,b) in zip(weights_large,weights_small)]
	m.similarityMatrix(raw_h_large+raw_h_small,names,averageWeights,"Similarity Matrix using raw sensor data projected to the latent space")

def allMotionslowDimRawSimilarity(n_components=3,savePlot=False,title="Similarity matrix"):
	# Load files and get segments
	(raw_v1,weights_v1)=m.getLowDimensionalSegments(m.readCSVfile("captures/VerticalArmSpin-Dan.csv"),n_components)
	(raw_v2,weights_v2)=m.getLowDimensionalSegments(m.readCSVfile("captures/VerticalArmSpin-Jibran.csv"),n_components)
	(raw_h1,weights_h1)=m.getLowDimensionalSegments(m.readCSVfile("captures/HorizontalArmSpin-Dan.csv"),n_components)
	(raw_h2,weights_h2)=m.getLowDimensionalSegments(m.readCSVfile("captures/HorizontalArmSpin-Jibran.csv"),n_components)
	(raw_h3,weights_h3)=m.getLowDimensionalSegments(m.readCSVfile("captures/HorizontalArmSpinLittleCircles-Jibran.csv"),n_components)
	# Discard bad segments
	raw_h1 = raw_h1[4:]
	raw_v2 = raw_v2[1:5]
	# Make name labels
	namesV1 = ["V1"]*len(raw_v1)
	namesV2 = ["V2"]*len(raw_v2)
	namesH1 = ["H1"]*len(raw_h1)
	namesH2 = ["H2"]*len(raw_h2)
	namesH3 = ["H3"]*len(raw_h3)
	names = namesV1+namesV2+namesH1+namesH2+namesH3
	# Calculate average weights
	averageWeights = [(a+b+c+d+e)/5.0 for (a,b,c,d,e) in zip(weights_v1,weights_v2,weights_h1,weights_h2,weights_h3)]
	# Crunch similarity matrix
	m.similarityMatrix(raw_v1+raw_v2+raw_h1+raw_h2+raw_h3,names,averageWeights,title,savePlot)

def plotPCA3d(filename):
	(lowDims,v)=pca.pcaFromFile(filename,n_components=2)
	title = "".join(filename.split('/')[-1].split('.')[:-1])
	plot.plotPCA3D(lowDims,title)

def plotSegments():
	m.getLowDimensionalSegments(m.readCSVfile("captures/HorizontalArmSpin-Jibran.csv"),n_components=1,plt=True,title="Large horizontal arm spin segments")
	m.getLowDimensionalSegments(m.readCSVfile("captures/HorizontalArmSpinLittleCircles-Jibran.csv"),n_components=1,plt=True,title="Small horizontal arm spin segments")