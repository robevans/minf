import direct.directbase.DirectStart
from panda3d.core import AmbientLight,DirectionalLight
from panda3d.core import TextNode,NodePath,LightAttrib
from panda3d.core import Vec3,Vec4,Quat
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
import sys
import select
import socket

jointNames = ['Skeleton', 'LeftHip', 'LeftKnee', 'RightHip', 'RightKnee']
mapping = {4:'Skeleton', 2:'LeftHip',6:'LeftKnee',3:'RightHip',5:'RightKnee'}
parents = {'Skeleton':None, 'LeftHip':'Skeleton','LeftKnee':'LeftHip','RightHip':'Skeleton','RightKnee':'RightHip'}

#A simple function to make sure a value is in a given range, -1 to 1 by default
def restrain(i, mn = -1, mx = 1): return min(max(i, mn), mx)

#Macro-like function used to reduce the amount to code needed to create the
#on screen instructions
def genLabelText(text, i):
  return OnscreenText(text = text, pos = (-1.3, .95-.06*i), fg=(1,1,1,1),
                      align = TextNode.ALeft, scale = .05)

class World(DirectObject):
  def __init__(self):
    #This code puts the standard title and instruction text on screen
    self.title = OnscreenText(text="",
                              style=1, fg=(1,1,1,1),
                              pos=(0.7,-0.95), scale = .07)
    self.onekeyText   = genLabelText("ESC: Quit", 0)
    self.onekeyText   = genLabelText("[1]: Calibrate", 1)
      
    #setup key input
    self.accept('escape', sys.exit)
    self.accept('1', self.calibrate)

    base.disableMouse()                  #Disable mouse-based camera-control
    camera.setPos(0,-15, 2)              #Position the cameraffff

    self.eve = Actor("models/ralph") #Load our animated charachter
    self.eve.reparentTo(render)          #Put it in the scene

    #Now we use controlJoint to get a NodePath that's in control of her neck
    #This must be done before any animations are played

    self.joints = dict()    # mapping from names to NodePath objects
    self.modelQ = dict()    # mapping from names to default joint orientations in the model
    self.jointCal = dict()  # mapping from names to calibration quaternion
    self.jointCur = dict()  # mapping from names to current device orientation
    for name in jointNames:
        self.joints[name] = self.eve.controlJoint(None, 'modelRoot', name)
        self.modelQ[name] = self.joints[name].getQuat()
        self.jointCal[name] = self.modelQ[name].identQuat()
        self.jointCur[name] = self.modelQ[name].identQuat()

    #We now play an animation. An animation must be played, or at least posed
    #for the nodepath we just got from controlJoint to actually effect the model
    #self.eve.actorInterval("walk", playRate = 2).loop()
    print self.eve.listJoints()

    self.setupLights()                           #Put in some default lighting

    # setup socket
    self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.udpSocket.bind(("localhost", 5555))
    self.udpSocket.setblocking(0)
    taskMgr.add(self.checkSocket, "checkSocket")

  def checkSocket(self, task):
      r_read, r_write, r_error = select.select([self.udpSocket],[],[],0)

      while r_read:
          msg = self.udpSocket.recv(1024)
          #print msg
          msg_list = msg.split(',')
          node_id = int(msg_list[0])
          [w, x, y, z] = [float(val) for val in msg_list[1:5]]
          seqNum = int(msg_list[5])
          #print seqNum
          q = Quat()
          q.setR(w)
          q.setI(x)
          q.setJ(y)
          q.setK(z)

          self.jointCur[mapping[node_id]] = q

          # update root
          root = jointNames[0]
          self.joints[root].setQuat(self.modelQ[root]*(self.jointCal[root]*self.jointCur[root]))

          #other joints
          for name in jointNames[1:]:
              parentName = parents[name]
              _q = self.jointCal[parentName]*self.jointCur[parentName]
              _q = _q.conjugate()
              self.joints[name].setQuat((self.jointCal[name]*self.jointCur[name])*_q*self.modelQ[name])

          r_read, r_write, r_error = select.select([self.udpSocket],[],[],0)
      return Task.cont

  def calibrate(self):
      for name in jointNames:
          self.jointCal[name] = self.jointCur[name].conjugate()

  def setupLights(self):                    #Sets up some default lighting
    ambientLight = AmbientLight( "ambientLight" )
    ambientLight.setColor( Vec4(.4, .4, .35, 1) )
    directionalLight = DirectionalLight( "directionalLight" )
    directionalLight.setDirection( Vec3( 0, 8, -2.5 ) )
    directionalLight.setColor( Vec4( 0.9, 0.8, 0.9, 1 ) )
    render.setLight(render.attachNewNode( directionalLight ) )
    render.setLight(render.attachNewNode( ambientLight ) )

w = World()        #Create an instance of our class
run()              #Run the simulation

