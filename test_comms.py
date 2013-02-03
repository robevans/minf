__author__ = 'Rat'

from Queue import Queue
from comms import *
import serial

PACKET_SIZE = 42
MESSAGE_TYPE = 8
DEVICE_ID = 1

#q = Queue()
#c = CaptureThread("COM30", q)
#c.start()

#sleep(10)

f = serial.Serial("COM30", timeout=3.0)

while(True):
    while True:
        s = f.read(1)
        try:
            (eop,) = struct.unpack("c", s)
            if (eop == '*'):
                break
        except struct.error:
            print "no data from basestation"
    prevSEQ = 0
    while True:
        s = f.read(PACKET_SIZE)
        if len(s) == PACKET_SIZE:
            packet_system_time = time()
            (msgType,) = struct.unpack("B", s[0])

            if msgType == MESSAGE_TYPE:
                (nodeID,) = struct.unpack("B", s[1])
                if nodeID == DEVICE_ID:
                    (seqNumber,) = struct.unpack("B", s[2])
                    (accelRTC,) = struct.unpack(">h", s[3:5])
                    (gyroRTC,) = struct.unpack(">h", s[5:7])
                    (magRTC,) = struct.unpack(">h", s[7:9])
                    (accelX, accelY, accelZ) = struct.unpack(">hhh", s[9:15])
                    (gyroX, gyroY, gyroZ) = struct.unpack("<hhh", s[15:21])
                    (magX, magY, magZ) = struct.unpack("<hhh", s[21:27])

                    if (((prevSEQ + 1)%256) != seqNumber) and (prevSEQ != seqNumber):
                        print "unexpected seqNumber, ", msgType, ", ", nodeID, ", ", prevSEQ, ", ", seqNumber
                    prevSEQ = seqNumber

                    #self.queue.put((accelRTC, gyroRTC, magRTC, accelX, accelY, accelZ, gyroX, gyroY, gyroZ, magX, magY, magZ))
                    print magX, magY, magZ
            else:
                print "unknown message type"
        else:
            print "incorrect packet size"