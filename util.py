from pylab import *
import scipy.signal
from scipy.signal import filtfilt, lfilter
from scipy.signal.filter_design import butter
from quat import Quat

''' Create an array of NaN values with the specified dimensions. '''
def nans(dims):
    a = empty(dims)
    a[:] = nan
    return a

''' Find the RMS value of an input signal in array form. '''
def rms(signal):
    return sqrt(mean(signal**2))

def rmsHamming(signal):
    squares = signal**2
    weights = hamming(len(signal))
    weightedSum = 0.0
    weightsSum = 0.0

    for i in range(len(signal)):
        weightedSum += squares[i] * weights[i]
        weightsSum += weights[i]

    return sqrt(weightedSum / weightsSum)


def rmsPosNeg(signal):
    posValues = []
    negValues = []
    for i in range(len(signal)):
        if signal[i] >= 0:
            posValues.append(signal[i])
        elif signal[i] < 0:
            negValues.append(signal[i])
    posArray = array(posValues)
    negArray = array(negValues)
    posRMS = sqrt(mean(posArray**2))
    negRMS = -sqrt(mean(negArray**2))
    return posRMS, negRMS

''' Compute the dot products of two arrays of vectors. '''
def adot(a, b):
    return (a*b).sum(axis=1)

''' Combine the contents of two dictionaries into one. '''
def combineDicts(d1, d2):
    d = d1.copy()
    for key in d2.keys():
        d[key] = d2[key]
    return d

''' Create a function by composition of a list of other functions.

    The last function in the array should take no non-keyword arguments.
    Any previous functions should take the function on which they operate
    as their sole non-keyword argument. '''
def compose(functions, **kwargs):
    if len(functions) == 1:
        return lambda **kw: functions[0](**combineDicts(kwargs,kw))
    else:
        return lambda **kw: functions[0](compose(functions[1:], **combineDicts(kwargs,kw)), **combineDicts(kwargs,kw))

''' Find islands of defined values in a signal that may contain NaNs. '''
def findIslandLimits(signal, minIslandLength=0, minIslandGap=0):

    islands = []

    start = None
    end = None
    foundIsland = False

    for i in range(len(signal)):
        if not signal[i]:
            if start == None:
                start = i
            else:
                end = i + 1
                if i == len(signal) - 1:
                    foundIsland = True
        else:
            if start != None:
                if end != None:
                    foundIsland = True
                else:
                    start = None

        if foundIsland:
            if (minIslandGap > 0) and (len(islands) > 0):
                prevIslandStart = islands[-1][0]
                prevIslandEnd = islands[-1][1]
                islandGap = start - prevIslandEnd - 1
                if islandGap < minIslandGap:
                    # merge the new island with the previous one
                    islands[-1] = ((prevIslandStart, end))
                else:
                    islands.append((start, end))
            else:    
                islands.append((start, end))

            start = None
            end = None
            foundIsland = False
            
    # now return only the islands that are long enough
    longIslands = []
    for island in islands:
        if (island[1] - island[0]) >= minIslandLength:
            longIslands.append(island)

    return longIslands

def firstValidIndex(signal):
    for i in range(len(signal)):
        if not isnan(signal[i]):
            return i
        
def lastValidIndex(signal):
    for i in reversed(range(len(signal))):
        if not isnan(signal[i]):
            return i

def default(k, v, **kwargs):
    if k in kwargs:
        return kwargs[k]
    else:
        return v
    
def ramp(func, arg, start, end, step, **kwargs):
    results = []
    args = []
    
    for i in range(start, end, step):
        kwargs[arg] = i
        args.append(i)
        results.append(func(**kwargs))
        
    return args,results

def compareAnalog(orient=None, cannula=None, **kwargs):
    if orient is None or cannula is None:
        return nan
    o = orient.breathingSignal(**kwargs)
    c = cannula.processedAnalogSignal(**kwargs)[:,0]
    limits = findIslandLimits(isnan(o))
    corrs = []
    for start,end in limits:
        poly = polyfit(o[start:end],c[start:end],1)
        scale = poly[0]
        offset = poly[1]
        c = (c - offset) / scale
        corrs.append(corrcoef(o[start:end], c[start:end])[0,1])
        
    return corrs

def createSeries(v, l):
    s = zeros((l,))
    s[:] = v
    return s

def createVectorSeries(v, l):
    s = zeros((l,3))
    s[:] = v
    return s

def mode(l):
    if len(l) == 0:
        return NaN, {}, []
    
    sortedRoundedArray = sort(around(l))
    dict = {}
    dist = zeros(sortedRoundedArray[-1] + 1)
    maxCount = 0
    for e in sortedRoundedArray:
        dist[e] += 1
        if e in dict:
            newCount = dict[e] + 1
            dict[e] = newCount
        else:
            newCount = 1
            dict[e] = newCount
            
        if newCount > maxCount:
                maxCount = newCount
    
    if maxCount > 0:
        l = []
        for e in dict:
            if dict[e] == maxCount:
                l.append(e)
        sorted = sort(l)
        return sorted[len(sorted) // 2], dict, dist
                
    else:
        return NaN, dict, dist
    
def aand(a,b):
    result = array(len(a))
    for i in range(len(result)):
        result[i] = a[i] and b[i]
    return result

def aor(a,b):
    result = empty((len(a), 1))
    for i in range(len(result)):
        result[i] = a[i] or b[i]
    return result

def flattenRates(rates):
        flattenedRates = []
        for bi in rates:
            fr = []
            for ri in bi:
                fr.extend(ri)
            flattenedRates.extend(fr)
        return flattenedRates
    
def flattenList(l):
    result = []
    for e in l:
        result.extend(e)
    return result
    
def fileOutput(h, t, fname, fmt=None):
    f = open(fname, 'w')
    for i in range(len(h)):
        f.write(h[i][0] + "," + str(h[i][1]) + "\n")
    f.write("\n")
    
    # write header line
    first = True
    header = ""
    for e in t:
        if first:
            first = False
        else:
            header += ","
        header += str(e[0])
    header += "\n"
    
    f.write(header)
    f.close()
    
    lines = len(t[0][1])
    cols = len(t)
    
    data = empty((lines, cols))
    
    for i in range(cols):
        print t[i][0]
        print shape(t[i][1])
        data[:,i] = t[i][1]        
    
    #print data
    
    f2 = open(fname, 'a')
    if fmt is None:
        savetxt(f2, data, delimiter=",")
    else:
        savetxt(f2, data, delimiter=",", fmt=fmt)
    f2.close()
    
def noBananas(l):
    result = []
    for i in l:
        if not isnan(i):
            result.append(i)
    return result
    
def ci95(l):
    m = mean(l)
    sd = std(l)
    
    return m - 1.96 * sd, m + 1.96 * sd

def principleComponent(data):
    import mdp
    pcaNode = mdp.nodes.PCANode()
    pcaNode.train(data)
    pcaNode.stop_training()
    return pcaNode.get_projmatrix()[:,0]

def angle(a,b):
    return arccos(dot(a,b) / (l2norm(a) * l2norm(b)))

def lowpass(signal, order, cutoff, sr):
    b,a = butter(order, cutoff/(sr/2))
    filteredSignal = nans(shape(signal))

    if len(signal) <= 3 * max(len(a), len(b)):
        print "signal too short to be lowpassed: " + str(len(signal))
        return nans(shape(signal))

    for i in range(shape(signal)[1]):
        filteredSignal[:,i] = filtfilt(b,a,signal[:,i])
            
    return filteredSignal
    
def quatFromVectors(s,d):
    s = s / l2norm(s)
    d = d / l2norm(d)
    v = s + d
    v /= l2norm(v)
    c = cross(v, d)

    q = Quat(dot(v, d),c[0],c[1],c[2])

    return q

def invalidate(data, invalid):
    result = copy(data)
    for i in range(len(data)):
        #print invalid[i]
        if invalid[i]:
            result[i] = NaN
    return result

def listdirs(folder):
    import os
    return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
