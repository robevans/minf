__author__ = 'Rat'

from OrientDataset import *
from numpy import where

filename = "ID_live1.log"
pc = OrientPCDataset("../ScottishBallet/finalCapture/pcCaptures/" + filename)

allLineNos = pc.getAllLineNumbers()
allrbs = pc.allRawBsRTC()
allbs, allbswraps = pc.allBsRTC()



for i in pc.IDs():
    lineNos = pc.getLineNumbers(i)
    rbs = pc.rawBsRTC(i)
    bs = pc.bsRTC(i)
    bsc = zeros(shape(bs))
    ids = pc.IDField()

    #for j in range(len(lineNos)):
    #    l = lineNos[j]
    #    k = where(allLineNos==l)[0][0]
    #    w = allbswraps[k]

    #    bsc[j] = rbs[j] + (48000 * w)


    #figure()
    #plot(allLineNos, allrbs)
    #plot(lineNos, rbs)

    #figure()
    #plot(allLineNos, allbs)
    #plot(lineNos, bs)

    #figure()
    #plot(allLineNos, allbs)
    #plot(lineNos, bsc)


    grtc = pc.gyroRTC(i)
    grrtc = pc.rawGyroRTC(i)

    figure()
    plot(grtc)
    plot(pc.gyroRTCnew(i))
    plot(pc.oldBsRTC(i))
    plot(bs)

    show()
