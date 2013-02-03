__author__ = 'Robert Evans'

import numpy as np
import pylab as pl

from sklearn.decomposition import PCA

def pca(highDimensionalData,n_components=3):
	pca = PCA(n_components=n_components)
	lowDimensionalData = pca.fit(highDimensionalData).transform(highDimensionalData)

	print lowDimensionalData
	print "Explained variance by component: " + str(pca.explained_variance_ratio_)

	pl.plot(lowDimensionalData)
	pl.show()

def pcaWithFiles(input_filename,output_filename="Null"):

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