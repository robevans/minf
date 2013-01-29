'''
Created on 4 Oct 2010

@author: Andrew
'''

from util import *
from matplotlib.transforms import Bbox

def graph(*args, **kwargs):
    sampleRate = default('sampleRate', 32, **kwargs)
    showTime = default('showTime', True, **kwargs)
    showLegend = default('showLegend', True, **kwargs)
    noLine = default('noLine', False, **kwargs)
    title = default('title', '', **kwargs)
    xLabel = default('xLabel', '', **kwargs)
    linkAxes = default('linkAxes', True, **kwargs)
    fig = default('fig', None, **kwargs)
    figSize=default('figSize', None, **kwargs)
    unlinked=default('unlinked', 0, **kwargs)
    xData = default('xData', None, **kwargs)
    n_subplots = len(args)
    #print args
    
    if fig == None:
        if figSize is None:
            fig = figure()
        else:
            fig = figure(figsize=figSize)
    else:
        clf()
        
    if 'title' in kwargs:
        fig.canvas.set_window_title(title)
    
    l = findLength(args[0])
    
    if showTime:
        xDataSecs = array(range(l)) / float(sampleRate )
        xDataMins = xDataSecs / float(60)
        xDataHours = xDataSecs / float(3600)
    
        xData = xDataHours
        xLabel = "Time (hours)"
        if xData[-1] < 10.0:
            xData = xDataMins
            xLabel = "Time (mins)"
            if xData[-1] < 3.0:
                xData = xDataSecs
                xLabel = "Time (seconds)"
    else:
        if xData is None:
            xData = array(range(l))

    
    global legendCount, nextColour
    legendCount = 1
    nextColour = 0
    
    i = 1
    
    for arg in args:
        if i == 1:
            sp = fig.add_subplot((100 * n_subplots) + 11, title=title)
            sp1 = sp
        else:
            if linkAxes:
                sp = fig.add_subplot((100 * n_subplots) + 10 + i, sharex=sp1)
            else:
                sp = fig.add_subplot((100 * n_subplots) + 10 + i)
            #sp.set_xlabel(xLabel)
        if i == len(args):
            sp.set_xlabel(xLabel)
            
        if type(arg) == type(tuple()):
            sp_twin = sp.twinx()
            graphSeries(arg[0], sp, xData=xData, noLine=noLine, showLegend=showLegend)
            if len(arg) > 1:
                graphSeries(arg[1], sp_twin, twin=True, xData=xData, noLine=noLine, showLegend=False)
        else:
            graphSeries(arg, sp, xData=xData, noLine=noLine, showLegend=showLegend)        
        i += 1
    #draw()
    return fig
        
def graphSeries(arg, sp, twin=False, xData=None, noLine=False, showLegend=True):
    #twin_colours = ['c','m','y']
    global legendCount
    legend = []
    legendSuffix=['x','y','z']
    loc = 'upper left'
    if twin:
        #colours = twin_colours
        loc = 'upper right'
  
    if type(arg) == type(dict()):
        for k in arg:
            n = plotArray(arg[k], sp, xData=xData, noLine=noLine)
            if n == 1:
                legend.append(str(legendCount) + ": " + k)
            else:
                for j in range(n):
                    legend.append(str(legendCount) + ": " + k + "(" + legendSuffix[j] + ")")
            legendCount += 1
    elif type(arg) == type(list()):
        for j in range(len(arg)):
            n = plotArray(arg[j], sp, xData=xData, noLine=noLine)
            if n == 1:
                legend.append(str(legendCount))
            else:
                for k in range(n):
                    legend.append(str(legendCount) + "(" + legendSuffix[k] + ")")
            legendCount += 1
    else:
        n = plotArray(arg, sp, xData = xData, noLine=noLine)
        if n == 1:
            legend.append(str(legendCount))
        else:
            for j in range(n):
                legend.append(str(legendCount) + "(" + legendSuffix[j] + ")")
        legendCount += 1
    if showLegend:
        sp.legend(legend, loc)

def plotArray(a, s, xData=None, noLine=False):
    
    global nextColour
    if len(shape(a)) == 0:
        if noLine:
            c = getNextColour()
            m = lookupMarker(c)
            doPlot(s, xData, createSeries(a, len(xData)), c, drawLine=False, marker=m)
        else:
            doPlot(s, xData, createSeries(a, len(xData)), getNextColour())
        return 1
    elif len(shape(a)) == 1:
        # if zero column array
        if noLine:
            c = getNextColour()
            m = lookupMarker(c)
            doPlot(s, xData, a, c, drawLine=False, marker=m)
        else:
            doPlot(s, xData, a, getNextColour())
        return 1
    else:
        n = shape(a)[1]
        for i in range(n):
            if noLine:
                c = getNextColour()
                m = lookupMarker(c)
                doPlot(s, xData, a[:,i], c, drawLine=False, marker=m)
            else:
                doPlot(s, xData, a[:,i], getNextColour())
        return n

def doPlot(s, xData, a, c, drawLine=True, marker=None):
    if not all(amap(isnan,a)):
        if drawLine:
            s.plot(xData, a, c)
        else:
            s.plot(xData, a, c, ls='None', marker=marker)
        
def findLength(arg):
    if type(arg) == type(tuple()) or type(arg) == type(list()):
        return findLength(arg[0])
    elif type(arg) == type(dict()):
        return findLength(arg[arg.keys()[0]])
    else:
        return len(arg)
    
def getNextColour():
    global nextColour
    colours = ['r','g','b', 'c', 'm', 'y','k','r','g','b', 'c', 'm', 'y','k','r','g','b', 'c', 'm', 'y','k','r','g','b', 'c', 'm', 'y','k','r','g','b', 'c', 'm', 'y','k','r','g','b', 'c', 'm', 'y','k']
    c = colours[nextColour]
    nextColour += 1
    return c

def lookupMarker(c):
    dict={'r':'o', 
          'g':'*',
          'b':'+',
          'c':'x',
          'm':'D',
          'y':'s',
          'k':'v'}
    
    return dict[c]
    

#a = array(range(10))
#x = array(range(2,12))
#graph(a, showTime=False, xData = x)
#show()

        
#a = array([1,2,3,4,5])
#b = array([6,7,8,9,10])
#c = zeros((5,2))
#c[:,0] = a
##c[:,1] = b
#d = array([-1,-2,-3,-4,-5])
#e = array([-6,-7,-8,-9,-10])
#g = [a,b,d,e]
#show()

#b = 7

#graph(a,b, noLine=True, figSize=(15,10))
#savefig('test.pdf', bbox_inches=Bbox.from_bounds(0,0,5,5))
#savefig('test.pdf')
#show()