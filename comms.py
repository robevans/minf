__author__ = 'Andrew'

import serial
import struct
import sys
from threading import Thread
from time import sleep, time
#from imusim.algorithms.orientation import OrientCF
#from imusim.maths.quaternions import *
#from imusim.algorithms.vector_observation import GramSchmidt
#from orientation import *
from pylab import array, l2norm
#from math import pi
#import socket
from findComPort import *

num_packets_recieved = 0

PACKET_SIZE = 42
MESSAGE_TYPE = 8
#DEVICE_ID = [1, 2, 3, 4, 5, 6,7,8,9,10,11,12,13]
#GYRO_SCALE = 70.0 / 1000.0


#
# Orient demo mode packet
#
#   1B	  1B   1B	   2B		2B     	   2B			 6B	   			  6B				6B
# +----+----+----+----+----+----+----+----+----+----+- ... -+----+----+- ... -+----+----+- ... -+----+
# |TYPE| ID |SEQ#|ACCEL_RTC|GYRO_RTC |MAGNE_RTC|  	ACCEL_VALUE   |    GYRO_VALUE	|  MAGNETO_VALUE  |
# +---------+----+----+----+----+----+----+----+----+- ... -+----+----+- ... -+----+----+- ... -+----+
#	 00	  01   02	03	 04	  05   06   07   08   09   		   14	15			 20	  21		   26
#

NODE_ID, ACCEL_RTC, GYRO_RTC, MAG_RTC, ACCEL, GYRO, MAG = range(7)

class CaptureThread(Thread):
    def __init__(self, callback, filename="ID_test0.log", time_mins=0.5, send_freq=3, cal_id=0):
        if len(filename) <> 12 or filename[8] <> '.':
            print "SD filename must be 8.3 format"
            exit(1)
        self.filename = filename
        self.capture_time_mins = time_mins
        self.send_freq = send_freq
        self.cal_id = cal_id
        self.handleData = callback
        self.f = open(filename, 'w')
        s = "type,ID,seq,accelRTC,gyroRTC,magRTC,accelX,accelY,accelZ,gyroX,gyroY,gyroZ,magX,magY,magZ,bsRTC\n"
        self.f.write(s)
        super(CaptureThread, self).__init__()
        self.stop = False

    def run(self):

        while(True):
            try:
                #port = findComPort()
                port = '/dev/tty.usbmodem1411'
                if port is not None:
                    f = serial.Serial(port, timeout=3.0)
                    print "Basestation found at " + port
                    break
            except serial.SerialException:
                print "failed to open serial port. Retrying..."
            sleep(1)

        # send SD card filename and capture time (for orient)
        #f.write(SD_FILENAME)
        cap_time = self.capture_time_mins * 60 * 100
        print(struct.unpack(">12sBIBB", struct.pack(">12sBIBB",self.filename, 0, cap_time,self.send_freq, self.cal_id)))
        f.write(struct.pack(">12sBIBB",self.filename, 0, cap_time,self.send_freq,self.cal_id))
        f.flush()

        SEQByNodeID = dict()

        while(True):
            while True:
                s = f.read(1)
                #print s
                try:
                    (eop,) = struct.unpack("c", s)
                    if (eop == '*'):
                        break
                except struct.error:
                    print "no data from basestation"
                    sys.exit("Done")
            prevSEQ = 0
            num_packets_recieved = 0

            while True:
                s = f.read(PACKET_SIZE)
                #print s
                if len(s) == PACKET_SIZE:
                    (msgType,) = struct.unpack("B", s[0])

                    if msgType == MESSAGE_TYPE:
                        (nodeID,) = struct.unpack("B", s[1])
                        #print nodeID

                        (seqNumber,) = struct.unpack("B", s[2])
                        (accelRTC,) = struct.unpack(">H", s[3:5])
                        (gyroRTC,) = struct.unpack(">H", s[5:7])
                        (magRTC,) = struct.unpack(">H", s[7:9])
                        (accelX, accelY, accelZ) = struct.unpack(">hhh", s[9:15])
                        (gyroX, gyroY, gyroZ) = struct.unpack("<hhh", s[15:21])
                        (magX, magY, magZ) = struct.unpack(">hhh", s[21:27])
                        (bsRTC,) = struct.unpack(">H", s[27:29])
                        #print bsRTC

                        if nodeID in SEQByNodeID:
                            prevSEQ = SEQByNodeID[nodeID]
                            seqDiff = seqNumber - prevSEQ
                        else:
                            seqDiff = 1

                        if seqDiff < 0:
                            gyroFactor  = seqDiff + 256
                        else:
                            gyroFactor = seqDiff

                        SEQByNodeID[nodeID] = seqNumber

                        if seqDiff <> 0:
                            #print nodeID,
                            accel = array((float(accelX), float(accelY), float(accelZ)))
                            #accel /= 1024.0
                            gyro = array((float(-gyroY), float(-gyroX), float(-gyroZ)))
                            #gyro *= float(gyroFactor)
                            mag = array((float(magX), float(magY), float(magZ)))
                            #mag = array((float(0.0), float(0.0), float(1.0)))

                            self.latest_data = (nodeID, accelRTC, gyroRTC, magRTC, accel, gyro, mag)
                            #s = "type,ID,seq,accelRTC,gyroRTC,magRTC,accelX,accelY,accelZ,gyroX,gyroY,gyroZ,magX,magY,magZ\n"
                            self.f.write("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d%s"%(msgType,nodeID,seqNumber,accelRTC,gyroRTC,magRTC,accelX,accelY,accelZ,gyroX,gyroY,gyroZ,magX,magY,magZ,bsRTC,"\n"))
                            #if nodeID == 12:
                            #    print magRTC, magX, magY, magZ, gyroX, gyroY, gyroZ
                            self.handleData(self.latest_data)

                            num_packets_recieved = num_packets_recieved + 1
                            if num_packets_recieved > 1000:
                                self.stop=True
                            if self.stop:
                                break

                    else:
                        break
                        print "unknown message type", str(s)
                        break
                else:
                    print "incorrect packet size"
                    break

            if self.stop:
                break
            if num_packets_recieved > 1000:
                break

        f.close()
        self.f.close()

if __name__ == '__main__':

    def f(data):
            print data

    def g(data):
        if data[1] == 2056 and data[2] == 2056 and data[3] == 2056:
            print data

    class alive:
        def __init__(self):
            self.ids=[]
        def h(self,data):
            if data[0] not in self.ids:
                self.ids.append(data[0])
            print self.ids
            print len(self.ids)

    #a = alive()
    comms = CaptureThread(f)
    comms.start()
