__author__ = 'Robert Evans'

import glob
import math
import numpy
import pylab
import smooth
from quats import plotQuatsFromFile
from mpl_toolkits.mplot3d import Axes3D

def plotSimilarityMatrix(distancesIn2DArray,tickLabels,title="DTW distances cross referenced",savePlot=False):
	distances = numpy.array(distancesIn2DArray)
	pylab.figure()
	pylab.imshow(distances, interpolation='nearest')
	pylab.xticks(range(len(distances)),tickLabels)
	pylab.yticks(range(len(distances)),tickLabels)
	pylab.colorbar()
	pylab.title(title)
	pylab.tight_layout()
	if savePlot:
		pylab.savefig('/Users/robertevans/Desktop/'+title+'.pdf', format='pdf')
	else:
		pylab.show()

def plotPCA3D(lowDims,title="Latent space"):
	fig = pylab.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.plot3D(range(len(lowDims[:,0])),lowDims[:,0],lowDims[:,1])
	ax.set_xlabel('Time')
	ax.set_ylabel('1st component')
	ax.set_zlabel('2nd component')
	pylab.title(title)
	pylab.show()

def plotPCA3Dsubplots(listOflowDimLists):
	f = pylab.figure()
	for i in range(len(listOflowDimLists)):
		ax = f.add_subplot(int(math.ceil(math.sqrt(len(listOflowDimLists)))),int(math.ceil(math.sqrt(len(listOflowDimLists)))),i+1,projection='3d')
		ax.plot3D(range(len(listOflowDimLists[i][:,0])),listOflowDimLists[i][:,0],listOflowDimLists[i][:,1])
		ax.set_xlabel('Time')
		ax.set_ylabel('1st component')
		ax.set_zlabel('2nd component')
	f.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
	pylab.show()

def plotGridOf2Ds(listOfDatas,title="Grid"):
	f = pylab.figure()
	for i in range(len(listOfDatas)):
		ax = f.add_subplot(int(math.ceil(math.sqrt(len(listOfDatas)))),int(math.ceil(math.sqrt(len(listOfDatas)))),i+1)
		ax.plot(listOfDatas[i])
		ax.set_xlabel('Time')
		ax.set_ylabel('y')
		if i==1:
			ax.set_title(title)
	pylab.show()

def plotDir(input_directory):

	inputFiles = glob.glob("%s/*.csv"%input_directory)

	data = []
	names = []
	for f in inputFiles:
		with open(f,'r') as fin:
			data.append(numpy.loadtxt(fin,delimiter=","))
			names.append(f.split('/')[-1].split('.')[0])

	n = int(math.ceil(math.sqrt(len(data))))
	figure,axes = pylab.subplots(n, n, sharex=True, sharey=True)

	i = 0
	for r in range(n):
		for c in range(n):
			if i >= len(data):
				axes[r,c].axis('off')
			else:
				axes[r,c].plot(data[i])
				axes[r,c].set_title(names[i])
			i+=1

	if len(data)-(n*n) != 0:
		pylab.setp([a.get_xticklabels() for a in axes[-2, len(data)-(n*n):]], visible=True)

	pylab.tight_layout()
	#pylab.savefig('/Users/robertevans/Desktop/VHsegments.pdf', format='pdf')
	pylab.show()

def plotCSV(input_filename):
	with open(input_filename,'r') as fin:
			X = numpy.loadtxt(fin,delimiter=",")

	pylab.figure()
	pylab.plot(X)
	pylab.xlabel('Time (frames)')
	pylab.ylabel('Sensor readings')
	pylab.title('Title')
	#pylab.legend((''))

	#pylab.tight_layout()
	pylab.show()
	#pylab.savefig('/Users/robertevans/Desktop/postPCA.pdf', format='pdf')

if __name__=='__main__':
	import sys
	if (len(sys.argv)==2):
		sys.exit(plotCSV(sys.argv[1]))
	print "Usage: plotCSV <file.csv>"