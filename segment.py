__author__ = 'Robert Evans'

import numpy as np
import mins_and_maxs as mm
import smooth as sm
import pylab as pl
from readRaw import readRaw
from pca import pca
from rpy2.robjects import r
from rpy2.robjects.packages import importr
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
#from rpy2 import robjects
#R = rpy2.robjects.r
DTW = importr('dtw')

def manuallySegment(inputFile, listOfSegmentationPoints, outputFilesPrefix):
	data = readRaw(inputFile)[:,4:]
	pcaData = pca(data,3)[0]
	segments = np.split(data,listOfSegmentationPoints)
	pcaSegments = np.split(pcaData,listOfSegmentationPoints)
	for i,seg,pcaSeg in zip(range(len(segments)),segments, pcaSegments):
		np.savetxt("%s%i%s"%(outputFilesPrefix,i,"RAW.txt"),seg, delimiter=",")
		np.savetxt("%s%i%s"%(outputFilesPrefix,i,"PCA.txt"),pcaSeg, delimiter=",")

def segmentAndPlot(X, xIsFilename=False, smoothingWindow=100, smoothing='blackman', title='Automatic Segmentation', save=False):
	if xIsFilename == True:
		with open(X,'r') as fin:
			X = np.loadtxt(fin,delimiter=",")

	(mins,maxs) = segmentationPoints(X, windowSize=smoothingWindow)
	pl.figure(figsize=(11,9))
	pl.plot(X)
	for m in mins:
		pl.axvline(m,color='g',linewidth=1.5)
	for m in maxs:
		pl.axvline(m,color='r',linewidth=1.5)

	pl.xlabel('Time (frames)')
	pl.ylabel('Latent co-ordinate')
	pl.title(title)
	#pl.legend((''))

	if save:
		pl.savefig(('/Users/robertevans/Desktop/Accelerometer Segments/'+title+'.pdf'), format='pdf')
	else:
		pl.show()

def plotSegPoints(data, segPoints, xs=None):
	pl.figure(figsize=(11,9))
	if xs==None:
		pl.plot(data)
	else:
		pl.plot(xs,data)
	for sp in segPoints:
		pl.axvline(sp,color='black',linewidth=2)
	"""
	pl.title("Automatic Gait Segmentation")
	pl.xlabel("Time (Seconds)")
	pl.ylabel("Rotation (Degrees per second)")
	"""
	pl.show()

def yCrossingSegPoints(data, yThresh=0, xBetweenSegs=1, yBetweenSegs=1):
	prev = data[0]
	segPoints = []
	canSegment = True
	candidate = None
	for i,d in enumerate(data):
		if len(segPoints) > 0 and abs(d-data[segPoints[-1]]) >= yBetweenSegs/2.0:
			canSegment = True
			if candidate and abs(candidate[0]-segPoints[-1]) >= xBetweenSegs:
				pass;#segPoints += candidate
		if np.signbit(prev-yThresh) != np.signbit(d-yThresh):
			candidate = [i]
			if canSegment and (len(segPoints) == 0 or abs(candidate[0]-segPoints[-1]) >= xBetweenSegs):
				segPoints += candidate
				canSegment = False
		prev = d
	return segPoints

def segmentAndSave(X, useData="useX", xIsFilename=False, segmentBy="maxs",trimFrom=None,trimTo=float('inf'),filePrefix="./segments/V",fileSuffix=".csv",smoothingWindow=100):
	if xIsFilename == True:
		with open(X,'r') as fin:
			X = np.loadtxt(fin,delimiter=",")

	if useData == "useX":
		(mins,maxs) = segmentationPoints(X, windowSize=smoothingWindow)
		if segmentBy == "maxs":
			segPoints=[m for m in maxs if m>=trimFrom and m<=trimTo]
		if segmentBy == "mins":
			segPoints=[m for m in mins if m>=trimFrom and m<=trimTo]
	else:
		segPoints=[p for p in segmentationPoints if p>=trimFrom and p<=trimTo]
	
	segments=np.split(X,segPoints)
	i=0
	for seg in segments:
		np.savetxt("%s%i%s"%(filePrefix,i,fileSuffix),seg, delimiter=",")
		i+=1
		print segments

def segmentationPoints(X, xIsFilename=False, windowSize=100, smoothing='blackman'):
	if xIsFilename == True:
		with open(X,'r') as fin:
			X = np.loadtxt(fin,delimiter=",")
	

	smoothX = sm.smooth(X,window_len=windowSize,window=smoothing)
	#(unsmoothedMins,unsmoothedMaxs) = mm.find_mins_and_maxs1D(X)
	(smoothedMins,smoothedMaxs) = mm.find_mins_and_maxs1D(smoothX)
	# Using Dynamic Time Warping to map the smoothed curve onto the original, noisy curve.
	alignmentOfSmoothedCurveAndOriginal = r.dtw(smoothX, X)
	warpIndexes=r.warp(alignmentOfSmoothedCurveAndOriginal,True)
	#pl.plot(warpIndexes,smoothX)
	#pl.plot(X)
	#pl.show()

	minsMappedToOriginal = sorted(list(set([warpIndexes[smoothedMins[i]] for i in range(len(smoothedMins))])))
	maxsMappedToOriginal = sorted(list(set([warpIndexes[smoothedMaxs[i]] for i in range(len(smoothedMaxs))])))

	#minsMappedToOriginal = mapToOriginalRecursive(X,smoothedMins,unsmoothedMins,"mins")
	#maxsMappedToOriginal = mapToOriginalRecursive(X,smoothedMaxs,unsmoothedMaxs,"maxs")

	return (minsMappedToOriginal,maxsMappedToOriginal)

def mapToOriginalRecursive(originalData, smoothedSegmentationPoints, originalSegmentationPoints, typeOfSegmentationPoints):
	averageSegmentLength = (smoothedSegmentationPoints[-1] - smoothedSegmentationPoints[0]) / (len(smoothedSegmentationPoints)-1)
	searchWindowDivisor=1

	while True:
		mappedSegments = []
		for sp in smoothedSegmentationPoints:
			indexOfNearestOriginalPoint = originalSegmentationPoints.index(min(originalSegmentationPoints, key=lambda x:abs(x-sp)))
			nearestOriginalPoint = min(originalSegmentationPoints, key=lambda x:abs(x-sp))
			nearbyOriginalPoints = [p for p in originalSegmentationPoints if abs(p-nearestOriginalPoint)<(averageSegmentLength/searchWindowDivisor)]
			if len(nearbyOriginalPoints) == 0:
				nearbyOriginalPoints.append(nearestOriginalPoint)
			if typeOfSegmentationPoints == "maxs":
				highestNearbyOriginalPeak = max(nearbyOriginalPoints, key=lambda x:originalData[x])
				mappedSegments.append(highestNearbyOriginalPeak)
			elif typeOfSegmentationPoints == "mins":
				deepestNearbyOriginalValley = min(nearbyOriginalPoints, key=lambda x:originalData[x])
				mappedSegments.append(deepestNearbyOriginalValley)
			else:
				mappedSegments.append(nearestOriginalPoint)

		if len(mappedSegments) != len(set(mappedSegments)) and len(originalData)/searchWindowDivisor>50:
			searchWindowDivisor += 1
		else:
			return sorted(list(set(mappedSegments)))

if __name__=='__main__':
	import sys
	if len(sys.argv)==2:
		with open(sys.argv[1],'r') as fin:
			X = np.loadtxt(sys.argv[1],delimiter=",")
		segmentAndPlot(X)
		sys.exit(0)
	if len(sys.argv)==3:
		if sys.argv[2] == "plot":
			with open(sys.argv[1],'r') as fin:
				X = np.loadtxt(sys.argv[1],delimiter=",")
			segmentAndPlot(X)
			sys.exit(0)
		if sys.argv[2] == "save":
			with open(sys.argv[1],'r') as fin:
				X = np.loadtxt(sys.argv[1],delimiter=",")
			segmentAndSave(X)
			sys.exit(0)
	print "Usage: segment <file.csv> [plot|save]"