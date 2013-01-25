__author__ = 'Robert Evans'

import os

def trim(startHours, startMinutes, startSeconds, footage, endHours, endMinutes, endSeconds, outfile):

	"""Given a start and end time of the form 00:00:00, and a video, trim to those times.  footage is of form movie.avi (or other format).  outfile must have same format."""
	durationHours = endHours-startHours
	durationMinutes = endMinutes-startMinutes
	if durationMinutes < 0:
		durationHours -= 1
		durationMinutes += 60
	durationSeconds = endSeconds-startSeconds
	if durationSeconds < 0:
		durationMinutes -= 1
		durationSeconds += 60
	os.system("ffmpeg -i \"%s\" -vcodec copy -acodec copy -ss %02d:%02d:%02d -t %02d:%02d:%02d \"%s\"" % (footage,startHours,startMinutes,startSeconds,durationHours,durationMinutes,durationSeconds,outfile))

if __name__=='__main__':
	import sys
	if (len(sys.argv)==9):
		sys.exit(trim(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),str(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7]),str(sys.argv[8])))
	print "Usage: trimVideo <startHours> <startMinutes> <startSeconds> <footage> <endHours> <endMinutes> <endSeconds> <outfile>"