__author__ = 'Rat'

from numpy import genfromtxt, column_stack, unique,array
from matplotlib.pyplot import plot, show
from util import listdirs, isInt
from os.path import exists, join
from os import listdir
from orientSD import *
from orientSync import unwrapTimestamps

#type,ID,seq,accelRTC,gyroRTC,magRTC,accelX,accelY,accelZ,gyroX,gyroY,gyroZ,magX,magY,magZ,bsRTC

#bsOffset = []
#bsOffset=[]

class OrientPCDataset:
    def __init__(self, filename):
        self.data = genfromtxt(filename, delimiter=',', names=True, skip_footer=1)

    def getField(self,id, field):
        return self.data[field][self.data['ID']==id]

    def getFieldAll(self, field):
        return self.data[field]

    def getFields(self,id,fields):
        return column_stack(self.data[v] for v in fields)[self.data['ID']==id,:]

    def accelVectors(self, id):
        l = ['accelX','accelY','accelZ']
        return self.getFields(id,l)

    def gyroVectors(self, id):
        l = ['gyroY','gyroX','gyroZ']
        return -self.getFields(id,l)

    def magVectors(self, id):
        l = ['magX','magY','magZ']
        return self.getFields(id,l)

    def rawAccelRTC(self,id):
        return self.getField(id,'accelRTC')

    def rawGyroRTC(self,id):
        return self.getField(id,'gyroRTC')

    def rawMagRTC(self,id):
        return self.getField(id,'magRTC')

    def seqNumbers(self,id):
        return self.getField(id,'seq')

    def rawBsRTC(self,id):
        return self.getField(id, 'bsRTC')

    def allRawBsRTC(self):
        return self.getFieldAll('bsRTC')

    # because of crap reception, we have to look at packets from all received devices to detect basestation wraps
    # for each node.

    def lossCorrectedBsRTC(self,id):
        allLineNos = self.getAllLineNumbers()
        allbs, allbswraps = self.allBsRTC()

        lineNos = self.getLineNumbers(id)
        rbs = self.rawBsRTC(id)
        bsc = zeros(shape(rbs))
        ids = self.IDField()

        for j in range(len(allLineNos)):
            if ids[j] == id:
                k = where(lineNos == allLineNos[j])[0][0]
                w = allbswraps[j]
                bsc[k] = rbs[k] + (48000 * w)
        return bsc

    def bsRTC(self,id):
        return unwrapTimestamps(self.rawBsRTC(id))[0]

    def allBsRTC(self):
        return unwrapTimestamps(self.allRawBsRTC())

    def messageTypes(self,id):
        return self.getField(id, 'messageTypes')

    def IDs(self):
        return sorted(array(unique(self.data['ID']),dtype='int').tolist())

    def IDField(self):
        return self.getFieldAll('ID')

    def gyroRTC(self, id):
        t =  unwrapTimestamps(self.rawGyroRTC(id))[0]
        #if id in bsOffset:
        #    return t + 48000
        #else:
        return t

    def lossCorrectedGyroRTC(self, id):
        return unwrapTimestampsUseSeqNumbers(self.rawGyroRTC(id), self.seqNumbers(id))[0]

    def accelRTC(self, id):
        return unwrapTimestamps(self.rawAccelRTC(id))[0]

    def lossCorrectedAccelRTC(self, id):
        return unwrapTimestampsUseSeqNumbers(self.rawAccelRTC(id), self.seqNumbers(id))[0]

    def magRTC(self, id):
        return unwrapTimestamps(self.rawMagRTC(id))[0]

    def lossCorrectedMagRTC(self, id):
        return unwrapTimestampsUseSeqNumbers(self.rawMagRTC(id), self.seqNumbers(id))[0]

    def synchronisedGyroRTC(self,id):
        return self.gyroRTC(id) + self.getSyncOffset(id)

    def synchronisedAccelRTC(self,id):
        return self.accelRTC(id) + self.getSyncOffset(id)

    def synchronisedMagRTC(self,id):
        return self.magRTC(id) + self.getSyncOffset(id)

    def lossCorrectedSynchronisedGyroRTC(self,id):
        return self.gyroRTC(id) + self.getSyncOffset(id)

    def lossCorrectedSynchronisedAccelRTC(self,id):
        return self.accelRTC(id) + self.getSyncOffset(id)

    def lossCorrectedSynchronisedMagRTC(self,id):
        return self.magRTC(id) + self.getSyncOffset(id)

    def getSyncOffset(self,id):
        return syncOffset(self.rawGyroRTC(id), self.rawBsRTC(id))

    def getLineNumbers(self,id):
        ids = self.data['ID']

        result = []
        for i in range(len(ids)):
            if ids[i] == id:
                result.append(i)
        return array(result)

    def getAllLineNumbers(self):
        ids = self.data['ID']
        return range(len(ids))




class OrientSDDataset:
    def __init__(self, root_path, filename):
        # get the list of subdirectories from the under the root path
        self.devices = dict()
        subdirs = listdirs(root_path)
        print subdirs
        for dir in subdirs:
            if 'Orient' in dir:
                f = join(root_path, dir, filename)
                print f
                if exists(f):
                    o = OrientSD(f)
                    id = o.ID
                    if id is not None:
                        self.devices[id] = o

        self.IDs = self.devices.keys()

    def synchroniseDataset(self, pc_filename):
        pc = OrientPCDataset(pc_filename)

        for id in self.devices:
            if id in pc.IDs():
                # get sync offset
                n = pc.gyroRTC(id)
                b = pc.bsRTC(id)
                offset = syncOffset(n,b)
                self.devices[id].applySyncOffset(offset)
                print "applying offset of " + str(offset) + " to device " + str(id)

class OrientSDDataset2:
    def __init__(self, root_path, filename, devices=None):
        # get the list of subdirectories from the under the root path
        self.devices = dict()
        #subdirs = listdirs(root_path)
        #print subdirs

        for file in listdir(root_path):
            if filename[2:] in file and isInt(file[0:2]):
                f = join(root_path, file)
                print f
                oid = file[0:2]
                if devices is None or int(oid) in devices:
                    o = OrientSD(f)
                    id = o.ID
                    if id is not None:
                        self.devices[id] = o

        self.IDs = self.devices.keys()

    def synchroniseDataset(self, pc_dataset):
        pc = pc_dataset

        for id in self.devices:
            if id in pc.IDs():
                # get sync offset
                n = pc.gyroRTC(id)
                b = pc.bsRTC(id)
                g = self.devices[id].gyroRTC
                offset = syncOffset(n,b)
                self.devices[id].applySyncOffset(offset)
                print "applying offset of " + str(offset) + " to device " + str(id)

    def wrapCorrectDataset(self, pc_dataset):
        wc = WrapCorrection(self,pc_dataset)
        corrections = wc.wrap_corrections
        for id in corrections:
            gyro = corrections[id][0]
            accel = corrections[id][1]
            mag = corrections[id][2]
            self.devices[id].applyWrapCorrection(gyro, accel, mag)

if __name__ == "__main__":
    filename = "ID_live1.log"
    sd = OrientSDDataset2("../ScottishBallet/finalCapture/sdCaptures", filename.upper())
    pc = OrientPCDataset("../ScottishBallet/finalCapture/pcCaptures/" + filename)
    sd.synchroniseDataset(pc)
    sd.wrapCorrectDataset(pc)

    #sg = sd.devices[15].synchronisedGyroRTC

    #diffs = empty(len(sg)-1,)
    #for i in range(1,len(sg)):
    #    diffs[i-1] = sg[i]-sg[i-1]

    #plot(diffs)
    #show()

    #figure()
    #plot(sd.devices[10].gyroRTC,sd.devices[10].gyroVectors)
    #plot(sd.devices[15].gyroRTC,sd.devices[15].gyroVectors)

    #figure()
    #plot(sd.devices[10].synchronisedGyroRTC,sd.devices[10].gyroVectors)
    #plot(sd.devices[15].synchronisedGyroRTC,sd.devices[15].gyroVectors)

    #figure()
    #plot(sd.devices[10].gyroRTC)
    #plot(sd.devices[10].synchronisedGyroRTC)

    #figure()
    #plot(sd.devices[15].gyroRTC)
    #plot(sd.devices[15].synchronisedGyroRTC)


    #pct9 = unwrapTimestamps(pc.gyroRTC(9))
    for i in sd.IDs:
        print i

        pcgst = pc.lossCorrectedSynchronisedGyroRTC(i)

        figure()
        plot(pcgst, pc.gyroVectors(i))
        plot(sd.devices[i].synchronisedGyroRTC,sd.devices[i].gyroVectors)




        figure()
        plot(pcgst, pc.rawGyroRTC(i))




        #figure()
        #plot(pc.lossCorrectedSynchronisedAccelRTC(i), pc.accelVectors(i))
        #plot(sd.devices[i].synchronisedAccelRTC,sd.devices[i].accelVectors)

        #figure()
        #plot(pc.lossCorrectedSynchronisedMagRTC(i), pc.magVectors(i))
        #plot(sd.devices[i].synchronisedMagRTC,sd.devices[i].magVectors)

        show()



#    for id in sd.IDs:
#        print id
#        figure()
#        plot(p.magVectors(id))
#        figure()
#        plot(sd.devices[id].magVectors)
#        show()

