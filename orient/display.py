__author__ = 'Andrew'

from enthought.traits.api import *
from enthought.traits.ui.api import *
import enthought.traits.api as api
from enthought.mayavi.core.api import PipelineBase
from enthought.mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel
from pylab import *


class Display(HasTraits, ):
    def __init__(self, scene):
        self.scene=scene
        self.q1 = scene.mlab.quiver3d(1.0,0.0,0.0, resolution=128, colormap='Reds',mode='arrow')

    def update(self, x,y,z):
        self.q1.mlab_source.set(u=x,v=y,w=z)