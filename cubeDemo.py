__author__ = 'Andrew'

#from pylab import *
from enthought.traits.api import Button, HasTraits
from enthought.traits.ui.api import View, Item
from Queue import Queue, Empty
from comms import *
from random import random
#from display import *
#import enthought.traits.api as api
from enthought.mayavi import mlab
import wx
from numpy import shape
from imusim.io.bvh import *
from pylab import plot, show
from orientation import *


class CubeDemo(HasTraits):

    startButton = Button('Start')
    stopButton = Button('Stop')


    view = View(Item('startButton'),
                Item('stopButton'))

    def __init__(self):
        HasTraits.__init__(self)
        self._scene = mlab.gcf().scene
        #self.q1 = mlab.quiver3d(-2.0,0.0,0.0,1.0,0.0,0.0, colormap='Reds',mode='arrow')
        #self.q2 = mlab.quiver3d(-1.0,0.0,0.0,1.0,0.0,0.0, colormap='Greens',mode='arrow')
        #self.q3 = mlab.quiver3d(0.0,0.0,0.0,1.0,0.0,0.0, colormap='Blues',mode='arrow')
        #self.q4 = mlab.quiver3d(1.0,0.0,0.0,1.0,0.0,0.0, colormap='Reds',mode='arrow')
        #self.q5 = mlab.quiver3d(2.0,0.0,0.0,1.0,0.0,0.0,  colormap='Greens',mode='arrow')
        #self.q6 = mlab.quiver3d(3.0,0.0,0.0,1.0,0.0,0.0,  colormap='Blues',mode='arrow')


        self.queue = Queue()
        self.c = CaptureThread("COM4")
        self.c.start()

        simModel = loadBVHFile('walk.bvh', conversionFactor=0.01)

        self.configure_traits()

        #self.d = Display(self.scene)

    #def _update_display_fired(self):
    #    print "hello"
    #    self.d.update(self.c.x, self.c.y, self.c.z)

    def _startButton_fired(self):
        wx.GetApp().Bind(wx.EVT_IDLE, self._onIdleEvent)
        self.x = 1.0
        self.y = 0.0

    def _stopButton_fired(self):
        wx.GetApp().Bind(wx.EVT_IDLE, None)
        plot(array(self.c.mag_x)*1000)
        plot(array(self.c.gyro_z))
        show()

    def _onIdleEvent(self, event):
        #at,gt,mt,ax,ay,az,gx,gy,gz,mx,my,mz = self.c.latest_data
        q = self.c.latestOrientation[1]
        #q2 = self.c.latestOrientation[2]
        #q3 = self.c.latestOrientation[3]
        #q4 = self.c.latestOrientation[4]
        #q5 = self.c.latestOrientation[5]
        #q6 = self.c.latestOrientation[6]

        v = array([0.0,0.0,1.0]).reshape(-1,1)
        v1 = q.rotateVector(v)
        #v2 = q2.rotateVector(v)
        #v3 = q3.rotateVector(v)
        #v4 = q4.rotateVector(v)
        #v5 = q5.rotateVector(v)
        #v6 = q6.rotateVector(v)

        #print shape(v1)

        #print ax, ay, az

        x1 = v1[0]
        y1 = v1[1]
        z1 = v1[2]

#        x2 = v2[0]
#        y2 = v2[1]
#        z2 = v2[2]
#
#        x3 = v3[0]
#        y3 = v3[1]
#        z3 = v3[2]
#
#        x4 = v4[0]
#        y4 = v4[1]
#        z4 = v4[2]
#
#        x5 = v5[0]
#        y5 = v5[1]
#        z5 = v5[2]
#
#        x6 = v6[0]
#        y6 = v6[1]
#        z6 = v6[2]

        #self.x = ax
        #self.y = ay
        #self.z = az

        self.q1.mlab_source.set(u=x1, v=y1, w=z1)
        #self.q2.mlab_source.set(u=x2, v=y2, w=z2)
        #self.q3.mlab_source.set(u=x3, v=y3, w=z3)
        #self.q4.mlab_source.set(u=x4, v=y4, w=z4)
        #self.q5.mlab_source.set(u=x5, v=y5, w=z5)
        #self.q6.mlab_source.set(u=x6, v=y6, w=z6)

        #print gx,gy,gz

        event.RequestMore()


if __name__ == "__main__":
    cd = CubeDemo()