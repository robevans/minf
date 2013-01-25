# A space separated file can be imported into a numpy array by:
# f = open("filename.txt")
# numpy.loadtxt(f)

__author__ = 'Robert Evans'

import sys

def CSVtoSSV(fname):
	with open(fname) as f:
		lines = f.read()
		lines = lines.replace(',',' ')
		print lines

	noExtension = str(fname.split('.')[0])

	with open(noExtension+".txt",'w') as o:
		o.write(lines)



if __name__=='__main__':
	if (len(sys.argv)!=2):
		print "Usage: CSVtoSSV <filename>"
		sys.exit(0)
	sys.exit(CSVtoSSV(sys.argv[1]))