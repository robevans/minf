__author__ = 'Robert Evans'

import master as m
import numpy as np
import quats
import pca
import plot

def plotPCA3d(filename):
	(lowDims,v)=pca.pcaFromFile(filename,n_components=2)
	title = "".join(filename.split('/')[-1].split('.')[:-1])
	plot.plotPCA3D(lowDims,title)

def plotSegments():
	m.getLowDimensionalSegments(m.readCSVfile("captures/HorizontalArmSpin-Jibran.csv"),n_components=1,plt=True,title="Large horizontal arm spin segments")
	m.getLowDimensionalSegments(m.readCSVfile("captures/HorizontalArmSpinLittleCircles-Jibran.csv"),n_components=1,plt=True,title="Small horizontal arm spin segments")

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
	weights = [1]*np.shape((segments_quats_h_large+segments_quats_h_small)[0])[1]
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