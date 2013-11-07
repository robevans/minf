import csv
import pandas as pd
import matplotlib.pyplot as plt

class KeyholeSurgerySimulatorData:
	# Sample rate of data is 12.5Hz
	def __init__(self, sourceDir="/Users/robertevans/repos/minf/captures/keyhole"):
		self.__R1_Anne = self.parse(sourceDir+'/RESpeck_1_Anne_20130708155603.csv')
		self.__R1_Ben = self.parse(sourceDir+'/RESpeck_1_Ben_20130708151903.csv')
		self.__R1_Jamie = self.parse(sourceDir+'/RESpeck_1_Jamie_20130708153533.csv')
		self.__R1_Jane = self.parse(sourceDir+'/RESpeck_1_Jane_20130708154832.csv')
		self.__R1_Katie_1 = self.parse(sourceDir+'/RESpeck_1_Katie_20130708153938.csv')
		self.__R1_Katie_2 = self.parse(sourceDir+'/RESpeck_1_Katie_20130708160309.csv')
		self.__R1_Mel = self.parse(sourceDir+'/RESpeck_1_Mel_20130708153122.csv')
		self.__R2_Jimmy_1 = self.parse(sourceDir+'/RESpeck_2_Jimmy_20130708154329.csv')
		self.__R2_Jimmy_2 = self.parse(sourceDir+'/RESpeck_2_Jimmy_20130708154741.csv')
		self.__R2_Merel = self.parse(sourceDir+'/RESpeck_2_Merel_20130708160055.csv')
		self.__R2_Neil = self.parse(sourceDir+'/RESpeck_2_Neil_20130708155420.csv')
		self.__R2_Richard = self.parse(sourceDir+'/RESpeck_2_Richard_20130708153313.csv')

		self.data = [self.__R1_Anne, self.__R1_Ben, self.__R1_Jamie, self.__R1_Jane, self.__R1_Katie_1, self.__R1_Katie_2, self.__R1_Mel, self.__R2_Jimmy_1, self.__R2_Jimmy_2, self.__R2_Merel, self.__R2_Neil, self.__R2_Richard]



	def parse(self, filepath, headerLines=1):
		with open(filepath,'rb') as csvfile:
			dialect = csv.Sniffer().sniff(csvfile.read())
			resp=pd.read_table(filepath, dialect=dialect)
		return resp

	def plotAgainstActvity(self, dataList=None):
		dataList = self.data if dataList == None else dataList
		for i in range(len(dataList)):
			plt.figure(1)
			ax = plt.subplot(211)
			plt.plot(dataList[i][['accelX','accelY','accelZ']])
			plt.subplot(212, sharex=ax)
			plt.plot(dataList[i]['activity'])
			plt.show()