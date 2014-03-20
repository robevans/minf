import csv
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from database_gyroGaits import PCAclusteringSegmenter
from pca import pca

class database_walksOrientPair:
	def __init__(self, sourceDir="captures/walksOrientPair"):
		self.feet = [self.parse(sourceDir+'/feet1.csv'), self.parse(sourceDir+'/feet2.csv'), self.parse(sourceDir+'/feet3.csv')]
		self.shins = [self.parse(sourceDir+'/shins1.csv'), self.parse(sourceDir+'/shins2.csv'), self.parse(sourceDir+'/shins3.csv')]
		self.thighs = [self.parse(sourceDir+'/thighs1.csv'), self.parse(sourceDir+'/thighs2.csv')]
		self.hips = [self.parse(sourceDir+'/hips1.csv'), self.parse(sourceDir+'/hips2.csv')]
		self.chest = [self.parse(sourceDir+'/chest1.csv'), self.parse(sourceDir+'/chest2.csv')]

		self.pca_segmenter = PCAclusteringSegmenter()
		
	def parse(self, filepath):
		with open(filepath, 'rb') as csvfile:
			dialect = csv.Sniffer().sniff(csvfile.read())
		date_parser = lambda x: dt.datetime.fromtimestamp(float(x))
		both_orients = pd.read_table(filepath, dialect=dialect, usecols=[0,4,5,6,8,9,10,12,13,14,15], parse_dates=[10], date_parser=date_parser)
		
		# Fixes pandas' sillyness, for some reason it reads the accelZ values as generic objects rather than numbers.
		both_orients["accelZ"] = both_orients["accelZ"].convert_objects(convert_numeric=True)
		
		left_orient = both_orients[ both_orients["nodeID"]==2 ].drop("nodeID",axis=1)
		right_orient = both_orients[ both_orients["nodeID"]==3 ].drop("nodeID",axis=1)

		left_orient.index = range(1,len(left_orient)+1)
		right_orient.index = range(1,len(right_orient)+1)

		return {'L':left_orient, 'R':right_orient}

	def plotLR(self, LRdict, show=True, sensors=['gyroX','gyroY','gyroZ','accelX','accelY','accelZ','magX','magY','magZ']):
		plt.figure(figsize=(12, 8), dpi=80)
		top = plt.subplot(211)
		plt.title("Left Orient Data")
		LRdict['L'][sensors].plot(ax=top)
		plt.xlabel("")
		plt.setp(top.get_xticklabels(), visible=False)
		bottom = plt.subplot(212, sharex=top)
		plt.title("Right Orient Data")
		LRdict['R'][sensors].plot(ax=bottom)

		if show:	
			plt.show()


	def plotAll(self, sensors=['gyroX','gyroY','gyroZ','accelX','accelY','accelZ','magX','magY','magZ'], LR='L', segment=None, applyPCA=False):
			plt.figure(figsize=(12, 8), dpi=80)

			foot = plt.subplot(511)
			plt.title("Foot")
			data = self.feet[2][LR][sensors]
			if segment:
				self.plotSegments(data, segPoints=segment, subplot=True, applyPCA=applyPCA)
			elif applyPCA:
				plt.plot(pca(data, n_components=1)[0])
			else:
				data.plot(ax=foot)
			plt.xlabel("")
			plt.setp(foot.get_xticklabels(), visible=False)

			shin = plt.subplot(512, sharex=foot)
			plt.title("Shin")
			data = self.shins[2][LR][sensors]
			if segment:
				self.plotSegments(data, segPoints=segment, subplot=True, applyPCA=applyPCA)
			elif applyPCA:
				plt.plot(pca(data, n_components=1)[0])
			else:
				data.plot(ax=shin)
			plt.xlabel("")
			plt.setp(shin.get_xticklabels(), visible=False)

			thigh = plt.subplot(513, sharex=foot)
			plt.title("Thigh")
			data = self.thighs[1][LR][sensors]
			if segment:
				self.plotSegments(data, segPoints=segment, subplot=True, applyPCA=applyPCA)
			elif applyPCA:
				plt.plot(pca(data, n_components=1)[0])
			else:
				data.plot(ax=thigh)
			plt.xlabel("")
			plt.setp(thigh.get_xticklabels(), visible=False)

			hip = plt.subplot(514, sharex=foot)
			plt.title("Hip")
			data = self.hips[1][LR][sensors]
			if segment:
				self.plotSegments(data, segPoints=segment, subplot=True, applyPCA=applyPCA)
			elif applyPCA:
				plt.plot(pca(data, n_components=1)[0])
			else:
				data.plot(ax=hip)
			plt.xlabel("")
			plt.setp(hip.get_xticklabels(), visible=False)

			chest = plt.subplot(515, sharex=foot)
			plt.title("Chest")
			data = self.chest[1][LR][sensors]
			if segment:
				self.plotSegments(data, segPoints=segment, subplot=True, applyPCA=applyPCA)
			elif applyPCA:
				plt.plot(pca(data, n_components=1)[0])
			else:
				data.plot(ax=chest)

			plt.show()

	def plotSegments(self, rawData, segPoints="pca", subplot=False, applyPCA=False):
		if "currentTime" in rawData.columns:
			rawData = rawData.drop("currentTime",axis=1)
		if not subplot:
			plt.figure(figsize=(11,9))
		if segPoints == "pca":
			segPoints = self.pca_segmenter.findSegments(rawData)
		if segPoints == "minExtrema":
			segPoints = self.relativeExtremaSegments(rawData, maxMin="min")
		if segPoints == "maxExtrema":
			segPoints = self.relativeExtremaSegments(rawData, maxMin="max")
		if applyPCA:
			plt.plot(pca(rawData, n_components=1)[0])
		else:
			plt.plot(rawData)
		for s in segPoints:
			if s <= len(rawData):
				plt.axvline(s,color='black',linewidth=2)
		if not subplot:
			plt.show()

	def relativeExtremaSegments(self, rawData, maxMin="max", minSegSize=50):
		from scipy.signal import argrelmax, argrelmin
		PCs = pca(rawData, n_components=1)[0]
		if maxMin == 'max':
			return argrelmax(PCs[:,0], order=minSegSize)[0]
		if maxMin == 'min':
			return argrelmin(PCs[:,0], order=minSegSize)[0]


