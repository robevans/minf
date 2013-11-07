import csv
from pylab import array

def parse(filepath,headerLines=9):
	with open(filepath,'rb') as csvfile:
		dialect = csv.Sniffer().sniff(csvfile.read())
		csvfile.seek(0)
		reader = csv.reader(csvfile,dialect)
		lines = 0
		data =[]
		for l in reader:
			lines += 1
			if lines <= headerLines:
				if lines == headerLines:
					key = l
					print key
			else:
				data.append([float(x) for x in l])
		return (array(data),key)