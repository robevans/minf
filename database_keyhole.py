import csv
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import math
import json
import operator
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
import gaussianFitter
import os
import matplotlib

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}

matplotlib.rc('font', **font)

class KeyholeSurgerySimulatorData:
	# Sample rate of data is 12.5Hz
	def __init__(self, sourceDir="/Users/robertevans/repos/minf/captures/keyhole/Respeck"):
		R1_Anne = self.parse(sourceDir+'/RESpeck_1_Anne_20130708155603.csv')
		R1_Ben = self.parse(sourceDir+'/RESpeck_1_Ben_20130708151903.csv')
		R1_Jamie = self.parse(sourceDir+'/RESpeck_1_Jamie_20130708153533.csv')
		R1_Jane = self.parse(sourceDir+'/RESpeck_1_Jane_20130708154832.csv')
		R1_Katie_1 = self.parse(sourceDir+'/RESpeck_1_Katie_20130708153938.csv')
		R1_Katie_2 = self.parse(sourceDir+'/RESpeck_1_Katie_20130708160309.csv')
		R1_Mel = self.parse(sourceDir+'/RESpeck_1_Mel_20130708153122.csv')
		R2_Jimmy_1 = self.parse(sourceDir+'/RESpeck_2_Jimmy_20130708154329.csv')
		R2_Jimmy_2 = self.parse(sourceDir+'/RESpeck_2_Jimmy_20130708154741.csv')
		R2_Merel = self.parse(sourceDir+'/RESpeck_2_Merel_20130708160055.csv')
		R2_Neil = self.parse(sourceDir+'/RESpeck_2_Neil_20130708155420.csv')
		R2_Richard = self.parse(sourceDir+'/RESpeck_2_Richard_20130708153313.csv')
		alldata = [R1_Anne, R1_Ben, R1_Jamie, R1_Jane, R1_Katie_1, R1_Katie_2, R1_Mel, R2_Jimmy_1, R2_Jimmy_2, R2_Merel, R2_Neil, R2_Richard]

		self.data_key = ["R1_Anne", "R1_Ben", "R1_Jamie", "R1_Jane", "R1_Katie_1", "R1_Katie_2", "R1_Mel", "R2_Jimmy_1", "R2_Jimmy_2", "R2_Merel", "R2_Neil", "R2_Richard"]
		self.split_data = map(self.__splitRawDataIntoLeftAndRight,alldata)
		self.merged_data = map(self.__extractLRSensorsToColumns,alldata)

		self.metrics = ActivityMetrics(self)

	def __splitRawDataIntoLeftAndRight(self, rawdata, keepTimestamp=True):
		sensor_names = set(rawdata['name'])
		columns = ['timestamp','accelX','accelY','accelZ'] if keepTimestamp else ['accelX','accelY','accelZ']
		return { side:rawdata[rawdata['name'] == name][columns] for name,side in zip(sensor_names,["R","L"]) }

	def __extractLRSensorsToColumns(self, rawdata):
		dataBySensor = self.__splitRawDataIntoLeftAndRight(rawdata, keepTimestamp=True)
		dataBySensor['L'].columns = ['timestamp','L_accelX','L_accelY','L_accelZ']
		dataBySensor['R'].columns = ['timestamp','R_accelX','R_accelY','R_accelZ']
		return pd.merge(dataBySensor['L'],dataBySensor['R'],how='outer',on='timestamp')

	def parse(self, filepath, headerLines=1):
		with open(filepath,'rb') as csvfile:
			dialect = csv.Sniffer().sniff(csvfile.read())
			date_parser = lambda x: dt.datetime.strptime(x, "%Y%m%d%H%M%S.%f")
			resp=pd.read_table(filepath, dialect=dialect, usecols=[0,1,2,3,4], parse_dates=[1], date_parser=date_parser)
		return resp

	def plotAll(self, LR=None, dataList=None):
		dataList = self.merged_data if dataList == None else dataList
		for i in range(len(dataList)):
			plt.figure()
			if LR == 'L':
				columns = ['L_accelX','L_accelY','L_accelZ']
			if LR == 'R':
				columns = ['R_accelX','R_accelY','R_accelZ']
			if LR == None:
				columns = ['L_accelX','L_accelY','L_accelZ','R_accelX','R_accelY','R_accelZ']
			plt.plot(dataList[i]['timestamp'], dataList[i][columns])
			plt.legend(columns)
			plt.show()

	def plotPercentageChange(self, data, window_size=1, smoothing_window=1):
		plt.figure()
		plt.suptitle("Percentage change over %i frames"%window_size)

		top = plt.subplot(211)
		plt.ylabel("Acceleration")
		plt.plot(data['timestamp'],data[data.columns - ['timestamp']])

		bottom = plt.subplot(212, sharex=top)
		plt.ylabel("Percentage change")
		plt.xlabel("Time (Frames)")

		sortedData = data.sort('timestamp')
		sortedTime = sortedData['timestamp']
		noTimestamp = sortedData[data.columns - ['timestamp']]
		normalisedData = (noTimestamp - noTimestamp.mean()) / (noTimestamp.max() - noTimestamp.min())
		summedPercentageChange = noTimestamp.pct_change(window_size).sum(axis=1)
		rolledAverage = pd.rolling_sum(summedPercentageChange, smoothing_window)
		restoredTimestamp = pd.concat( [sortedTime, rolledAverage], axis=1).rename(columns={0:'timestamp', 1:'Percentage change'})
		restoredTimestamp.plot(ax=bottom, x=['timestamp'], y=restoredTimestamp.columns - ['timestamp'])
		
		# Can do arbitary rolling window functions (eg try sum of differences) with pd.rolling_apply

		plt.show()


class ActivityMetrics:
	def __init__(self, db):
		self.db = db

	def sumsOfDifferences(self, data, window_size=10):
		differences = {}
		for sensor in data[data.columns-['timestamp']]:
			differences[sensor] = pd.rolling_apply(data[sensor], window_size, lambda x: sum(np.ediff1d(x)))
		return pd.DataFrame(differences)

	def sumsOfSquaredDifferences(self, data, window_size=10):
		squaredDifferences = {}
		for sensor in data[data.columns-['timestamp']]:
			squaredDifferences[sensor] = pd.rolling_apply(data[sensor], window_size, lambda x: sum(np.ediff1d(x)**2))
		return pd.DataFrame(squaredDifferences)

	def averageSumOfDifferences(self, data, window_size=10):
		return self.sumsOfDifferences(data, window_size).mean(axis=1)

	def averageSumOfSquaredDifferences(self, data, window_size=10):
		return self.sumsOfSquaredDifferences(data, window_size).mean(axis=1)

	def averageMeans(self, data, window_size=10):
		means = {}
		for sensor in data[data.columns-['timestamp']]:
			means[sensor] = pd.rolling_mean(data[sensor], window_size)
		return pd.DataFrame(means).mean(axis=1)

	def averageVariances(self, data, window_size=10):
		variances = {}
		for sensor in data[data.columns-['timestamp']]:
			variances[sensor] = pd.rolling_var(data[sensor], window_size)
		return pd.DataFrame(variances).mean(axis=1)

	def plotStack(self, data, metrics, title="Keyhole surgery simulator data"):
		plt.figure()
		plt.suptitle(title)
		data_axes = plt.subplot(len(metrics)+1,1,1)
		plt.ylabel("Acceleration (G)")
		data.plot(x=['timestamp'], y=data.columns - ['timestamp'], ax=data_axes)

		for i,metric in enumerate(metrics):
			ax = plt.subplot(len(metrics)+1,1,i+2, sharex=data_axes)
			plt.ylabel("Mean variance")
			if isinstance(metric, pd.Series):
				pd.concat([data['timestamp'],metric],axis=1).plot(x=[0],y=[1], ax=ax)
			if isinstance(metric, pd.DataFrame):
				metric['timestamp']=data['timestamp']
				metric.plot(x=['timestamp'], y=metric.columns-['timestamp'])

		plt.xlabel('Time of capture')
		plt.tight_layout(h_pad=-5.2)
		plt.show()

	def plotComparisonOfMetrics(self, data, window_size=10):
		metrics = [ 												\
		#self.sumsOfDifferences(data, window_size),					\
		#self.averageSumOfDifferences(data, window_size),			\
		##self.averageSumOfDifferences(data, window_size).cumsum(),			\
		#pd.rolling_sum(self.averageSumOfDifferences(data, window_size),50).cumsum(),			\
		#self.sumsOfSquaredDifferences(data, window_size),			\
		#self.averageSumOfSquaredDifferences(data, window_size),		\
		##self.averageSumOfSquaredDifferences(data, window_size).cumsum(),		\
		#pd.rolling_sum(self.averageSumOfSquaredDifferences(data, window_size),50).cumsum(),		\
		#self.averageMeans(data, window_size),						\
		self.averageVariances(data,window_size),					\
		##self.averageVariances(data,window_size).cumsum(),					\
		#pd.rolling_sum(self.averageVariances(data,window_size),50).cumsum()	\
		]

		self.plotStack(data, metrics, title='Data and Smoothness of Simulated Laparoscopy Task')

	def plotLRwithMetrics(self, dataIndex=1):
		l,r = self.db.split_data[dataIndex]['L'],self.db.split_data[dataIndex]['R']
		l_metric = self.averageSumOfDifferences(l)
		r_metric = self.averageSumOfDifferences(r)

		plt.figure()
		top = plt.subplot(411)
		l.plot(ax=top)
		plt.title('Left')

		ax = plt.subplot(412, sharex=top)
		l_metric.plot(ax=ax)

		ax = plt.subplot(413, sharex=top)
		r.plot(ax=ax)
		plt.title('Right')

		ax = plt.subplot(414, sharex=top)
		r_metric.plot(ax=ax)

		plt.show()


class OrientationCalculator:
	def __init__(self, db):
		self.db = db

	def plotMagnitudeOfAccelVectors(self, dataframe):
		rootOfSquare = pd.rolling_apply((dataframe[['accelX','accelY','accelZ']]**2).sum(axis=1),1,math.sqrt)
		plt.figure()
		plt.title("Magnitude of accelerometer values over time: mean = %f"%rootOfSquare.mean())
		rootOfSquare.plot()
		plt.show()

	def pitchAndRoll(self, dataframe, pitch_axis, roll_axis, plot=True):
		pitch = np.zeros((len(dataframe)))
		roll = np.zeros((len(dataframe)))

		pitch_denominator = list( set([0,1,2]) - set([pitch_axis]) )
		roll_denominator = list( set([0,1,2]) - set([roll_axis]) )

		for i,xyz in enumerate( dataframe[['accelX','accelY','accelZ']].values ):
			pitch[i] = math.degrees(math.atan( xyz[pitch_axis] / math.sqrt(xyz[pitch_denominator[0]]**2 + xyz[pitch_denominator[1]]**2) ))
			roll[i] = math.degrees(math.atan( xyz[roll_axis] / math.sqrt(xyz[roll_denominator[0]]**2 + xyz[roll_denominator[1]]**2) ))

		if plot:
			plt.figure()
			plt.plot(np.arange(0,len(pitch)/12.5,1/12.5)[:len(pitch)], pitch)
			plt.plot(np.arange(0,len(roll)/12.5,1/12.5)[:len(roll)], roll)
			plt.legend(["Pitch","Roll"], loc=0)
			plt.title("Instrument Pitch and Roll from One Trial")
			plt.xlabel("Time (seconds)")
			plt.ylabel("Degrees")
			plt.show()

		return pd.DataFrame({'pitch':pitch, 'roll':roll} )

	def coneBase(self, dataframe, pitch_axis, roll_axis, plot=False):
		pitch_roll = self.pitchAndRoll(dataframe, pitch_axis=pitch_axis, roll_axis=roll_axis, plot=False)
		trace =[]
		for i in range(len(pitch_roll)):
			p = math.radians(pitch_roll['pitch'][i])
			r = math.radians(pitch_roll['roll'][i])
			to = [0, -100, 0]
			tx = self.rotateAroundXAxis(to, p)
			ty = self.rotateAroundYAxis(tx, r)
			t = map(operator.add, ty, [750.0,100.0,0.0])
			trace.append(t)
		if plot:
			centroid=np.mean(trace, axis=0)
			fig=plt.figure()
			ax = Axes3D(fig)
			xs, ys, zs = zip(*trace)
			ax.scatter(xs, ys, zs, s=2)
			ax.scatter(*centroid, s=100, c='r')
			plt.show()
		return trace

	def flattenedConeBase(self, dataframe, pitch_axis, roll_axis, plot=False):
		trace = self.coneBase(dataframe, pitch_axis=pitch_axis, roll_axis=roll_axis, plot=False)
		pca_flattener = PCA(n_components=2)
		flat = pca_flattener.fit_transform(trace)
		if plot:
			centroid=np.mean(flat, axis=0)
			fig=plt.figure()
			xs, ys = zip(*flat)
			plt.scatter(xs,ys, s=2)
			plt.scatter(*centroid, s=100, c='r')
			plt.show()
		return flat

	def showConeBaseForAllAxisCombinations(self, dataframe):
		combinations = [(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)]
		letterMap = ['x','y','z']
		plt.figure()
		for i,(p,r) in enumerate(combinations):
			coneBase = self.flattenedConeBase(dataframe, pitch_axis=p, roll_axis=r, plot=False)
			centroid=np.mean(coneBase, axis=0)
			plt.subplot(2,3,i+1)
			plt.title("Pitch: {0}-axis Roll: {1}-axis".format(letterMap[p],letterMap[r]))
			plt.scatter(*zip(*coneBase), s=2)
			plt.scatter(*centroid, s=100, c='r')
			
		#plt.show()



	def rotateAroundXAxis(self, point, angleInRads):
		xRotate = [[1.0, 0.0, 0.0], [0.0, math.cos(angleInRads), -math.sin(angleInRads)], [0.0, math.sin(angleInRads), math.cos(angleInRads)]]
		return self.__rotateAroundAxis(xRotate, point)

	def rotateAroundYAxis(self, point, angleInRads):
		yRotate = [[math.cos(angleInRads), 0.0, math.sin(angleInRads)], [0.0, 1.0, 0.0], [-math.sin(angleInRads), 0, math.cos(angleInRads)]]
		return self.__rotateAroundAxis(yRotate, point)

	def rotateAroundZAxis(self, point, angleInRads):
		zRotate = [[math.cos(angleInRads), -math.sin(angleInRads), 0.0], [math.sin(angleInRads), math.cos(angleInRads), 0.0], [0.0, 0, 1.0]]
		return self.__rotateAroundAxis(zRotate, point)

	def __rotateAroundAxis(self, rotationMatrix, point):
		R = [0.0, 0.0, 0.0]
		for row in range(3):
			for i in range(3):
				R[row] += rotationMatrix[row][i] * point[i]
		return R

	def JSONPitchAndRoll(self, dataframe, pitch_axis, roll_axis):
		pitch_roll = self.pitchAndRoll(dataframe, pitch_axis=pitch_axis, roll_axis=roll_axis, plot=False)
		json_pitch = json.JSONEncoder().encode(pitch_roll['pitch'].tolist())
		json_roll = json.JSONEncoder().encode(pitch_roll['roll'].tolist())
		return (json_pitch, json_roll)

	def dumpDataForProcessingScript(self, destinationFolder="/Users/robertevans/repos/minf/Keyhole surgery data visualiser/pitch_roll/data"):
		for i,data in enumerate(self.db.split_data):
			l_pitch, l_roll = self.JSONPitchAndRoll(data['L'], pitch_axis=1, roll_axis=2)
			r_pitch, r_roll = self.JSONPitchAndRoll(data['R'], pitch_axis=1, roll_axis=2)
			if not os.path.exists(destinationFolder+"/L"):
				os.makedirs(destinationFolder+"/L")
			if not os.path.exists(destinationFolder+"/R"):
				os.makedirs(destinationFolder+"/R")	
			with open(destinationFolder+"/L/{0}_pitch.json".format(i),'w') as outfile:
				outfile.write(l_pitch)
			with open(destinationFolder+"/L/{0}_roll.json".format(i),'w') as outfile:
				outfile.write(l_roll)
			with open(destinationFolder+"/R/{0}_pitch.json".format(i),'w') as outfile:
				outfile.write(r_pitch)
			with open(destinationFolder+"/R/{0}_roll.json".format(i),'w') as outfile:
				outfile.write(r_roll)





