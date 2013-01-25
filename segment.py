import numpy as np
import mins_and_maxs as mm
import smooth as sm
import pylab as pl

def segmentAndPlot(X):
	(mins,maxs) = segmentationPoints(X)
	pl.figure(figsize=(11,9))
	pl.plot(X)
	for m in mins:
		pl.axvline(m,color='g')
	for m in maxs:
		pl.axvline(m,color='r')

	pl.xlabel('Time (frames)')
	pl.ylabel('Latent co-ordinate')
	pl.title('Vertical Arm Spins - Post PCA segmentation')
	#pl.legend((''))

	pl.show()
	#pl.savefig('/Users/robertevans/Desktop/segments.pdf', format='pdf')

def segmentAndSave(X, segmentBy="maxs",trimFrom=None,trimTo=float('inf'),filePrefix="H",fileSuffix=".csv"):
	(mins,maxs) = segmentationPoints(X)
	if segmentBy == "maxs":
		segPoints=[m for m in maxs if m>=trimFrom and m<=trimTo]
	if segmentBy == "mins":
		segPoints=[m for m in mins if m>=trimFrom and m<=trimTo]
	segments=np.split(X,segPoints)

	i=0
	for seg in segments:
		np.savetxt("%s%i%s"%(filePrefix,i,fileSuffix),seg, delimiter=",")
		i+=1
		print segments

def segmentationPoints(X):
	smoothX = sm.smooth(X,window_len=11,window='flat')
	(unsmoothedMins,unsmoothedMaxs) = mm.find_mins_and_maxs1D(X)
	(smoothedMins,smoothedMaxs) = mm.find_mins_and_maxs1D(smoothX)

	minSegmentations = mapToOriginal(X,smoothedMins,unsmoothedMins,"mins")
	maxSegmentations = mapToOriginal(X,smoothedMaxs,unsmoothedMaxs,"maxs")

	return (minSegmentations,maxSegmentations)

def mapToOriginal(originalData, smoothedSegmentationPoints, originalSegmentationPoints, typeOfSegmentationPoints):
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