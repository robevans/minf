__author__ = 'Robert Evans'

import matplotlib.pyplot as plt
from subprocess import Popen, PIPE

class tool():
	def __init__(self, data, absolutePathToVideo):
		self.videoControl = videoController(absolutePathToVideo)
	 	self.data=data
	 	self.line=None
	 	self.mousePressed = None
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
		if self.line:
			del(self.ax.lines[-1])
			self.line=None
		if event.inaxes and event.xdata > 0:
			self.line =  self.ax.axvline(x=event.xdata, color='red')
			self.fig.canvas.draw()
			self.mousePressed = True

	def onMotion(self,event):
		if self.mousePressed:
			if event.inaxes and event.xdata > 0:
				if self.line:
					del(self.ax.lines[-1])
					self.line=None
				self.line =  self.ax.axvline(x=event.xdata, color='red')
				self.fig.canvas.draw()

	def onRelease(self,event):
		if self.line:
			del(self.ax.lines[-1])
			self.line=None
		if event.inaxes and event.xdata > 0:
			self.line =  self.ax.axvline(x=event.xdata, color='red')
			self.fig.canvas.draw()
		self.mousePressed = None

class videoController():
	def __init__(self,absolutePathToVideo=None):
		if absolutePathToVideo:
			self.open(absolutePathToVideo)

	def open(self, absolutePathToVideo):
		self.quit()
		applescript="""tell application "VLC"
							OpenURL "file://%s"
							activate
							play
							play
						end tell""" % absolutePathToVideo
		p = Popen(['osascript', '-'] + ['2', '2'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate(applescript)

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

	def setTime(self, seconds):
		applescript="""tell application "VLC"
							set current time to %i
						end tell"""%seconds
		p = Popen(['osascript', '-'] + ['2', '2'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate(applescript)

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