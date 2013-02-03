from pylab import *
import sys
from imusim.all import *

samplingPeriod = 0.04
imu = IdealIMU()
env = Environment()
#samples = 1000
#rotationalVelocity = 20
#calibrator = ScaleAndOffsetCalibrator(env, samples, samplingPeriod, rotationalVelocity)
#calibration = calibrator.calibrate(imu)
model = loadBVHFile('walk.bvh', CM_TO_M_CONVERSION)
splinedModel = SplinedBodyModel(model)
sim = Simulation(environment=env)
imu.simulation = sim
imu.trajectory = splinedModel.getJoint('rfoot')
sim.time = splinedModel.startTime
BasicIMUBehaviour(imu, samplingPeriod, initialTime=sim.time)
sim.run(splinedModel.endTime)
accel = imu.accelerometer.rawMeasurements
gyro = imu.gyroscope.rawMeasurements
mag = imu.magnetometer.rawMeasurements


