__author__ = 'Robert Evans'

from quats import plotQuatsFromFile

if __name__=='__main__':
	import sys
	if (len(sys.argv)==2):
		sys.exit(plotQuatsFromFile(sys.argv[1]))
	print "Usage: plotQuatsFromFile <file.csv>"