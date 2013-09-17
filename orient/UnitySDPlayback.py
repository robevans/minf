__author__ = 'Andrew'
from numpy import loadtxt
from time import sleep
from OrientSocket import *
from matplotlib.pyplot import plot, show

PLAYBACK_FILE = "ph005.csv"

#NODE_ID, ACCEL_RTC, GYRO_RTC, MAG_RTC, ACCEL, GYRO, MAG = range(7)

#RATE = 0.025
RATE=1.0

data_array = loadtxt(PLAYBACK_FILE, delimiter=',')
s = Panda(live=False, sd=True, path="../ScottishBallet/finalCapture/calibration/")

print "loaded"

#plot(data_array[:,1])
#show()

firstTimestamp = data_array[1,1]
#startTimestamp = firstTimestamp + (46875 * 20)

for i in range(len(data_array)-1):

    if True or data_array[i,1] > startTimestamp:
        #latestData = (latestID, aRTC, latestGyroRTC, mRTC, a, g, m)
        latestData = (data_array[i,0],data_array[i,2],data_array[i,1],data_array[i,3],data_array[i,7:10],data_array[i,4:7],data_array[i,10:13])
        #print latestData
        s.handleData(latestData)
        #sleep for difference between current and next gyro timestamp
        time_diff = data_array[i+1,1]-data_array[i,1]
        #print time_diff
        sleep((time_diff/46875.0) / RATE)
