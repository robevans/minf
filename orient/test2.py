__author__ = 'Andrew'
from graph import *

from imusim.simulation.base import Simulation
from imusim.io.bvh import loadBVHFile
from imusim.trajectories.rigid_body import SampledBodyModel, SplinedBodyModel
from imusim.platforms.imus import IdealIMU
from imusim.behaviours.imu import BasicIMUBehaviour
from imusim.algorithms.orientation import OrientCF
from imusim.visualisation.plotting import plot
from imusim.maths.quaternions import QuaternionArray
from pylab import show, array, arccos, dot, empty, figure, shape, transpose, l2norm, degrees, mean, title, xlabel, ylabel, legend
from numpy.random import random_sample

# Create the simulation, load a splined body model of walking from existing mocap data that can be
# evaluated at any time.

sim = Simulation()
env = sim.environment
samplingPeriod = 1.0/800
oversampling = 16
# worst case for offsets is probably +/-1
accel_offset = 0
gyro_offset = 0
mag_offset = 0
probDrippedPacket = 0.0
transmissionPeriod = samplingPeriod * oversampling
print "transmission rate: ", 1 / transmissionPeriod, " Hz"
simModel = SplinedBodyModel(loadBVHFile('walk.bvh', conversionFactor=0.01))
sim.time = simModel.startTime

def angle(a,b):
    return arccos(dot(a,b) / (l2norm(a) * l2norm(b)))

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

# get the sensor reading from the IMU at each sample time.

accel = behaviour.imu.accelerometer.rawMeasurements
mag = behaviour.imu.magnetometer.rawMeasurements
gyro = behaviour.imu.gyroscope.rawMeasurements
sample_timestamps = accel.timestamps
accel_values = accel.values
mag_values = mag.values
gyro_values = gyro.values


# Apply the sensor readings to an orientation complimentary filter to compute the orientation of the IMU at each
# sample time

initialRotation=joint.rotation(simModel.startTime)
orientationFilter = OrientCF(simModel.startTime, initialRotation, 1, 1)
quats = []
ts = []

start_offset = max(0,-min([mag_offset, accel_offset, gyro_offset]))
end_offset = min(0,-max([mag_offset, accel_offset, gyro_offset]))

print start_offset
print end_offset

for i in range(start_offset, len(sample_timestamps) - oversampling+end_offset, oversampling):
    a = mean(accel_values[:,i+accel_offset:i+oversampling+accel_offset], axis=1).reshape(-1,1)
    m = mean(mag_values[:,i+mag_offset:i+oversampling+mag_offset], axis=1).reshape(-1,1)
    g = mean(gyro_values[:,i+gyro_offset:i+oversampling+gyro_offset], axis=1).reshape(-1,1)
    # use the timestamp of the latest sample
    if random_sample() > probDrippedPacket:
        t = sample_timestamps[i + oversampling - 1]
        ts.append(t)
        orientationFilter(a, m, g, t)

        # evaluate true orientation of the joint at each IMU transmission time
        quats.append(joint.rotation(t))

original_quaternions = QuaternionArray(quats)
imu_quaternions = orientationFilter.rotation.values[1:]
if len(original_quaternions) <> len(imu_quaternions):
    print "lengths don't match"
    exit()

l = len(original_quaternions)


plot(original_quaternions, label='original')
plot(imu_quaternions,label='IMU')
title("Quaternions (original and IMU, right foot), 50Hz transmission rate, 100% delivery")
xlabel("Time (samples)")
#legend()

#graph(original_quaternions)
#show()



vx = array([1.0,0.0,0.0]).reshape(-1,1)
vy = array([0.0,1.0,0.0]).reshape(-1,1)
vz = array([0.0,0.0,1.0]).reshape(-1,1)
error_angles_x = empty((l,))
error_angles_y = empty((l,))
error_angles_z = empty((l,))
for i in range(l):
    q1 = imu_quaternions[i]
    q2 = original_quaternions[i]
    v1x = transpose(q1.rotateVector(vx))
    v2x = transpose(q2.rotateVector(vx))
    ax = degrees(angle(v1x[0],v2x[0]))
    v1y = transpose(q1.rotateVector(vy))
    v2y = transpose(q2.rotateVector(vy))
    ay = degrees(angle(v1y[0],v2y[0]))
    v1z = transpose(q1.rotateVector(vz))
    v2z = transpose(q2.rotateVector(vz))
    az = degrees(angle(v1z[0],v2z[0]))

    error_angles_x[i] = ax
    error_angles_y[i] = ay
    error_angles_z[i] = az

figure()
plot(error_angles_x,label='x')
plot(error_angles_y,label='y')
plot(error_angles_z,label='z')
title("Orientation error (right foot), 50Hz transmission rate, 100% delivery")
xlabel("Time (samples)")
ylabel("Angle (degrees)")
legend()

graph

show()