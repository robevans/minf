import numpy
import pylab as pl
def CSVtoRawData(inFile,outFile):
	allData=[]
	with open(inFile,'r') as fin:
			lines = pl.loadtxt(fin,delimiter=",")
	
	for data in lines:
		nodeID = int(data[0])
		accelRTC = int(data[1])
		gyroRTC = int(data[2])
		magRTC = int(data[3])
		accel = numpy.array(data[4:7])
		gyro =  numpy.array(data[7:10])
		mag = numpy.array(data[10:13])
		allData.append((nodeID, accelRTC, gyroRTC, magRTC, accel, gyro, mag))

	with open (outFile,'w') as fout:
		for data in allData:
			fout.write(str(data)+'\n')