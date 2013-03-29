__author__ = 'Robert Evans'

import dtw
import plot
import progressbar
from multiprocessing import Pool, Lock

def _pickle_method(method):
	func_name = method.im_func.__name__
	obj = method.im_self
	cls = method.im_class
	return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
	for cls in cls.mro():
		try:
			func = cls.__dict__[func_name]
		except KeyError:
			pass
		else:
			break
	return func.__get__(obj, cls)

import copy_reg
import types
copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)

lock = Lock()

class averageSimilarityMatrix():
	def __init__ (self, dictOfClasses, dictOfWeights,title="Cluster similarity matrix",savePlot=False):
		self.bar = progressbar.ProgressBar(maxval=len(dictOfClasses.keys())**2, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		self.bar.start()
		self.progressCount = 0
		self.dictOfClasses = dictOfClasses
		self.dictOfWeights = dictOfWeights

		# Initialise task matrix
		self.arguments = []
		self.distances = []
		for i,k in zip(range(len(self.dictOfClasses.keys())),reversed(sorted(self.dictOfClasses.keys()))):
			self.arguments.append([])
			self.distances.append([])
			for j in sorted(self.dictOfClasses.keys()):
				self.arguments[i].append((self.dictOfClasses[k],self.dictOfClasses[j],self.dictOfWeights[k],self.dictOfWeights[j]))
				self.distances.append([])

		# Distribute tasks
		poo = Pool()
		for i in xrange(1,300):
			j = range(len(self.dictOfClasses.keys())**2)
			poo.apply_async(self.interClassDistance,(j,),callback=self.updateResultMatrix)
		poo.close()
		poo.join()

		self.bar.finish()
		plot.plotSimilarityMatrix(distances,sorted(dictOfClasses.keys()),title,savePlot)

	def interClassDistance(taskIndex):
		(classA,classB,classAweights,classBweights) = arguments[taskIndex/len(self.dictOfClasses.keys())][taskIndex%len(self.dictOfClasses.keys())]
		summedDistances = 0
		for a,aw in zip(classA,classAweights):
			for b,bw in zip(classB,classBweights):
				weights = [float(sum(t))/float(len(t)) for t in zip(aw,bw)]
				summedDistances += dtw.getDTWdist2DweightedSum(a,b,weights)
		averageDistance = summedDistances / (len(classA)*len(classB))
		return (taskIndex,averageDistance)

	def updateResultMatrix(self, returnTuple):
		lock.acquire()
		distances[returnTuple[0]/len(self.dictOfClasses.keys())][returnTuple[0]%len(self.dictOfClasses.keys())] = returnTuple[1]
		self.progressCount += 1
		self.bar.update(progressCount)
		print progressCount, returnTuple
		lock.release()