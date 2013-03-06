import numpy

def readRaw(input_filename):
	with open(input_filename) as f:
		lines = f.readlines()

	data = []
	for l in lines:
		l= map(float,filter(lambda x: x!='' ,l.translate(None,',ary()[]/n')[:-1].split(' ')))
		data.append(l)

	return numpy.array(data)