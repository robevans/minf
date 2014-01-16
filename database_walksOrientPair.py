import csv
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

class database_walksOrientPair:
	def __init__(self, sourceDir="captures/walksOrientPair"):

		self.feet = [self.parse(sourceDir+'/feet1.csv'), self.parse(sourceDir+'/feet2.csv'), self.parse(sourceDir+'/feet3.csv')]
		self.shins = [self.parse(sourceDir+'/shins1.csv'), self.parse(sourceDir+'/shins2.csv'), self.parse(sourceDir+'/shins3.csv')]
		self.thighs = [self.parse(sourceDir+'/thighs1.csv'), self.parse(sourceDir+'/thighs2.csv')]
		self.hips = [self.parse(sourceDir+'/hips1.csv'), self.parse(sourceDir+'/hips2.csv')]
		self.chest = [self.parse(sourceDir+'/chest1.csv'), self.parse(sourceDir+'/chest2.csv')]
		
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

	def plotAllCategories