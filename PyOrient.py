
import struct
import time
import usb.core

class Sample(object):
    FORMAT = "<BBBHHHhhhhhhhhh"
    NBYTES = struct.calcsize(FORMAT)

    def __init__(self, buf, offset):
        tpl = struct.unpack_from(Sample.FORMAT, buf, offset)

        self.node_id = tpl[0]
        self.last_sequence_no = tpl[1]
        self.status = tpl[2]
        self.gyro_tick = tpl[3]
        self.accel_tick = tpl[4]
        self.mag_tick = tpl[5]
        self.gyro_vector = (tpl[6], tpl[7], tpl[8])
        self.accel_vector = (tpl[9], tpl[10], tpl[11])
        self.mag_vector = (tpl[12], tpl[13], tpl[14])
	
class Orient(object):
    VID = 0xffff
    PID = 0x0001

    INTERFACE = 0
    ENDPOINT = 0x80 | 1

    CONFIG_READ = 0
    CONFIG_WRITE = 1
    MASTER_START = 2
    MASTER_STOP = 3

    def __init__(self):
        self.dev = usb.core.find(idVendor=Orient.VID, idProduct=Orient.PID)

        if self.dev == None:
            raise Exception("Orient device is not connected")

    def start(self, num_devices, capture_id):
        val = (capture_id << 8) | num_devices

        self.dev.ctrl_transfer(bmRequestType=0x41, \
            bRequest=Orient.MASTER_START, \
            wValue=val, \
            wIndex=Orient.INTERFACE)

    def stop(self):
        self.dev.ctrl_transfer(bmRequestType=0x41, \
            bRequest=Orient.MASTER_STOP, \
            wIndex=Orient.INTERFACE)

        time.sleep(0.01)

    # N.B. Sleep at least a few msec between calls to this method
    def read(self):
        chunk = self.dev.read(Orient.ENDPOINT, Sample.NBYTES * 128).tostring()

        nrecords = len(chunk) / Sample.NBYTES
        result = list()

        for i in range(0, nrecords):
            record = Sample(chunk, i * Sample.NBYTES)
            result.append(record)

        return result

#
# Sample code
#

if __name__ == '__main__':
    print "Connecting to Orient"
    ori = Orient()

    print "Starting 16-node capture"
    ori.start(16, 0)

    try:
        while True:
            samples = ori.read()

            if len(samples) > 0:
                print [x.node_id for x in samples]

            time.sleep(0.01)

    except KeyboardInterrupt:
        print "Got Ctrl-C, shutting down"

    print "Stopping Orient"
    ori.stop()

