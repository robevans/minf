__author__ = 'Andrew'

from threading import Thread
from numpy import array, shape, empty
from PyOrient import *
from time import sleep

NODE_ID, ACCEL_RTC, GYRO_RTC, MAG_RTC, ACCEL, GYRO, MAG = range(7)

class CaptureThread(Thread):
    def __init__(self, callback):
        self.handleData = callback
        print "Connecting to Orient"
        self.orient = Orient()
        print "Starting 16-node capture"
        self.orient.start(16,0)
        self.stop = False
        super(CaptureThread, self).__init__()



    def run(self):

        while not self.stop:
            samples = self.orient.read()
            #print "read"

            if len(samples) > 0:
                for s in samples:
                    nodeID = s.node_id
                    accelRTC = s.accel_tick
                    gyroRTC = s.gyro_tick
                    magRTC = s.mag_tick
                    accel = array(s.accel_vector)

                    gyro = array(s.gyro_vector, dtype=float)
                    accel = array(s.accel_vector, dtype=float)
                    mag = array(s.mag_vector, dtype=float)

                    """
                    # Corrections no longer needed after firmware update - it's all done orient side now
                    corrected_gyro = empty(shape(gyro))
                    corrected_gyro[0] = -gyro[1]
                    corrected_gyro[1] = -gyro[0]
                    corrected_gyro[2] = -gyro[2]
                    
                    corrected_accel = empty(shape(gyro))
                    corrected_accel[0] = accel[0]
                    corrected_accel[1] = accel[1]
                    corrected_accel[2] = accel[2]

                    corrected_mag = empty(shape(gyro))
                    corrected_mag[0] = mag[0]
                    corrected_mag[1] = mag[2]
                    corrected_mag[2] = mag[1]
                    """

                    latest_data = (nodeID, accelRTC, gyroRTC, magRTC, accel, gyro, mag)
                    self.handleData(latest_data)

            time.sleep(0.01)

        print "stopping"
        self.orient.stop()

if __name__ == '__main__':
    def printData(data):
        #if data[NODE_ID] is 8:
            print data
    def f(data):
        if data[NODE_ID] is 1:
            print data[ACCEL] / 8192.0

    def g(data):
        if data[NODE_ID] is 1:
            print data[GYRO][2] * 500.0 / pow(2,15)

    comms = CaptureThread(printData)
    comms.start()

    sleep(30)
    comms.stop=True