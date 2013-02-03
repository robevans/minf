__author__ = 'Andrew'
from OrientDataset import *
from OrientSocket import *
from time import sleep

#od = OrientSDDataset2("../ScottishBallet/finalCapture/sdCaptures", "ID_ARM02.LOG")
#od.synchroniseDataset("../ScottishBallet/finalCapture/pcCaptures/ID_arm02.log")
FILE = "ph3_4"

pc = OrientPCDataset("../ScottishBallet/finalCapture/pcCaptures/ID_" + FILE + ".log")
od = OrientSDDataset2("../ScottishBallet/finalCapture/sdCaptures", "ID_" + FILE.upper() + ".LOG")
od.synchroniseDataset(pc)
od.wrapCorrectDataset(pc)
SYNC=True

#s = Panda(live=False)

#NODE_ID, ACCEL_RTC, GYRO_RTC, MAG_RTC, ACCEL, GYRO, MAG = range(7)

def closestIndex(target, timestamps):
     return (abs(timestamps-target)).argmin()

data_array = empty((0,13))

# get gyro timestamps for all orients. Build numpy array of data and sort by gyro timestamp

figure()
for id in od.devices:
    #if id not in [8,9,10,11,12,13]:
    print id
    o = od.devices[id]
    if not SYNC:
        gyroTimestamps = o.gyroRTC
        accelTimestamps = o.accelRTC
        magTimestamps = o.magRTC
    else:
        gyroTimestamps = o.synchronisedGyroRTC
        accelTimestamps = o.synchronisedAccelRTC
        magTimestamps = o.synchronisedMagRTC

    gyroVectors = o.gyroVectors
    accelVectors = o.accelVectors
    magVectors = o.magVectors

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
#show()

data_array = data_array[data_array[:,1].argsort()]

savetxt(FILE+".csv", data_array, delimiter=',')
exit()


