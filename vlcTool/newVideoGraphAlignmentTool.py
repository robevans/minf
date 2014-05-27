__author__ = 'Robert Evans'

''' Example usage (type into iPython):
										import newVideoGraphAlignmentTool as tool
										tool.tool('data.csv','video.mov')
'''

import matplotlib.pyplot as plt
from subprocess import Popen, PIPE
import threading
import numpy
import time
import os

lock = threading.Lock()

class tool():
	def __init__(self, csvFile, pathToVideo):
			if not os.path.isfile(pathToVideo):
				raise Exception("Invalid video file path")
			if not (csvFile.lower().endswith('.csv') and os.path.isfile(csvFile)):
				raise Exception("Invalid csv file path")

			with open(csvFile,'r') as fin:
				data = numpy.loadtxt(fin,delimiter=",")

			self.graph = graph(data)
			self.video = videoController(os.path.abspath(pathToVideo))
			self.coordinator = coordinator(self.graph, self.video)
			self.coordinator.start()

class coordinator(threading.Thread):
	def __init__(self, graph, videoController):
		self.g = graph
		self.v = videoController
		super(coordinator, self).__init__()

	def run(self):
		while self.v.isOpen() == 'true' and plt.fignum_exists(self.g.fig.number):
			if self.g.isUpdated:
				self.v.setTime((self.g.currentX/len(self.g.data)*self.v.getDuration()))
				self.g.isUpdated = False
			else:
				lock.acquire()
				if self.g.isUpdated == False:
					self.g.setLine((float(self.v.getTime())/float(self.v.getDuration()))*len(self.g.data))
				lock.release()
			time.sleep(0.1)

class graph():
	def __init__(self, data):
		self.data=data
		self.line=None
		self.mousePressed = None
		self.currentX = None
		self.isUpdated = False
		self.drawGraph()

	def drawGraph(self):
		plt.ion()
		self.fig = plt.figure()
		self.ax = self.fig.add_subplot(111)
		self.ax.plot(self.data)
		self.fig.canvas.mpl_connect('button_press_event', self.onPress)
		self.fig.canvas.mpl_connect('motion_notify_event', self.onMotion)
		self.fig.canvas.mpl_connect('button_release_event', self.onRelease)

	def onPress(self,event):
		lock.acquire()
		if event.inaxes and event.xdata > 0:
			self.currentX = event.xdata
			self.isUpdated = True
			self.setLine(event.xdata)
			self.mousePressed = True
		lock.release()

	def onMotion(self,event):
		lock.acquire()
		if self.mousePressed:
			if event.inaxes and event.xdata > 0:
				self.currentX = event.xdata
				self.isUpdated = True
				self.setLine(event.xdata)
		lock.release()

	def onRelease(self,event):
		lock.acquire()
		if event.inaxes and event.xdata > 0:
			self.currentX = event.xdata
			self.isUpdated = True
			self.setLine(event.xdata)
		self.mousePressed = None
		lock.release()

	def setLine(self, x):
		if self.line:
			del(self.ax.lines[-1])
			self.line=None
		if x>=0 and x<=len(self.data):
			self.line = self.line = self.ax.axvline(x=x, color='red', linewidth=5)
			self.fig.canvas.draw()
			

class videoController():
	def __init__(self,absolutePathToVideo=None):
		if absolutePathToVideo:
			self.open(absolutePathToVideo)

	def open(self, absolutePathToVideo):
		if os.path.isfile(absolutePathToVideo):
			self.quit()
			applescript="""tell application "VLC"
								OpenURL "file://%s"
								activate
								play
								play
							end tell""" % absolutePathToVideo
			p = Popen(['osascript', '-'] + ['2', '2'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
			stdout, stderr = p.communicate(applescript)

	def isOpen(self):
		applescript="""application "VLC" is running"""
		p = Popen(['osascript', '-'] + ['2', '2'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate(applescript)
		return stdout[:-1]

	def play(self):
		applescript="""tell application "VLC"
							if not playing then
								play
							end if
						end tell"""
		p = Popen(['osascript', '-'] + ['2', '2'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate(applescript)

	def pause(self):
		applescript="""tell application "VLC"
							if playing then
								play
							end if
						end tell"""
		p = Popen(['osascript', '-'] + ['2', '2'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate(applescript)

	def isPlaying(self):
		applescript="""tell application "VLC"
							playing
						end tell"""
		p = Popen(['osascript', '-'] + ['2', '2'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate(applescript)
		if 'true' in stdout:
			return True
		else:
			return False

	def setTime(self, seconds):
		applescript="""tell application "VLC"
							set current time to %i
						end tell"""%seconds
		p = Popen(['osascript', '-'] + ['2', '2'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate(applescript)

	def getTime(self):
		applescript="""tell application "VLC"
							get current time
						end tell"""
		p = Popen(['osascript', '-'] + ['2', '2'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate(applescript)
		return int(stdout[:-1])

	def getDuration(self):
		applescript="""tell application "VLC"
							duration of current item
						end tell"""
		p = Popen(['osascript', '-'] + ['2', '2'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate(applescript)
		return int(stdout[:-1])

	def quit(self):
		applescript="""if application "VLC" is running
							tell application "VLC"
								quit
							end tell
						end if

						repeat until application "VLC" is not running
							delay 1
						end repeat"""
		p = Popen(['osascript', '-'] + ['2', '2'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate(applescript)