import csv
import pandas as pd

class RespireWalks:
	# Sample rate of data is 12.5Hz
	def __init__(self, sourceDir="/Users/robertevans/repos/minf/captures/Gait data/respire"):
		self.__dec6 = self.parse(sourceDir+'/respire-20121206000850.csv')
		self.__feb10 = self.parse(sourceDir+'/respire-20130210162724.csv')
		self.__feb11 = self.parse(sourceDir+'/respire-20130211014154.csv')
		self.__feb18_0 = self.parse(sourceDir+'/respire-20130218132621.csv')
		self.__feb18_1 = self.parse(sourceDir+'/respire-20130218141032.csv')
		self.__feb20_0 = self.parse(sourceDir+'/respire-20130220101143.csv')
		self.__feb20_1 = self.parse(sourceDir+'/respire-20130220111156.csv')
		self.__feb20_2 = self.parse(sourceDir+'/respire-20130220114757.csv')
		self.__feb20_3 = self.parse(sourceDir+'/respire-20130220121539.csv')
		self.__feb20_4 = self.parse(sourceDir+'/respire-20130220131133.csv')
		self.__feb20_5 = self.parse(sourceDir+'/respire-20130220142242.csv')
		self.__feb20_6 = self.parse(sourceDir+'/respire-20130220155513.csv')
		self.__feb21 = self.parse(sourceDir+'/respire-20130221060649.csv')

		self.data = [self.__dec6, self.__feb10, self.__feb11, self.__feb18_0, self.__feb18_1, self.__feb20_0, self.__feb20_1, self.__feb20_2, self.__feb20_3, self.__feb20_4, self.__feb20_5, self.__feb20_6, self.__feb21]

	def parse(self, filepath, headerLines=1):
		with open(filepath,'rb') as csvfile:
			dialect = csv.Sniffer().sniff(csvfile.read())
			resp=pd.read_table(filepath, dialect=dialect, usecols=[8,9,10])
		return resp