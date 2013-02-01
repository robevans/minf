__author__ = 'rat'

from comms import *
import socket
#from imusim.algorithms.orientation import OrientCF
#from imusim.maths.quaternions import *
#from imusim.algorithms.vector_observation import GramSchmidt
from orientation import *
from math import pi




######
#
# 6  calibration speck
#
# 21 lfoot
# 2  rfoot
#
#####


HOST = 'localhost'
PORT = 5555

COORD_CHANGE = Quaternion(0.5, -0.5, 0.5, 0.5)
GYRO_SCALE = 70.0 / 1000.0

CALIBRATION_FILES = [1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21]
CALIBRATION_PATH = "./calibration/"

CAPTURE_TIME=30
FILENAME="ID_wales.log"
SEND_FREQ = 4
DEVICE_ID=0 # 0 is all devices


class Panda:
    def __init__(self, live=True, sd=True, path=CALIBRATION_PATH, send_freq=SEND_FREQ):
        self.mag_calibrations = self.readCalibration(CALIBRATION_FILES, path)
        #print path
        #print self.mag_calibrations

        self.prevFrameTimestamp = 0

        self.orientationFilters = dict()
        for i in CALIBRATION_FILES:
            self.orientationFilters[i] = OrientCF(Quaternion(0,0,0,1),1.0,1.0)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.prevGyroTimestamps = dict()

        #if sd:
        #    self.gyro_interval = 499.0/46875.0
        #else:
        #    self.gyro_interval = 1.0/(100.0/send_freq)

        self.count = 0

        if live:
            self.gyro_interval = 1.0/(100.0/send_freq)
            c = CaptureThread(self.handleData,filename=FILENAME, time_mins=CAPTURE_TIME, send_freq=send_freq, cal_id=DEVICE_ID)
            c.start()

    def readCalibration(self,ids, path):
        result = dict()
        for id in ids:
            filename = path + str(id) + ".cal"
            #filename = "../ScottishBallet/finalCapture/calibration/" + str(id) + ".cal"
            try:
                f = open(filename, mode='r')
                f.readline()
                line = f.readline()
                cal = line.split(',')
                if id == int(cal[0]):
                    x_offset = float(cal[1])
                    x_scale = float(cal[2])
                    y_offset = float(cal[3])
                    y_scale = float(cal[4])
                    z_offset = float(cal[5])
                    z_scale = float(cal[6])

                    result[id] = ((x_offset,x_scale),(y_offset,y_scale),(z_offset,z_scale))
            except:
                print "failed to open calibration file for " + str(id)
                pass

        return result

    def handleData(self, data, returnQuat=False):
        #print "hello"

        self.count += 1

        accel = data[ACCEL]
        gyro = data[GYRO]
        mag = data[MAG]
        nodeID = data[NODE_ID]
        gyroRTC = data[GYRO_RTC]
        #print nodeID

        if nodeID in self.mag_calibrations:
            x_offset, x_scale = self.mag_calibrations[nodeID][0]
            y_offset, y_scale = self.mag_calibrations[nodeID][1]
            z_offset, z_scale = self.mag_calibrations[nodeID][2]

            magX = (float(mag[0]) - x_offset) * x_scale
            magY = (float(mag[1]) - y_offset) * y_scale
            magZ = (float(mag[2]) - z_offset) * z_scale

            mag = array([magX,magY,magZ]).reshape(-1,1)
            accel = array(accel,dtype='float')
            accel = accel.reshape(-1,1)
            gyro = array(gyro,dtype='float')
            gyro = gyro.reshape(-1,1)

            if nodeID in self.prevGyroTimestamps:
                gyro_interval = gyroRTC - self.prevGyroTimestamps[nodeID]
                if gyro_interval <= 0:
                    gyro_interval += 48000

                gyro_interval = float(gyro_interval) / 46875.0

                if (gyroRTC - self.prevFrameTimestamp) > (46875.0 / 25.0):
                    recordFrame = True
                    self.prevFrameTimestamp = gyroRTC
                else:
                    recordFrame = False

                #if self.count > 800 * 17:
                    #q = self.orientationFilters[nodeID].update(accel/1024.0, mag, gyro * GYRO_SCALE * pi / 180.0, gyro_interval, k=10.0, aT=0.5)
                    #print "new values"
                #else:
                q = self.orientationFilters[nodeID].update(accel/1024.0, mag, gyro * GYRO_SCALE * pi / 180.0, gyro_interval)
                if recordFrame:
                    self.sock.sendto("%d,%1.10f,%1.10f,%1.10f,%1.10f,%d"%(nodeID,q.w,q.x,-q.y,-q.z,1), (HOST, PORT))
                    print "frame " + str(gyroRTC)
                else:
                    self.sock.sendto("%d,%1.10f,%1.10f,%1.10f,%1.10f,%d"%(nodeID,q.w,q.x,-q.y,-q.z,0), (HOST, PORT))
                if returnQuat:
                    return q

            self.prevGyroTimestamps[nodeID] = gyroRTC

if __name__ == '__main__':
    panda = Panda()