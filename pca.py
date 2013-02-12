__author__ = 'Robert Evans'

import numpy as np
import pylab as pl

from sklearn.decomposition import PCA

def doPCAonMultipleMotions(listOfHighDimMotions,n_components=3):
	listOfLowDimMotions = []
	for highDimMotion in listOfHighDimMotions:
		(lowDimMotion,variance) = pca(highDimMotion,n_components)
		listOfLowDimMotions.append(lowDimMotion)
	return listOfLowDimMotions

def pca(highDimensionalData,n_components=3):
	pca = PCA(n_components=n_components)
	lowDimensionalData = pca.fit(highDimensionalData).transform(highDimensionalData)

	#print "Explained variance by component: " + str(pca.explained_variance_ratio_)
	#pl.plot(lowDimensionalData)
	#pl.xlabel('Time (frames)')
	#pl.title('PCA using Euler Angles')
	#pl.savefig('/Users/robertevans/Desktop/eulerPCA.pdf', format='pdf')
	#pl.show()
	return (lowDimensionalData,pca.explained_variance_ratio_)

def pcaFromFile(input_filename,n_components=3):
	with open(input_filename,'r') as fin:
		X = np.loadtxt(fin,delimiter=",")
	return pca(X,n_components)

def pcaWithInputOutputFiles(input_filename,output_filename="Null"):
	with open(input_filename,'r') as fin:
		X = np.loadtxt(fin,delimiter=",")

	pca = PCA(n_components=3)
	X_r = pca.fit(X).transform(X)

	print X_r
	print "Explained variance by component: " + str(pca.explained_variance_ratio_)

	pl.plot(X_r)
	pl.show()

	if (output_filename!="Null"):
		np.savetxt("PCA-"+output_filename, X_r, delimiter=",")

if __name__=='__main__':
	import sys
	if (len(sys.argv)==2):
		sys.exit(pcaWithFiles(sys.argv[1]))
	if (len(sys.argv)==3):
		sys.exit(pcaWithFiles(sys.argv[1],sys.argv[2]))
	print "Usage: pca <input_filename> [output_filename]"