__author__ = 'Andrew'
from numpy import loadtxt
from time import sleep
from OrientSocket import *
from matplotlib.pyplot import plot, show
from orientSync import unwrapTimestamps
from OrientDataset import *

#type,ID,seq,accelRTC,gyroRTC,magRTC,accelX,accelY,accelZ,gyroX,gyroY,gyroZ,magX,magY,magZ,bsRTC
#NODE_ID, ACCEL_RTC, GYRO_RTC, MAG_RTC, ACCEL, GYRO, MAG = range(7)
CAL_PATH="../ScottishBallet/finalCapture/calibration/"
PC_SEND_FREQ = 5
PC_FILE= "../ScottishBallet/finalCapture/pcCaptures/ID_arm02.log"

dataset = OrientPCDataset(PC_FILE)
plot(dataset.accelVectors(6)[:,2])
show()

data_array = loadtxt(PC_FILE, delimiter=',',skiprows=1)
s = Panda(live=False, sd=False, path=CAL_PATH, send_freq=PC_SEND_FREQ)

print "loaded"
print len(data_array)

unwrapped_timestamps = unwrapTimestamps(data_array[:,15])[0]

#plot(unwrapped_timestamps)
#show()

SEQByNodeID = dict()

for i in range(len(data_array)):
    if data_array[i,1] == 6 and data_array[i,8] < 0:
        print "calibration stance " + str(i)

    type,nodeID,seqNumber,accelRTC,gyroRTC,magRTC,accelX,accelY,accelZ,gyroX,gyroY,gyroZ,magX,magY,magZ,bsRTC = data_array[i,:]

    SEQByNodeID[nodeID] = seqNumber

    gyro = array((float(-gyroY), float(-gyroX), float(-gyroZ)))
    #gyro *= float(gyroFactor)
    accel = array((float(accelX), float(accelY), float(accelZ)))
    mag = array((float(magX), float(magY), float(magZ)))

    #latestData = (latestID, aRTC, latestGyroRTC, mRTC, a, g, m)
    latestData = (nodeID,accelRTC,gyroRTC,magRTC,accel,gyro,mag)
    #print latestData
    s.handleData(latestData)
    #sleep for difference between current and next gyro timestamp
    time_diff = unwrapped_timestamps[i+1]-unwrapped_timestamps[i]
    #print time_diff
    sleep(time_diff/46875.0)
