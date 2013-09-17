__author__ = 'Andrew'

__author__ = 'Andrew'

from imusim.all import *

# Create the simulation, load a splined body model of walking from existing mocap data that can be
# evaluated at any time.

sim = Simulation()
env = sim.environment
samplingPeriod = 1.0/800
oversampling = 16
# worst case for offsets is probably +/-1
accel_offset = -16
gyro_offset = 8
mag_offset = 16
probDrippedPacket = 0.00
transmissionPeriod = samplingPeriod * oversampling
print "transmission rate: ", 1 / transmissionPeriod, " Hz"
simModel = SplinedBodyModel(loadBVHFile('walk.bvh', conversionFactor=0.01))
sim.time = simModel.startTime

def setupIMU(id, joint):
    # Set up an ideal IMU with the trajectory of the supplied joint, which samples at samplingPeriod.
    imu = IdealIMU()
    imu.simulation = sim
    imu.trajectory = joint

    def handleSample(behaviour):
        pass

    behaviour = BasicIMUBehaviour(imu, samplingPeriod, sampleCallback=handleSample, initialTime=sim.time)
    return behaviour

joint = simModel.getJoint('rfoot')
#original_quaternions = joint.rotationKeyFrames
behaviour = setupIMU(1, joint)
#show()

sim.run(simModel.endTime)

