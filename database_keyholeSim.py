import pandas as pd
import csv
import datetime
import orient.orientation as oo
import numpy as np
import json
import matplotlib.pyplot as plt

# nodeID 2 == Left, nodeID 3 == right.

class KeyholeSim:
	def __init__(self):
		with open('/Users/robertevans/repos/minf/captures/keyhole/session1/expertTouchFourPegs.csv','r') as csvfile:
			self.__csv_dialect = csv.Sniffer().sniff(csvfile.read())
		self.loadAll()

	def performancesForThreadingTask(self):
		expert = self.performance( 0, 1 )
		novice1 = self.performance( 2, 3 )
		novice2 = self.performance( 4, 5 )
		novice3 = self.performance( 6, 7 )

		plt.figure()
		plt.title("Total Task Duration")
		plt.ylabel("Time (seconds)")
		plt.plot([expert['duration'], novice1['duration'], novice2['duration'], novice3['duration']])
		plt.ylim([0,500])
		plt.xticks( range(4), ('Expert', 'Novice 1', 'Novice 2', 'Novice 3') )

		plt.figure()
		plt.title("Total Task Angular Distance")
		plt.ylabel("Rotation (degrees)")
		plt.plot([expert['angularDist'], novice1['angularDist'], novice2['angularDist'], novice3['angularDist']])
		plt.ylim([0,120000])
		plt.xticks( range(4), ('Expert', 'Novice 1', 'Novice 2', 'Novice 3') )

		plt.figure()
		plt.title("Total Task Average Speed")
		plt.ylabel("Speed (degrees/second)")
		plt.plot([expert['duration']/expert['angularDist'], novice1['duration']/novice1['angularDist'], novice2['duration']/novice2['angularDist'], novice3['duration']/novice3['angularDist']])
		plt.ylim([0,0.0052])
		plt.xticks( range(4), ('Expert', 'Novice 1', 'Novice 2', 'Novice 3') )

		plt.figure()
		plt.title("Total Task Performace")
		plt.plot([expert['perf'], novice1['perf'], novice2['perf'], novice3['perf']])
		
		plt.xticks( range(4), ('Expert', 'Novice 1', 'Novice 2', 'Novice 3') )

		plt.show()

	def angularVelocityHistsForThreadingTask(self):
		plt.figure()
		plt.title("Expert: Angular Velocity Distribution")
		plt.hist(self.diffs[0]+self.diffs[1], normed=True, stacked=True, range=(0,3.15))
		plt.ylim([0,1.2])

		plt.figure()
		plt.title("Novice 1: Angular Velocity Distribution")
		plt.hist(self.diffs[2]+self.diffs[3], normed=True, stacked=True, range=(0,3.15))
		plt.ylim([0,1.2])

		plt.figure()
		plt.title("Novice 2: Angular Velocity Distribution")
		plt.hist(self.diffs[4]+self.diffs[5], normed=True, stacked=True, range=(0,3.15))
		plt.ylim([0,1.2])

		plt.figure()
		plt.title("Novice 3: Angular Velocity Distribution")
		plt.hist(self.diffs[6]+self.diffs[7], normed=True, stacked=True, range=(0,3.15))
		plt.ylim([0,1.2])

		plt.show()

	def performance(self, L_index, R_index):
		L_duration = self.data[L_index]['currentTime'][self.data[L_index].index[-1]] - self.data[L_index]['currentTime'][self.data[L_index].index[0]]
		R_duration = self.data[R_index]['currentTime'][self.data[R_index].index[-1]] - self.data[R_index]['currentTime'][self.data[R_index].index[0]]
		duration = max(L_duration, R_duration)

		L_distance = sum( self.diffs[L_index] )
		R_distance = sum( self.diffs[L_index] )
		distance = L_distance + R_distance

		return {'duration':duration, 'angularDist':distance, 'perf':((1/duration) + (1/distance))};

	def loadAll(self):
		csvfiles = ['rawOrient/expertRoland1.csv','rawOrient/noviceRoland1.csv','rawOrient/noviceRobert2.csv','rawOrient/noviceCristie3.csv','rawOrient/expertTouchingBases.csv','rawOrient/expertTouchFourPegs.csv']
		self.data = []
		self.quats = []
		self.diffs = []
		print "Loading..."
		for capture in csvfiles:
			self.data.extend(self.parse_csv(capture))
		
		for i,d in enumerate(self.data):
			print "%i / %i..."%(i+1,len(self.data))
			self.quats.append( self.getQuaternionSequence(d) )

		for qs in self.quats:
			self.diffs.append(self.angleDifferences(qs))

	def parse_csv(self, filepath):
		table = pd.read_table(filepath, dialect=self.__csv_dialect, usecols=[0,4,5,6,8,9,10,12,13,14,15])
		sensors = table.groupby('nodeID')
		return [sensors.get_group(i) for i in sensors.indices if len(sensors.get_group(i))>10]

	def getQuaternionSequence(self, DataFrame):
		orientationEstimator = oo.OrientCF(oo.Quaternion(0,0,0,1),k=0.1,aT=0.1)
		quaternionSequence = [oo.Quaternion(0,0,0,1)]

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

	def angleDifferences(self, quaternionSequence):
		angle_differences = []
		for i in range(len(quaternionSequence)-1):
			q1 = quaternionSequence[i]
			q2 = quaternionSequence[i+1]
			quaternion_difference = (q1**-1)*q2
			angle_differences.append( quaternion_difference.toAxisAngle()[1] )
		return angle_differences

	def dumpJSONrotationMatricies(self, quatsIndex, filepath):
		rotation_matricies = []
		for q in self.quats[quatsIndex]:
			rotation_matricies.append(q.toMatrix().tolist())
		with open(filepath, 'w') as jsonfile:
			jsonfile.write(json.JSONEncoder().encode(rotation_matricies))

	def dumpAllJSONrotationMatricies(self, folder):
		self.dumpJSONrotationMatricies(0, '{0}/expert1_L.json'.format(folder))
		self.dumpJSONrotationMatricies(1, '{0}/expert1_R.json'.format(folder))
		self.dumpJSONrotationMatricies(2, '{0}/novice1_L.json'.format(folder))
		self.dumpJSONrotationMatricies(3, '{0}/novice1_R.json'.format(folder))
		self.dumpJSONrotationMatricies(4, '{0}/novice2_L.json'.format(folder))
		self.dumpJSONrotationMatricies(5, '{0}/novice2_R.json'.format(folder))
		self.dumpJSONrotationMatricies(6, '{0}/novice3_L.json'.format(folder))
		self.dumpJSONrotationMatricies(7, '{0}/novice3_R.json'.format(folder))
		self.dumpJSONrotationMatricies(8, '{0}/touchingBases_L.json'.format(folder))
		self.dumpJSONrotationMatricies(9, '{0}/touchingBases_R.json'.format(folder))

	def dumpJSONeuler(self, quatsIndex, filepath):
		rotation_matricies = []
		for q in self.quats[quatsIndex]:
			rotation_matricies.append(q.toEuler().tolist())
		with open(filepath, 'w') as jsonfile:
			jsonfile.write(json.JSONEncoder().encode(rotation_matricies))

	def dumpAllJSONeuler(self, folder):
		self.dumpJSONeuler(0, '{0}/expert1_L.json'.format(folder))
		self.dumpJSONeuler(1, '{0}/expert1_R.json'.format(folder))
		self.dumpJSONeuler(2, '{0}/novice1_L.json'.format(folder))
		self.dumpJSONeuler(3, '{0}/novice1_R.json'.format(folder))
		self.dumpJSONeuler(4, '{0}/novice2_L.json'.format(folder))
		self.dumpJSONeuler(5, '{0}/novice2_R.json'.format(folder))
		self.dumpJSONeuler(6, '{0}/novice3_L.json'.format(folder))
		self.dumpJSONeuler(7, '{0}/novice3_R.json'.format(folder))
		self.dumpJSONeuler(8, '{0}/touchingBases_L.json'.format(folder))
		self.dumpJSONeuler(9, '{0}/touchingBases_R.json'.format(folder))



