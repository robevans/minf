__author__ = 'Robert Evans'

import Rdtw
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.table import Table
import numpy as np
import glob
import pandas

def dtwDirectoryAgainstItself(dir_name):
	inputFiles = glob.glob("%s/*.csv"%dir_name)
	distances = []
	for i in range(len(inputFiles)):
		distances.append([])
		for j in range(len(inputFiles)):
			distances[i].append(Rdtw.getDTWdist(inputFiles[i],inputFiles[j]))
	
	npDists = np.array(distances)

	plt.imshow(npDists, interpolation='nearest')
	plt.xticks(range(len(inputFiles)),[f.split('/')[-1].split('.')[0] for f in inputFiles])
	plt.yticks(range(len(inputFiles)),[f.split('/')[-1].split('.')[0] for f in inputFiles])
	plt.colorbar()
	plt.title("DTW distances cross referenced")

	data = pandas.DataFrame(np.array(distances), columns=[f.split('/')[-1].split('.')[0] for f in inputFiles])
	square_table(data)
	plt.show()

def square_table(data, fmt='{:.0f}'):
	fig, ax = plt.subplots()
	ax.set_axis_off()
	tb = Table(ax, bbox=[0,0,1,1])
	nrows, ncols = data.shape
	width, height = 1.0 / ncols, 1.0 / nrows

	# Add cells
	for (i,j), val in np.ndenumerate(data):
		tb.add_cell(i, j, width, height, text=fmt.format(val), loc='center')
	
	"""
    # Row and Column Labels...
	for i, label in enumerate(data.columns):
		tb.add_cell(i, -1, width, height, text=label, loc='right', edgecolor='none', facecolor='none')
		tb.add_cell(-1, i, width, height/2, text=label, loc='center', edgecolor='none', facecolor='none')
    """

	ax.add_table(tb)
	return fig

if __name__=='__main__':
	import sys
	if (len(sys.argv)==2):
		sys.exit(dtwDirectoryAgainstItself(sys.argv[1]))
	print "Usage: DTWDirectoryAgainstItself <directory>"