import pandas as pd
import csv
import datetime
import orient.orientation as oo
import numpy as np


class KeyholeSim:
	def __init__(self):
		with open('rawOrient/expertTouchFourPegs.csv','r') as csvfile:
			self.__csv_dialect = csv.Sniffer().sniff(csvfile.read())
		self.loadAll()

	def loadAll(self):
		csvfiles = ['rawOrient/expertRoland1.csv','rawOrient/expertTouchFourPegs.csv','rawOrient/expertTouchingBases.csv','rawOrient/noviceCristie3.csv','rawOrient/noviceRobert2.csv','rawOrient/noviceRoland1.csv']
		self.data = []
		print "Loading..."
		for i,capture in enumerate(csvfiles):
			print "%i / %i..."%(i+1,len(csvfiles))
			self.data.extend(self.parse_csv(capture))

	def parse_csv(self, filepath):
		table = pd.read_table(filepath, dialect=self.__csv_dialect, usecols=[0,4,5,6,8,9,10,12,13,14,15])
		sensors = table.groupby('nodeID')
		return [sensors.get_group(i) for i in sensors.indices if len(sensors.get_group(i))>10]

	def getQuaternionSequence(self, DataFrame):
		orientationEstimator = oo.OrientCF(oo.Quaternion(0,0,0,1),k=0.1,aT=0.1)
		quaternionSequence = []

		prev = DataFrame.index[0]
		for i in DataFrame.index[1:]:
			accel = np.float64( np.array( [[DataFrame.accelX[i]],[DataFrame.accelY[i]],[DataFrame.accelZ[i]]] ) )
			mag = np.float64( np.array( [[DataFrame.magX[i]],[DataFrame.magY[i]],[DataFrame.magZ[i]]] ) )
			gyro = np.float64( np.array( [[DataFrame.gyroX[i]],[DataFrame.gyroY[i]],[DataFrame.gyroZ[i]]] ) )
			dt = np.float64( DataFrame.currentTime[i] - DataFrame.currentTime[prev] )
			
			quat = orientationEstimator.update(accel, mag, gyro, dt)

			quaternionSequence.append( quat.copy() )
			prev = i

		return quaternionSequence