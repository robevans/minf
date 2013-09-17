__author__ = 'Robert Evans'

import orient.commsTDMA
from time import sleep

if __name__ == '__main__':

	import sys
	if (len(sys.argv)!=3):
		print "Usage: doCapture <captureTimeInSeconds> <output_file>"
		sys.exit(0);
	captureTime = float(sys.argv[1])
	output_file = sys.argv[2]
	with open (output_file, "w") as fout:
		fout.write('')  # Init file

	def callback(frame):
		with open (output_file, "a") as fout:
			fout.write(str(frame)+'\n')  # Append frame to file

	comms = commsTDMA.CaptureThread(callback)
	comms.start()
	sleep(captureTime)
	comms.stop=True
	sys.exit(0);