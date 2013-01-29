__author__ = 'Andrew'
#from OrientDataset import *
from scipy.interpolate import splrep, splev
from graph import *

def syncOffset(nodeTimestamps, bsTimestamps):
    correctedNodeTimestamps = unwrapTimestamps(nodeTimestamps)[0]
    correctedBsTimestamps = unwrapTimestamps(bsTimestamps)[0]
    #correctedSdGyroTimestamps = unwrapTimestamps(sdGyroTimestamps)

    #figure()
    #plot(correctedNodeTimestamps)
    #plot(correctedBsTimestamps)


    diffs = correctedBsTimestamps - correctedNodeTimestamps
    syncCorrection = int(round(mean(diffs)))

    #plot(correctedNodeTimestamps + syncCorrection)
    #show()

    #figure()
    #plot(correctedBsTimestamps - (correctedNodeTimestamps + syncCorrection))
    #show()

    return syncCorrection

def unwrapTimestamps(timestamps, correction_increment=48000):
    correctedTimestamps = copy(timestamps)
    wraps = zeros(shape(timestamps))
    # correct rtc overflow
    correction = 0
    wrap_count = 0
    for i in range(1,len(correctedTimestamps)):
        correctedTimestamps[i] += correction
        wraps[i] = wrap_count
        if correctedTimestamps[i] < correctedTimestamps[i-1]:
            decrease = correctedTimestamps[i-1]-correctedTimestamps[i]
            if decrease < 24000:
                print "SMALL DECREASE CAUSING WRAP: " + str(decrease)
            correction += correction_increment
            wrap_count += 1
            correctedTimestamps[i] += correction_increment
            wraps[i] = wrap_count
    return correctedTimestamps, wraps


def unwrapTimestampsUseSeqNumbers(timestamps, seqs, correction_increment=48000):

    def meanTimePerSeq(timestamps, seqs):
        # first calculate the mean timestamp increase when the seq number increases by 1.
        prevSeq = seqs[0]
        prevTime = timestamps[0]
        increases = []
        for i in range(1, len(seqs)):
            if seqs[i] - prevSeq == 1:
                if timestamps[i] > prevTime:
                    increases.append(timestamps[i] - prevTime)
            prevSeq = seqs[i]
            prevTime = timestamps[i]
        return mean(increases)

    wraps = zeros(shape(timestamps))
    timePerSeq = meanTimePerSeq(timestamps, seqs)
    print timePerSeq
    wrap_count = 0

#    seqDiffs = []
#    for i in range(1,len(timestamps)):
#        seqDiff = seqs[i] - seqs[i-1]
#        if seqDiff < 1:
#            seqDiff += 256
#        seqDiffs.append(seqDiff)
#
#    figure()
#    plot(seqDiffs)
#    show()

    for i in range(1,len(timestamps)):
        seqDiff = seqs[i] - seqs[i-1]
        if seqDiff < 1:
            seqDiff += 256

        if seqDiff == 1:
            if timestamps[i] < timestamps[i-1]:
                wrap_count += 1
                wraps[i] = wrap_count
            else:
                wraps[i] = wrap_count
        else:
            estimatedTimeJump = timePerSeq * seqDiff
            newEstimatedTime = timestamps[i-1] + estimatedTimeJump

            # now add wrap increments to get closest to the new estimated time (may not require any)
            newTime = timestamps[i]
            newWraps = 0
            diffFromEstimated = abs(newTime-newEstimatedTime)

            for j in range(1,10):
                nt = timestamps[j] + (correction_increment * j)
                if abs(nt - newEstimatedTime) < diffFromEstimated:
                    newWraps = j
                    diffFromEstimated = abs(nt - newEstimatedTime)
                    print j

            wrap_count += newWraps
            wraps[i] = wrap_count

    correctedTimestamps = empty(shape(timestamps))
    for i in range(len(timestamps)):
        correctedTimestamps[i] = timestamps[i] + (wraps[i] * correction_increment)

    return correctedTimestamps, wraps

def unwrapTimestampsUseHash(pct, pcd, sdt, sdd, correction_increment=48000):
    # SD data should not have any gaps, so use this to detect timestamp wraps in the PC data when there's packet loss.
    # SD data is higher sample rate than PC data, so looking always looking forward for next match should work.

    sdi = 0
    for pci in range(len(pcd)):
        pch = hash(tuple(pcd[:,pci].tolist()))
        for sdj in range(sdi, len(sdd)):
            sdh = hash(tuple(sdd[:,sdj].tolist()))




class WrapCorrection():
    def __init__(self, sd, pc, correction_increment=48000):
        self.sd=sd
        self.pc=pc
        self.correction_increment=correction_increment
        self.wrap_corrections = dict()
        for id in sd.IDs:
            if id in pc.IDs():
                self.wrapCorrection(id)

    def wrapCorrection(self, id):
        sdgt = self.sd.devices[id].synchronisedGyroRTC
        sdgx = self.sd.devices[id].gyroVectors[:,0]
        sdat = self.sd.devices[id].synchronisedAccelRTC
        sdax = self.sd.devices[id].accelVectors[:,0]
        sdmt = self.sd.devices[id].synchronisedMagRTC
        sdmx = self.sd.devices[id].magVectors[:,0]

        pcgt = self.pc.lossCorrectedSynchronisedGyroRTC(id)
        pcgx = self.pc.gyroVectors(id)[:,0]
        pcat = self.pc.lossCorrectedSynchronisedAccelRTC(id)
        pcax = self.pc.accelVectors(id)[:,0]
        pcmt = self.pc.lossCorrectedSynchronisedMagRTC(id)
        pcmx = self.pc.magVectors(id)[:,0]

        gyro_correction = self.sensorWrapCorrection(sdgt,sdgx,pcgt,pcgx)
        accel_correction = self.sensorWrapCorrection(sdat,sdax,pcat,pcax)
        mag_correction = self.sensorWrapCorrection(sdmt,sdmx,pcmt,pcmx)

        self.wrap_corrections[id] = (gyro_correction, accel_correction, mag_correction)

    def sensorWrapCorrection(self, sdt, sdv, pct, pcv):

        offsets = range(-3,4)
        corrs = empty(shape(offsets))

        for i in range(len(offsets)):
            # spline fit SD data
            shifted_sd_timestamps = sdt + (offsets[i] * self.correction_increment)

            start = max(shifted_sd_timestamps[0], pct[0])
            end = min(shifted_sd_timestamps[-1], pct[-1])

            j = 0
            while pct[j] < start:
                j += 1
            first = j

            j = -1
            while pct[j] > end:
                j -= 1
            last = j

            tck_sd, fp_sd, ier_sd, msg_sd = splrep(shifted_sd_timestamps,sdv, full_output=True)

            #trimmed timestamps for evaluation
            trimmed_pct = pct[first:last]

            spline_sd_data = splev(trimmed_pct, tck_sd)

            # calculate correlation
            #figure()
            #plot(trimmed_pct,pcv[first:last])
            #plot(trimmed_pct, spline_sd_data)
            #show()
            corrs[i] = corrcoef(pcv[first:last], spline_sd_data)[0][1]
            print corrs[i]


        #figure()
        #plot(corrs)
        #show()


        # pick the offset that gives the best correlation
        best_index = argmax(corrs)
#        if max(corrs) < 0.99:
        #            print "possible sync problem. Best correlation: " + str(max(corrs))
        #            shifted_sd_timestamps = sdt + (offsets[best_index] * self.correction_increment)
        #            tck_sd, fp_sd, ier_sd, msg_sd = splrep(shifted_sd_timestamps,sdv, full_output=True)
        #            spline_sd_data = splev(pct, tck_sd)
        #            figure()
        #            plot(pcv)
        #            plot(spline_sd_data)
        #            show()

        return offsets[best_index] * self.correction_increment





#def manualSyncCorrection(id, correction_increment=48000, sensor=''):
#    if id in manual_sync_correction:
#        if sensor=='gyro':
#            correction = manual_sync_correction[id][0]
#        elif sensor=='accel':
#            correction = manual_sync_correction[id][1]
#        elif sensor=='mag':
#            correction = manual_sync_correction[id][2]
#        else:
#            correction = None
#    else:
#        correction = 0
#    #print manual_sync_correction[id]
#    #print correction_increment
#    #print type(correction_increment)
#    return correction * correction_increment

if __name__ == "__main__":
    if __name__ == "__main__":
        sd = OrientSDDataset2("../ScottishBallet/finalCapture/sdCaptures", "ID_RUN01.LOG",devices=[1,16])
        pc = OrientPCDataset("../ScottishBallet/finalCapture/pcCaptures/ID_run01.log")
        sd.synchroniseDataset("../ScottishBallet/finalCapture/pcCaptures/ID_run01.log")



