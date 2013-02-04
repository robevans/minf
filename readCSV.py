__author__ = 'Robert Evans'

import numpy
import pylab

def read(input_filename):
	with open(input_filename,'r') as fin:
			X = numpy.loadtxt(fin,delimiter=",")
	return X