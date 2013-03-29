__author__ = 'Robert Evans'

import dtw
import plot
import progressbar
from multiprocessing import Pool, Lock
lock = Lock()

def averageSimilarityMatrix(dictOfClassesLocal, dictOfWeightsLocal,title="Cluster similarity matrix",savePlot=False):
	global bar, progressCount, dictOfClasses, dictOfWeights, arguments, distances
	dictOfClasses = dictOfClassesLocal
	dictOfWeights = dictOfWeightsLocal
	bar = progressbar.ProgressBar(maxval=len(dictOfClasses.keys())**2, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()
	progressCount = 0

	# Initialise task matrix
	arguments = []
	distances = []
	for i,k in zip(range(len(dictOfClasses.keys())),reversed(sorted(dictOfClasses.keys()))):
		arguments.append([])
		distances.append([])
		for j in sorted(dictOfClasses.keys()):
			arguments[i].append((dictOfClasses[k],dictOfClasses[j],dictOfWeights[k],dictOfWeights[j]))
			distances[i].append([])

	# Distribute tasks
	poo = Pool()
	for i in range(len(dictOfClasses.keys())**2):
		poo.apply_async(interClassDistance,(i,),callback=updateResultMatrix)
	poo.close()
	poo.join()

	bar.finish()
	plot.plotSimilarityMatrix(distances,sorted(dictOfClasses.keys()),title,savePlot)

def interClassDistance(taskIndex):
	(classA,classB,classAweights,classBweights) = arguments[taskIndex/len(dictOfClasses.keys())][taskIndex%len(dictOfClasses.keys())]
	summedDistances = 0
	for a,aw in zip(classA,classAweights):
		for b,bw in zip(classB,classBweights):
			weights = [float(sum(t))/float(len(t)) for t in zip(aw,bw)]
			summedDistances += dtw.getDTWdist2DweightedSum(a,b,weights)
	averageDistance = summedDistances / (len(classA)*len(classB))
	return (taskIndex,averageDistance)

def updateResultMatrix(returnTuple):
	global progressCount
	lock.acquire()
	distances[returnTuple[0]/len(dictOfClasses.keys())][returnTuple[0]%len(dictOfClasses.keys())] = returnTuple[1]
	progressCount += 1
	bar.update(progressCount)
	lock.release()