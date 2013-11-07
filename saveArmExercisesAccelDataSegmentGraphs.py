import segment
import armExercisesDatabase

db = armExercisesDatabase.db(computeSegments=False)

classes = ['10l','10r','20l','20r','30l','30r','40l','40r','50l','50r','60l','60r','70l','70r','80l','80r','90l','90r']
subjects = ['dan','rob','laura']
db.accelData_pca

sIndex = -1
for s in subjects:
	sIndex += 1
	for c in classes:
		segment.segmentAndPlot(db.accelData_pca[c][sIndex][0][:,0], smoothingWindow=300, save=True, title=s+': '+c)