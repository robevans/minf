import csv
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
from sklearn.decomposition import PCA

class TiltSlideData:
	def __init__(self, sourceDir="/Users/robertevans/repos/minf/captures/Respeck tilt and slide"):
		self.data = {0: self.parse(sourceDir+'/20131129115732.csv'),
					1: self.parse(sourceDir+'/20131129120013.csv'),
					2: self.parse(sourceDir+'/20131129120041.csv'),
					#3: self.parse(sourceDir+'/20131129135326.csv'),
					3: self.parse(sourceDir+'/20131129135417.csv'),
					4: self.parse(sourceDir+'/20131129135525.csv'),
					5: self.parse(sourceDir+'/20131129135653.csv'),
					6: self.parse(sourceDir+'/20131129152858.csv'),
					7: self.parse(sourceDir+'/20131129153437.csv')
					}

	def parse(self, filepath):
		with open(filepath, 'rb') as csvfile:
			dialect = csv.Sniffer().sniff(csvfile.read())
			date_parser = lambda x: dt.datetime.strptime(x, "%Y%m%d%H%M%S.%f")
			data = pd.read_table(filepath, dialect=dialect, usecols=[0,1,2,3,4,5,6,7], parse_dates=[1], date_parser=date_parser)
		data['accelX'] = self.__combineAccelBytes(data['accelX0'],data['accelX1'])
		data['accelY'] = self.__combineAccelBytes(data['accelY0'],data['accelY1'])
		data['accelZ'] = self.__combineAccelBytes(data['accelZ0'],data['accelZ1']) 
		return data.drop('name',1).drop('accelX0',1).drop('accelX1',1).drop('accelY0',1).drop('accelY1',1).drop('accelZ0',1).drop('accelZ1',1)

	def __combineAccelBytes(self, b0s, b1s):
		import struct
		def convert(b0,b1):
			b0 = int(b0)
			b1 = int(b1)
			ba = bytearray([b0,b1])
			r = struct.unpack(">h",str(ba))
			return r
		return [t[0] for t in map(convert,b0s,b1s)]

	def plotMagnitudeOfAccelVectors(self, dataframe,i):
		dataframe['accelX'] = dataframe['accelX'] / 16384.0
		dataframe['accelY'] = dataframe['accelY'] / 16384.0
		dataframe['accelZ'] = dataframe['accelZ'] / 16384.0
		rootOfSquare = pd.rolling_apply((dataframe[['accelX','accelY','accelZ']]**2).sum(axis=1),1,math.sqrt)
		plt.figure(figsize=(12, 8), dpi=80)
		top = plt.subplot(211)
		plt.title("Raw accelerometer data")
		dataframe.plot(ax=top, x=['timestamp'], y=['accelX','accelY','accelZ'])
		plt.legend(['X','Y','Z'])
		plt.xlabel("")
		plt.ylabel("Acceleration (G)")
		plt.setp(top.get_xticklabels(), visible=False)
		bottom = plt.subplot(212, sharex=top)
		pd.concat([dataframe['timestamp'],rootOfSquare],axis=1).plot(x=[0],y=[1])
		plt.xlabel("Time")
		plt.ylabel("Acceleration (G)")
		plt.title("Magnitude of accelerometer values")
		#plt.plot(dataframe['timestamp'],rootOfSquare)
		#rootOfSquare.plot()
		plt.tight_layout()
		plt.savefig('/Users/robertevans/Desktop/tiltGraphs/'+str(i)+'.pdf', format='pdf')
		#plt.show()

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
			plt.plot(pitch)
			plt.plot(roll)
			plt.legend(["Pitch","Roll"])
			plt.title("Pitch and roll of the accelerometer")
			plt.xlabel("Time")
			plt.ylabel("Degrees")
			plt.show()

		return pd.DataFrame({'pitch':pitch, 'roll':roll} )

	def pca(self, dataframe, n_components=3, plot=True):
		reducer = PCA(n_components=n_components)
		components = reducer.fit_transform(dataframe[['accelX','accelY','accelZ']])

		if plot:
			plt.plot(components)
			plt.show()

		return components