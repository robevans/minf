import cv2
from numpy import loadtxt
import matplotlib.pyplot as plt

if __name__ == '__main__':
    import sys
    print sys.argv
    # This will eventually launch the whole application.

class VideoPlayer:
    """
    Manages frame by frame video playback through OpenCV and provides an API to control it.
    """

    def __init__(self, videoFile):
        self.loadVideo(videoFile)

    def loadVideo(self, videoFile):
            # Load video from file
            self._videoCapture = cv2.VideoCapture(videoFile)
            if not self._videoCapture.isOpened():
                raise ValueError("Invalid video file")
            self._nFrames = int(self._videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
            self._fps = self._videoCapture.get(cv2.cv.CV_CAP_PROP_FPS)
            self._waitPerFrameInMillisec = int( 1000/self._fps )

            # And display the first frame
            cv2.namedWindow("window")

            self._currentFrame = -1
            self._showCurrentFrame()

    def showNextFrame(self):
        self._currentFrame = (self._currentFrame + 1) % self._nFrames
        self._showCurrentFrame()

    def showPrevFrame(self):
        self._currentFrame = (self._currentFrame - 1) % self._nFrames
        self._showCurrentFrame()

    def _showCurrentFrame(self):
        self._videoCapture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, self._currentFrame)
        success, img = self._videoCapture.read()
        cv2.imshow("window", img)
        cv2.waitKey(self._waitPerFrameInMillisec)

    def closePlayer(self):
        cv2.destroyWindow("window")

    def __del__(self):
        cv2.destroyWindow("window")

class Graph():
    def __init__(self, csvFile):
        self.loadData(csvFile)
        self.line=None
        self.mousePressed = None
        self.drawGraph()

    def loadData(self, csvFile):
        # TODO: Add arguments for number of header lines and which columns to use.
        with open(csvFile,'r') as fin:
            self.data = loadtxt(fin,delimiter=",")

    def drawGraph(self):
        plt.ion()
        self.fig = plt.figure()
        self.toolbar = plt.get_current_fig_manager().toolbar
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.data)
        self.fig.canvas.mpl_connect('button_press_event', self.onPress)
        self.fig.canvas.mpl_connect('motion_notify_event', self.onMotion)
        self.fig.canvas.mpl_connect('button_release_event', self.onRelease)

    def onPress(self, event):
        if self.toolbar.mode == '':
            if event.inaxes and event.xdata > 0:
                self.currentX = event.xdata
                self.isUpdated = True
                self.setLine(event.xdata)
        self.mousePressed = True

    def onMotion(self, event):
        if self.toolbar.mode == '' and self.mousePressed:
            if event.inaxes and event.xdata > 0:
                self.currentX = event.xdata
                self.isUpdated = True
                self.setLine(event.xdata)

    def onRelease(self, event):
        if self.toolbar.mode == '':
            if event.inaxes and event.xdata > 0:
                self.currentX = event.xdata
                self.isUpdated = True
                self.setLine(event.xdata)
        self.mousePressed = None

    def setLine(self, x):
        if self.line:
            del(self.ax.lines[-1])
            self.line=None
        if x>=0 and x<=len(self.data):
            self.line = self.line = self.ax.axvline(x=x, color='red', linewidth=5)
            self.fig.canvas.draw()

