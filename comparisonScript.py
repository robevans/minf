import demos
import armExercisesDatabase

db = armExercisesDatabase.db()

time db.computeAccelSegments()
db.LDsegs = db.LDaccelSegments
time demos.armExercisesIndividualSimMatrix(db,title='Accelerometer data similarities: Subject A', subjectNumber=0)
time demos.armExercisesIndividualSimMatrix(db,title='Accelerometer data similarities: Subject B', subjectNumber=1)
time demos.armExercisesIndividualSimMatrix(db,title='Accelerometer data similarities: Subject C', subjectNumber=2)
time demos.armExercisesLDParallelsimMatrix(db,title="All arm exercise similarities: PCA Accelerometer data")

time db.computeGyroSegments()
db.LDsegs = db.LDgyroSegments
time demos.armExercisesIndividualSimMatrix(db,title='Gyroscope data similarities: Subject A', subjectNumber=0)
time demos.armExercisesIndividualSimMatrix(db,title='Gyroscope data similarities: Subject B', subjectNumber=1)
time demos.armExercisesIndividualSimMatrix(db,title='Gyroscope data similarities: Subject C', subjectNumber=2)
time demos.armExercisesLDParallelsimMatrix(db,title="All arm exercise similarities: PCA Gyroscope data")

time db.computeMagSegments()
db.LDsegs = db.LDmagSegments
time demos.armExercisesIndividualSimMatrix(db,title='Magnetometer data similarities: Subject A', subjectNumber=0)
time demos.armExercisesIndividualSimMatrix(db,title='Magnetometer data similarities: Subject B', subjectNumber=1)
time demos.armExercisesIndividualSimMatrix(db,title='Magnetometer data similarities: Subject C', subjectNumber=2)
time demos.armExercisesLDParallelsimMatrix(db,title="All arm exercise similarities: PCA Magnetometer data")

time db.computeAccelWithGyroSegments()
db.LDsegs = db.LDaccelWithGyroSegments
time demos.armExercisesIndividualSimMatrix(db,title='Accel+Gyro data similarities: Subject A', subjectNumber=0)
time demos.armExercisesIndividualSimMatrix(db,title='Accel+Gyro data similarities: Subject B', subjectNumber=1)
time demos.armExercisesIndividualSimMatrix(db,title='Accel+Gyro data similarities: Subject C', subjectNumber=2)
time demos.armExercisesLDParallelsimMatrix(db,title="All arm exercise similarities: PCA Accel+Gyro data")

time db.computeAccelWithMagSegments()
db.LDsegs = db.LDaccelWithMagSegments
time demos.armExercisesIndividualSimMatrix(db,title='Accel+Mag data similarities: Subject A', subjectNumber=0)
time demos.armExercisesIndividualSimMatrix(db,title='Accel+Mag data similarities: Subject B', subjectNumber=1)
time demos.armExercisesIndividualSimMatrix(db,title='Accel+Mag data similarities: Subject C', subjectNumber=2)
time demos.armExercisesLDParallelsimMatrix(db,title="All arm exercise similarities: PCA Accel+Mag data")

time db.computeGyroWithMagSegments()
db.LDsegs = db.LDgyroWithMagSegments
time demos.armExercisesIndividualSimMatrix(db,title='Gyro+Mag data similarities: Subject A', subjectNumber=0)
time demos.armExercisesIndividualSimMatrix(db,title='Gyro+Mag data similarities: Subject B', subjectNumber=1)
time demos.armExercisesIndividualSimMatrix(db,title='Gyro+Mag data similarities: Subject C', subjectNumber=2)
time demos.armExercisesLDParallelsimMatrix(db,title="All arm exercise similarities: PCA Gyro+Mag data")