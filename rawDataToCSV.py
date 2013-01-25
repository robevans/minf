#!/usr/bin/python
# This works on data from the comms.py script, if you 'print data' from python

def rawToCSV(input_filename,output_filename):

	with open(input_filename,'r') as fin:
		lines = fin.readlines()

	noExponents = []
	for l in lines:
		if not 'e' in l:
			noExponents = noExponents + [l]
	lines = noExponents

	onlyNumbers = []
	for l in lines:
		l = l.translate(None,'ary()')
		l = l.split(',')
		s = []
		for x in l:
			x=x.translate(None,'[ ]\n').split('.')	#extract x y z values from sensor array in form [123. 456. 789.]
			x = [n for n in x if n != '']	# get rid of null items
			s = s + [x]
		s = [n for sublist in s for n in sublist]	#flatten list
		onlyNumbers = onlyNumbers + [s]
	lines = onlyNumbers

	#separate sensors
	s1 = []
	s2 = []
	s3 = []
	for l in lines:
		if l[0] == str(10):
			s1 = s1 + [l]
		if l[0] == str(13):
			s2 = s2 + [l]
		if l[0] == str(18):
			s3 = s3 + [l]

	#delete all but sensor values
	t = []
	for l in s1:
		t = t + [l[4:]]
	s1 = t
	t = []
	for l in s2:
		t = t + [l[4:]]
	s2 = t
	t = []
	for l in s3:
		t = t + [l[4:]]
	s3 = t

	# interleave sensor values
	out = []
	for i in range(min(len(s1),len(s2),len(s3))):
		out = out + [s1[i]+s2[i]+s3[i]]

	#convert to csv
	string = ''
	with open(output_filename,'w') as fout:
		for l in out:
			for item in l:
				string = string + item + ','
			fout.write(string[:-1]+'\n')
			string = ''

if __name__=='__main__':
	import sys
	if (len(sys.argv)!=3):
		print "Usage: rawDataToCSV <input_filename> <output_filename>"
		sys.exit(0)
	sys.exit(rawToCSV(sys.argv[1],sys.argv[2]))

