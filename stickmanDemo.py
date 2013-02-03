from imusim.all import *
from test3 import *

quats = joint.rotationKeyFrames.values


model = loadBVHFile('complex_bm_2_standing.bvh', CM_TO_M_CONVERSION)

l = []

for n in model.jointNames:
    d = dict()
    d['jointName'] = n
    d['rotation'] = Quaternion(0,0,0,1)
    l.append(d)

print l

reconstructor = BodyModelReconstructor(model)
for i in range(len(quats)):
    l[2]['rotation'] = quats[i]
    reconstructor.handleData(l,(i+1)/100.0)

renderer = BodyModelRenderer(model)
InteractiveAnimation(1/100.0, model.endTime, renderer)

