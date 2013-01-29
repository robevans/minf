__author__ = 'Andrew'
from numpy import loadtxt
from time import sleep
from OrientSocket import *
from matplotlib.pyplot import plot, show
from orientSync import unwrapTimestamps
from OrientDataset import *
from graph import *

PC_FILE= "../ScottishBallet/finalCapture/pcCaptures/ID_run01.log"
pc = OrientPCDataset(PC_FILE)
SYNC=True

def closestIndex(target, timestamps):
    return (abs(timestamps-target)).argmin()

allArray = empty((0,4))

bsOffset = [2,21,5,15]

for i in pc.IDs():
    if i not in bsOffset:
        grtc = pc.synchronisedGyroRTC(i)
        bsrtc = pc.bsRTC(i)
        lines = pc.getLineNumbers(i)
        print len(grtc)
        print len(lines)

        if i == 2:
            figure()
            plot(grtc)
            plot(bsrtc)

        deviceArray = empty((len(grtc),4))
        deviceArray[:,0]=grtc
        deviceArray[:,1]=bsrtc
        deviceArray[:,2]=lines
        deviceArray[:,3]=i

        allArray = append(allArray, deviceArray,axis=0)
allArray = allArray[allArray[:,2].argsort()]

graph(allArray[:,0], allArray[:,2], allArray[:,3])
show()

data_array = empty((0,13))

for id in pc.IDs():
    #if id not in [8,9,10,11,12,13]:
    print id

    if not SYNC:
        gyroTimestamps = pc.gyroRTC(id)
        accelTimestamps = pc.accelRTC(id)
        magTimestamps = pc.magRTC(id)
    else:
        gyroTimestamps = pc.synchronisedGyroRTC(id)
        accelTimestamps = pc.synchronisedAccelRTC(id)
        magTimestamps = pc.synchronisedMagRTC(id)

    gyroVectors = pc.gyroVectors(id)
    accelVectors = pc.accelVectors(id)
    magVectors = pc.magVectors(id)

    gta = empty((len(gyroTimestamps),13))
    gta[:,0] = id
    gta[:,1] = gyroTimestamps

    for i in range(len(gyroTimestamps)):
        latestGyroRTC = gyroTimestamps[i]
        gyroIndex = i
        closestAccelIndex = closestIndex(latestGyroRTC, accelTimestamps)
        closestMagIndex = closestIndex(latestGyroRTC,magTimestamps)

        g = gyroVectors[gyroIndex]
        a = accelVectors[closestAccelIndex]
        m = magVectors[closestMagIndex]

        aRTC = accelTimestamps[closestAccelIndex]
        mRTC = magTimestamps[closestMagIndex]

        gta[i,2] = aRTC
        gta[i,3] = mRTC
        gta[i,4] = g[0]
        gta[i,5] = g[1]
        gta[i,6] = g[2]
        gta[i,7] = a[0]
        gta[i,8] = a[1]
        gta[i,9] = a[2]
        gta[i,10] = m[0]
        gta[i,11] = m[1]
        gta[i,12] = m[2]

    data_array = append(data_array, gta,axis=0)

data_array = data_array[data_array[:,1].argsort()]

savetxt("orientation.csv", data_array, delimiter=',')