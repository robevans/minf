import pandas as pd
import csv
import datetime

class TateData:
	def __init__(self):
		with open('captures/Tate data/Tuesday 24/tuesday.txt','r') as csvfile:
			self.__csv_dialect = csv.Sniffer().sniff(csvfile.read())

	def loadAll(self):
		csvfiles = ['captures/Tate data/thursday 19/thursday.txt','captures/Tate data/thursday 19/tuesday2.txt','captures/Tate data/friday 20/friday.txt','captures/Tate data/friday 20/friday2.txt','captures/Tate data/saturday 21/saturday.txt','captures/Tate data/saturday 21/saturday2.txt','captures/Tate data/Tuesday 24/tuesday.txt','captures/Tate data/Tuesday 24/tuesday2.txt','captures/Tate data/wednesday 25/wednesday.txt','captures/Tate data/thursday 26/thursday.txt','captures/Tate data/thursday 26/thursday2.txt','captures/Tate data/friday 27/friday.txt','captures/Tate data/saturday 28/saturday2.txt','captures/Tate data/sunday 29/sunday.txt','captures/Tate data/sunday 29/sunday2.txt']
		self.data = []
		print "Loading..."
		for i,capture in enumerate(csvfiles):
			print "%i / %i..."%(i+1,len(csvfiles))
			self.data.extend(self.parse_csv(capture))

	def parse_csv(self, filepath):
		table = pd.read_table(filepath, dialect=self.__csv_dialect, usecols=[0,4,5,6,8,9,10,12,13,14,15])
		sensors = table.groupby('nodeID')
		return [sensors.get_group(i) for i in sensors.indices if len(sensors.get_group(i))>10]