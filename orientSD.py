__author__ = 'Andrew'
import struct
from numpy import empty, append
from matplotlib.pyplot import plot, show
from orientSync import *

IGNORE_LINES = 30

class OrientSD:
    def __init__(self, filename):
        f = open(filename, 'rb')
        line = f.read(11)
        self.ID = None
        self.accelVectors = empty((0,3),dtype=int)
        self.gyroVectors = empty((0,3),dtype=int)
        self.magVectors = empty((0,3),dtype=int)
        self.rawAccelRTC = empty((0,),dtype=int)
        self.rawGyroRTC = empty((0,),dtype=int)
        self.rawMagRTC = empty((0,),dtype=int)
        self.accelRTC = None
        self.gyroRTC = None
        self.magRTC = None
        self.synchronisedAccelRTC = None
        self.synchronisedGyroRTC = None
        self.synchronisedMagRTC = None

        IDs = set()
        line_number = 0

        while line:
            (header, packetid, nodeid, time, x, y, z) = struct.unpack(">cBBHhhh", line)
            if packetid==0:
                #print len(line[6:])
                (x, y, z) = struct.unpack("<hhh", line[5:])
            if line_number > IGNORE_LINES:
                if header == '*':
                    if nodeid not in IDs:
                        IDs.add(nodeid)
                    if packetid == 0:
                        self.gyroVectors = append(self.gyroVectors,[[-y,-x,-z]],axis=0)
                        self.rawGyroRTC = append(self.rawGyroRTC,time)
                    elif packetid == 1:
                        self.accelVectors = append(self.accelVectors,[[x,y,z]],axis=0)
                        self.rawAccelRTC = append(self.rawAccelRTC,time)
                    elif packetid == 2:
                        self.magVectors = append(self.magVectors,[[x,y,z]],axis=0)
                        self.rawMagRTC = append(self.rawMagRTC,time)
            line_number += 1
            line = f.read(11)

        # check IDs
        if len(IDs) == 1:
            self.ID = IDs.pop()
            print "device ID: " + str(self.ID)
        else:
            print "multiple device IDs found"

        self.accelRTC = unwrapTimestamps(self.rawAccelRTC)[0]
        self.gyroRTC = unwrapTimestamps(self.rawGyroRTC)[0]
        self.magRTC = unwrapTimestamps(self.rawMagRTC)[0]

    def applySyncOffset(self,offset):

        #man_sync = manualSyncCorrection(self.ID)
        #print "applying manual offset of " + str(man_sync) + " to device " + str(self.ID)

        total_offset = offset #+ man_sync
        print "applying sync offset of " + str(total_offset) + " to device " + str(self.ID)

        self.synchronisedAccelRTC = self.accelRTC + total_offset
        self.synchronisedGyroRTC = self.gyroRTC + total_offset
        self.synchronisedMagRTC = self.magRTC + total_offset

    def applyWrapCorrection(self,gyro, accel, mag):
        self.synchronisedAccelRTC = self.synchronisedAccelRTC + accel
        self.synchronisedGyroRTC = self.synchronisedGyroRTC + gyro
        self.synchronisedMagRTC = self.synchronisedMagRTC + mag


if __name__ == "__main__":
    o = OrientSD("../ScottishBallet/finalCapture/sdCaptures/01_ARM02.LOG")
    plot(o.gyroVectors)
    figure()
    plot(o.accelVectors)
    figure()
    plot(o.magVectors)
    show()
