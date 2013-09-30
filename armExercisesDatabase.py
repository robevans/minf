__author__ = 'Robert Evans'

import master as m
import progressbar
import pca as p
from numpy import concatenate

class db:
	def __init__ (self, computeSegments=False):
		print "Reading data..."

		dan10r=m.readRaw("captures/armExercise/Up/Dan Berbec/10r.txt")[26:,4:]
		dan10l=m.readRaw("captures/armExercise/Up/Dan Berbec/10l.txt")[26:,4:]
		dan20r=m.readRaw("captures/armExercise/Up/Dan Berbec/20r.txt")[26:,4:]
		dan20l=m.readRaw("captures/armExercise/Up/Dan Berbec/20l.txt")[26:,4:]
		dan30r=m.readRaw("captures/armExercise/Up/Dan Berbec/30r.txt")[26:,4:]
		dan30l=m.readRaw("captures/armExercise/Up/Dan Berbec/30l.txt")[26:,4:]
		dan40r=m.readRaw("captures/armExercise/Up/Dan Berbec/40r.txt")[26:,4:]
		dan40l=m.readRaw("captures/armExercise/Up/Dan Berbec/40l.txt")[26:,4:]
		dan50r=m.readRaw("captures/armExercise/Up/Dan Berbec/50r.txt")[26:,4:]
		dan50l=m.readRaw("captures/armExercise/Up/Dan Berbec/50l.txt")[26:,4:]
		dan60r=m.readRaw("captures/armExercise/Up/Dan Berbec/60r.txt")[26:,4:]
		dan60l=m.readRaw("captures/armExercise/Up/Dan Berbec/60l.txt")[26:,4:]
		dan70r=m.readRaw("captures/armExercise/Up/Dan Berbec/70r.txt")[26:,4:]
		dan70l=m.readRaw("captures/armExercise/Up/Dan Berbec/70l.txt")[26:,4:]
		dan80r=m.readRaw("captures/armExercise/Up/Dan Berbec/80r.txt")[26:,4:]
		dan80l=m.readRaw("captures/armExercise/Up/Dan Berbec/80l.txt")[26:,4:]
		dan90r=m.readRaw("captures/armExercise/Up/Dan Berbec/90r.txt")[26:,4:]
		dan90l=m.readRaw("captures/armExercise/Up/Dan Berbec/90l.txt")[26:,4:]
		
		robert10r=m.readRaw("captures/armExercise/Up/Robert Evans/10r.txt")[26:,4:]
		robert10l=m.readRaw("captures/armExercise/Up/Robert Evans/10l.txt")[66:,4:]
		robert20r=m.readRaw("captures/armExercise/Up/Robert Evans/20r.txt")[26:,4:]
		robert20l=m.readRaw("captures/armExercise/Up/Robert Evans/20l.txt")[26:,4:]
		robert30r=m.readRaw("captures/armExercise/Up/Robert Evans/30r.txt")[26:,4:]
		robert30l=m.readRaw("captures/armExercise/Up/Robert Evans/30l.txt")[26:,4:]
		robert40r=m.readRaw("captures/armExercise/Up/Robert Evans/40r.txt")[26:,4:]
		robert40l=m.readRaw("captures/armExercise/Up/Robert Evans/40l.txt")[26:,4:]
		robert50r=m.readRaw("captures/armExercise/Up/Robert Evans/50r.txt")[26:,4:]
		robert50l=m.readRaw("captures/armExercise/Up/Robert Evans/50l.txt")[26:,4:]
		robert60r=m.readRaw("captures/armExercise/Up/Robert Evans/60r.txt")[26:,4:]
		robert60l=m.readRaw("captures/armExercise/Up/Robert Evans/60l.txt")[26:,4:]
		robert70r=m.readRaw("captures/armExercise/Up/Robert Evans/70r.txt")[26:,4:]
		robert70l=m.readRaw("captures/armExercise/Up/Robert Evans/70l.txt")[26:,4:]
		robert80r=m.readRaw("captures/armExercise/Up/Robert Evans/80r.txt")[26:,4:]
		robert80l=m.readRaw("captures/armExercise/Up/Robert Evans/80l.txt")[26:,4:]
		robert90r=m.readRaw("captures/armExercise/Up/Robert Evans/90r.txt")[26:,4:]
		robert90l=m.readRaw("captures/armExercise/Up/Robert Evans/90l.txt")[26:,4:]

		laura10r=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura10r.txt")[26:,4:]
		laura10l=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura10l.txt")[26:,4:]
		laura20r=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura20r.txt")[26:,4:]
		laura20l=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura20l.txt")[26:,4:]
		laura30r=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura30r.txt")[26:,4:]
		laura30l=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura30l.txt")[26:,4:]
		laura40r=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura40r.txt")[26:,4:]
		laura40l=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura40l.txt")[26:,4:]
		laura50r=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura50r.txt")[26:,4:]
		laura50l=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura50l.txt")[26:,4:]
		laura60r=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura60r.txt")[26:,4:]
		laura60l=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura60l.txt")[26:,4:]
		laura70r=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura70r.txt")[26:,4:]
		laura70l=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura70l.txt")[26:,4:]
		laura80r=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura80r.txt")[26:,4:]
		laura80l=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura80l.txt")[26:,4:]
		laura90r=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura90r.txt")[26:,4:]
		laura90l=m.readRaw("captures/armExercise/Up/Laura Ionescu/laura90l.txt")[26:,4:]

		self.data = {'10l':[dan10l,robert10l,laura10l],'20l':[dan20l,robert20l,laura20l],'30l':[dan30l,robert30l,laura30l],'40l':[dan40l,robert40l,laura40l],'50l':[dan50l,robert50l,laura50l],'60l':[dan60l,robert60l,laura60l],'70l':[dan70l,robert70l,laura70l],'80l':[dan80l,robert80l,laura80l],'90l':[dan90l,robert90l,laura90l],
		             '10r':[dan10r,robert10r,laura10r],'20r':[dan20r,robert20r,laura20r],'30r':[dan30r,robert30r,laura30r],'40r':[dan40r,robert40r,laura40r],'50r':[dan50r,robert50r,laura50r],'60r':[dan60r,robert60r,laura60r],'70r':[dan70r,robert70r,laura70r],'80r':[dan80r,robert80r,laura80r],'90r':[dan90r,robert90r,laura90r]}

		self.accelData = {k:[a[:,0:3] for a in v] for k,v in self.data.iteritems()}
		self.gyroData = {k:[a[:,3:6] for a in v] for k,v in self.data.iteritems()}
		self.magData = {k:[a[:,6:9] for a in v] for k,v in self.data.iteritems()}

		self.accelWithGyroData = {k:[a[:,0:6] for a in v] for k,v in self.data.iteritems()}
		self.accelWithMagData = {k:[concatenate((a[:,0:3],a[:,6:9]),axis=1) for a in v] for k,v in self.data.iteritems()}
		self.gyroWithMagData = {k:[a[:,3:9] for a in v] for k,v in self.data.iteritems()}

		print "Computing dimensionality reduction..."

		self.pca = {k:[p.pca(a,n_components=9) for a in v] for k,v in self.data.iteritems()}
		self.accelData_pca = {k:[p.pca(a,n_components=3) for a in v] for k,v in self.accelData.iteritems()}
		self.gyroData_pca = {k:[p.pca(a,n_components=3) for a in v] for k,v in self.gyroData.iteritems()}
		self.magData_pca = {k:[p.pca(a,n_components=3) for a in v] for k,v in self.magData.iteritems()}
		
		self.accelWithGyroData_pca = {k:[p.pca(a,n_components=6) for a in v] for k,v in self.accelWithGyroData.iteritems()}
		self.accelWithMagData_pca = {k:[p.pca(a,n_components=6) for a in v] for k,v in self.accelWithMagData.iteritems()}
		self.gyroWithMagData_pca = {k:[p.pca(a,n_components=6) for a in v] for k,v in self.gyroWithMagData.iteritems()}

		self.pcaDataOnly = {key:[tuple[0] for tuple in value] for key,value in self.pca.iteritems()}
		self.explainedVariances = {key:[tuple[1] for tuple in value] for key,value in self.pca.iteritems()}
		self.averageExplainedVariance = [float(sum(t))/len(t) for t in zip(*[[float(sum(t))/len(t) for t in zip(*l)] for l in self.explainedVariances.values()])]

		if computeSegments:
			self.computeSegments()

		print "Database ready"

	def computeAccelSegments(self):
		print "Segmenting just accelerometer data..."
		self.accelSegs = {k:[m.getHighAndLowDimSegments(a, n_components=3, smoothingWindow=300) for a in v] for k,v in self.accelData.iteritems()}
		self.HDaccelSegments = {k:[HD for (HD,LD,vs) in v] for k,v in self.accelSegs.iteritems()}
		self.LDaccelSegments = {k:[LD for (HD,LD,vs) in v] for k,v in self.accelSegs.iteritems()}

	def computeGyroSegments(self):
		print "Segmenting just gyroscope data..."
		self.gyroSegs = {k:[m.getHighAndLowDimSegments(a, n_components=3, smoothingWindow=300) for a in v] for k,v in self.gyroData.iteritems()}
		self.HDgyroSegments = {k:[HD for (HD,LD,vs) in v] for k,v in self.gyroSegs.iteritems()}
		self.LDgyroSegments = {k:[LD for (HD,LD,vs) in v] for k,v in self.gyroSegs.iteritems()}

	def computeMagSegments(self):
		print "Segmenting just magnetometer data..."
		self.magSegs = {k:[m.getHighAndLowDimSegments(a, n_components=3, smoothingWindow=300) for a in v] for k,v in self.magData.iteritems()}
		self.HDmagSegments = {k:[HD for (HD,LD,vs) in v] for k,v in self.magSegs.iteritems()}
		self.LDmagSegments = {k:[LD for (HD,LD,vs) in v] for k,v in self.magSegs.iteritems()}

	def computeAccelWithGyroSegments(self):
		print "Segmenting accelerometer with gyroscope data..."
		self.accelWithGyroSegs = {k:[m.getHighAndLowDimSegments(a, n_components=3, smoothingWindow=300) for a in v] for k,v in self.accelWithGyroData.iteritems()}
		self.HDaccelWithGyroSegments = {k:[HD for (HD,LD,vs) in v] for k,v in self.accelWithGyroSegs.iteritems()}
		self.LDaccelWithGyroSegments = {k:[LD for (HD,LD,vs) in v] for k,v in self.accelWithGyroSegs.iteritems()}

	def computeAccelWithMagSegments(self):
		print "Segmenting accelerometer with magnetometer data..."
		self.accelWithMagSegs = {k:[m.getHighAndLowDimSegments(a, n_components=3, smoothingWindow=300) for a in v] for k,v in self.accelWithMagData.iteritems()}
		self.HDaccelWithMagSegments = {k:[HD for (HD,LD,vs) in v] for k,v in self.accelWithMagSegs.iteritems()}
		self.LDaccelWithMagSegments = {k:[LD for (HD,LD,vs) in v] for k,v in self.accelWithMagSegs.iteritems()}

	def computeGyroWithMagSegments(self):
		print "Segmenting gyroscope with magnetometer data..."
		self.gyroWithMagSegs = {k:[m.getHighAndLowDimSegments(a, n_components=3, smoothingWindow=300) for a in v] for k,v in self.gyroWithMagData.iteritems()}
		self.HDgyroWithMagSegments = {k:[HD for (HD,LD,vs) in v] for k,v in self.gyroWithMagSegs.iteritems()}
		self.LDgyroWithMagSegments = {k:[LD for (HD,LD,vs) in v] for k,v in self.gyroWithMagSegs.iteritems()}

	def mergeSegments(dictOfSegmentsBySubject):
		mergedSubjects = {key:value for (key,value) in zip( dictOfSegmentsBySubject.keys(), [sum(subject,[]) for subject in dictOfSegmentsBySubject.values()] ) }
		mergedLeftAndRightArmExercises = {}
		for classLabel,motions in mergedSubjects.iteritems():
			for segment in motions:
				mergedLeftAndRightArmExercises.setdefault(classLabel[:-1], []).append(segment)
		return mergedLeftAndRightArmExercises

	def computeSegments(self):
		print "Segmenting data..."
		bar = progressbar.ProgressBar(maxval=54, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		bar.start(); progress = 0

		#Each of these returns in the form (HDsegments,LDsegments,explainedVariance)
		dan10r=m.getHighAndLowDimSegments(self.data['10r'][0], n_components=9, smoothingWindow=150); progress += 1; bar.update(progress)
		dan10l=m.getHighAndLowDimSegments(self.data['10l'][0], n_components=9, smoothingWindow=150); progress += 1; bar.update(progress)
		dan20r=m.getHighAndLowDimSegments(self.data['20r'][0], n_components=9, smoothingWindow=150); progress += 1; bar.update(progress)
		dan20l=m.getHighAndLowDimSegments(self.data['20l'][0], n_components=9, smoothingWindow=150); progress += 1; bar.update(progress)
		dan30r=m.getHighAndLowDimSegments(self.data['30r'][0], n_components=9, smoothingWindow=170); progress += 1; bar.update(progress)
		dan30l=m.getHighAndLowDimSegments(self.data['30l'][0], n_components=9, smoothingWindow=160); progress += 1; bar.update(progress)
		dan40r=m.getHighAndLowDimSegments(self.data['40r'][0], n_components=9, smoothingWindow=200); progress += 1; bar.update(progress)
		dan40l=m.getHighAndLowDimSegments(self.data['40l'][0], n_components=9, smoothingWindow=150); progress += 1; bar.update(progress)
		dan50r=m.getHighAndLowDimSegments(self.data['50r'][0], n_components=9, smoothingWindow=180); progress += 1; bar.update(progress)
		dan50l=m.getHighAndLowDimSegments(self.data['50l'][0], n_components=9, smoothingWindow=180); progress += 1; bar.update(progress)
		dan60r=m.getHighAndLowDimSegments(self.data['60r'][0], n_components=9, smoothingWindow=180); progress += 1; bar.update(progress)
		dan60l=m.getHighAndLowDimSegments(self.data['60l'][0], n_components=9, smoothingWindow=200); progress += 1; bar.update(progress)
		dan70r=m.getHighAndLowDimSegments(self.data['70r'][0], n_components=9, smoothingWindow=170); progress += 1; bar.update(progress)
		dan70l=m.getHighAndLowDimSegments(self.data['70l'][0], n_components=9, smoothingWindow=150); progress += 1; bar.update(progress)
		dan80r=m.getHighAndLowDimSegments(self.data['80r'][0], n_components=9, smoothingWindow=150); progress += 1; bar.update(progress)
		dan80l=m.getHighAndLowDimSegments(self.data['80l'][0], n_components=9, smoothingWindow=180); progress += 1; bar.update(progress)
		dan90r=m.getHighAndLowDimSegments(self.data['90r'][0], n_components=9, smoothingWindow=180); progress += 1; bar.update(progress)
		dan90l=m.getHighAndLowDimSegments(self.data['90l'][0], n_components=9, smoothingWindow=150); progress += 1; bar.update(progress)

		robert10r=m.getHighAndLowDimSegments(self.data['10r'][1], n_components=9, smoothingWindow=130); progress += 1; bar.update(progress)
		robert10l=m.getHighAndLowDimSegments(self.data['10l'][1], n_components=9, smoothingWindow=130); progress += 1; bar.update(progress)
		robert20r=m.getHighAndLowDimSegments(self.data['20r'][1], n_components=9, smoothingWindow=130); progress += 1; bar.update(progress)
		robert20l=m.getHighAndLowDimSegments(self.data['20l'][1], n_components=9, smoothingWindow=130); progress += 1; bar.update(progress)
		robert30r=m.getHighAndLowDimSegments(self.data['30r'][1], n_components=9, smoothingWindow=130); progress += 1; bar.update(progress)
		robert30l=m.getHighAndLowDimSegments(self.data['30l'][1], n_components=9, smoothingWindow=130); progress += 1; bar.update(progress)
		robert40r=m.getHighAndLowDimSegments(self.data['40r'][1], n_components=9, smoothingWindow=130); progress += 1; bar.update(progress)
		robert40l=m.getHighAndLowDimSegments(self.data['40l'][1], n_components=9, smoothingWindow=130); progress += 1; bar.update(progress)
		robert50r=m.getHighAndLowDimSegments(self.data['50r'][1], n_components=9, smoothingWindow=170); progress += 1; bar.update(progress)
		robert50l=m.getHighAndLowDimSegments(self.data['50l'][1], n_components=9, smoothingWindow=130); progress += 1; bar.update(progress)
		robert60r=m.getHighAndLowDimSegments(self.data['60r'][1], n_components=9, smoothingWindow=200); progress += 1; bar.update(progress)
		robert60l=m.getHighAndLowDimSegments(self.data['60l'][1], n_components=9, smoothingWindow=130); progress += 1; bar.update(progress)
		robert70r=m.getHighAndLowDimSegments(self.data['70r'][1], n_components=9, smoothingWindow=130); progress += 1; bar.update(progress)
		robert70l=m.getHighAndLowDimSegments(self.data['70l'][1], n_components=9, smoothingWindow=130); progress += 1; bar.update(progress)
		robert80r=m.getHighAndLowDimSegments(self.data['80r'][1], n_components=9, smoothingWindow=190); progress += 1; bar.update(progress)
		robert80l=m.getHighAndLowDimSegments(self.data['80l'][1], n_components=9, smoothingWindow=130); progress += 1; bar.update(progress)
		robert90r=m.getHighAndLowDimSegments(self.data['90r'][1], n_components=9, smoothingWindow=150); progress += 1; bar.update(progress)
		robert90l=m.getHighAndLowDimSegments(self.data['90l'][1], n_components=9, smoothingWindow=130); progress += 1; bar.update(progress)

		laura10r=m.getHighAndLowDimSegments(self.data['10r'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura10l=m.getHighAndLowDimSegments(self.data['10l'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura20r=m.getHighAndLowDimSegments(self.data['20r'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura20l=m.getHighAndLowDimSegments(self.data['20l'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura30r=m.getHighAndLowDimSegments(self.data['30r'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura30l=m.getHighAndLowDimSegments(self.data['30l'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura40r=m.getHighAndLowDimSegments(self.data['40r'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura40l=m.getHighAndLowDimSegments(self.data['40l'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura50r=m.getHighAndLowDimSegments(self.data['50r'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura50l=m.getHighAndLowDimSegments(self.data['50l'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura60r=m.getHighAndLowDimSegments(self.data['60r'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura60l=m.getHighAndLowDimSegments(self.data['60l'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura70r=m.getHighAndLowDimSegments(self.data['70r'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura70l=m.getHighAndLowDimSegments(self.data['70l'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura80r=m.getHighAndLowDimSegments(self.data['80r'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura80l=m.getHighAndLowDimSegments(self.data['80l'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura90r=m.getHighAndLowDimSegments(self.data['90r'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)
		laura90l=m.getHighAndLowDimSegments(self.data['90l'][2], n_components=9, smoothingWindow=100); progress += 1; bar.update(progress)

		#Delete bad segments and throw some away anyway - there are plenty to spare!
		
		dan10r=([],[],dan10r[2]) # This was garbage
		dan10l=(dan10l[0][2:-2],dan10l[1][2:-2],dan10l[2])
		dan20r=(dan20r[0][2:-2],dan20r[1][2:-2],dan20r[2])
		dan20l=(dan20l[0][2:-2],dan20l[1][2:-2],dan20l[2])
		dan30r=(dan30r[0][2:-2],dan30r[1][2:-2],dan30r[2])
		dan30l=(dan30l[0][2:-2],dan30l[1][2:-2],dan30l[2])
		dan40r=(dan40r[0][2:-2],dan40r[1][2:-2],dan40r[2])
		dan40l=(dan40l[0][2:-2],dan40l[1][2:-2],dan40l[2])
		dan50r=(dan50r[0][2:-2],dan50r[1][2:-2],dan50r[2])
		dan50l=(dan50l[0][2:-2],dan50l[1][2:-2],dan50l[2])
		dan60r=(dan60r[0][2:-2],dan60r[1][2:-2],dan60r[2])
		dan60l=(dan60l[0][2:-2],dan60l[1][2:-2],dan60l[2])
		dan70r=(dan70r[0][2:-2],dan70r[1][2:-2],dan70r[2])
		dan70l=(dan70l[0][2:-2],dan70l[1][2:-2],dan70l[2])
		dan80r=(dan80r[0][2:-2],dan80r[1][2:-2],dan80r[2])
		dan80l=(dan80l[0][2:-2],dan80l[1][2:-2],dan80l[2])
		dan90r=(dan90r[0][2:-2],dan90r[1][2:-2],dan90r[2])
		dan90l=(dan90l[0][2:-2],dan90l[1][2:-2],dan90l[2])

		robert10r=(robert10r[0][2:-2],robert10r[1][2:-2],robert10r[2])
		robert10l=(robert10l[0][2:-2],robert10l[1][2:-2],robert10l[2])
		robert20r=(robert20r[0][2:-2],robert20r[1][2:-2],robert20r[2])
		robert20l=(robert20l[0][2:-2],robert20l[1][2:-2],robert20l[2])
		robert30r=(robert30r[0][2:-2],robert30r[1][2:-2],robert30r[2])
		robert30l=(robert30l[0][2:-2],robert30l[1][2:-2],robert30l[2])
		robert40r=(robert40r[0][2:-2],robert40r[1][2:-2],robert40r[2])
		robert40l=(robert40l[0][2:-2],robert40l[1][2:-2],robert40l[2])
		robert50r=(robert50r[0][2:-2],robert50r[1][2:-2],robert50r[2])
		robert50l=(robert50l[0][2:-2],robert50l[1][2:-2],robert50l[2])
		robert60r=(robert60r[0][2:-2],robert60r[1][2:-2],robert60r[2])
		robert60l=(robert60l[0][2:-2],robert60l[1][2:-2],robert60l[2])
		robert70r=(robert70r[0][2:-2],robert70r[1][2:-2],robert70r[2])
		robert70l=(robert70l[0][2:-2],robert70l[1][2:-2],robert70l[2])
		robert80r=(robert80r[0][2:-2],robert80r[1][2:-2],robert80r[2])
		robert80l=(robert80l[0][2:-2],robert80l[1][2:-2],robert80l[2])
		robert90r=(robert90r[0][2:-2],robert90r[1][2:-2],robert90r[2])
		robert90l=(robert90l[0][2:-2],robert90l[1][2:-2],robert90l[2])

		laura10r=(laura10r[0][2:-2],laura10r[1][2:-2],laura10r[2])
		laura10l=(laura10l[0][2:-2],laura10l[1][2:-2],laura10l[2])
		laura20r=(laura20r[0][2:-2],laura20r[1][2:-2],laura20r[2])
		laura20l=(laura20l[0][2:-2],laura20l[1][2:-2],laura20l[2])
		laura30r=(laura30r[0][2:-2],laura30r[1][2:-2],laura30r[2])
		laura30l=(laura30l[0][2:-2],laura30l[1][2:-2],laura30l[2])
		laura40r=(laura40r[0][2:-2],laura40r[1][2:-2],laura40r[2])
		laura40l=(laura40l[0][2:-2],laura40l[1][2:-2],laura40l[2])
		laura50r=(laura50r[0][2:-2],laura50r[1][2:-2],laura50r[2])
		laura50l=(laura50l[0][2:-2],laura50l[1][2:-2],laura50l[2])
		laura60r=(laura60r[0][2:-2],laura60r[1][2:-2],laura60r[2])
		laura60l=(laura60l[0][2:-2],laura60l[1][2:-2],laura60l[2])
		laura70r=(laura70r[0][2:-2],laura70r[1][2:-2],laura70r[2])
		laura70l=(laura70l[0][2:-2],laura70l[1][2:-2],laura70l[2])
		laura80r=(laura80r[0][2:-2],laura80r[1][2:-2],laura80r[2])
		laura80l=(laura80l[0][2:-2],laura80l[1][2:-2],laura80l[2])
		laura90r=(laura90r[0][2:-2],laura90r[1][2:-2],laura90r[2])
		laura90l=(laura90l[0][2:-2],laura90l[1][2:-2],laura90l[2])

		self.HDsegs={'10l':[dan10l[0],robert10l[0],laura10l[0]],'20l':[dan20l[0],robert20l[0],laura20l[0]],'30l':[dan30l[0],robert30l[0],laura30l[0]],'40l':[dan40l[0],robert40l[0],laura40l[0]],'50l':[dan50l[0],robert50l[0],laura50l[0]],'60l':[dan60l[0],robert60l[0],laura60l[0]],'70l':[dan70l[0],robert70l[0],laura70l[0]],'80l':[dan80l[0],robert80l[0],laura80l[0]],'90l':[dan90l[0],robert90l[0],laura90l[0]],
		             '10r':[dan10r[0],robert10r[0],laura10r[0]],'20r':[dan20r[0],robert20r[0],laura20r[0]],'30r':[dan30r[0],robert30r[0],laura30r[0]],'40r':[dan40r[0],robert40r[0],laura40r[0]],'50r':[dan50r[0],robert50r[0],laura50r[0]],'60r':[dan60r[0],robert60r[0],laura60r[0]],'70r':[dan70r[0],robert70r[0],laura70r[0]],'80r':[dan80r[0],robert80r[0],laura80r[0]],'90r':[dan90r[0],robert90r[0],laura90r[0]]}

		self.LDsegs={'10l':[dan10l[1],robert10l[1],laura10l[1]],'20l':[dan20l[1],robert20l[1],laura20l[1]],'30l':[dan30l[1],robert30l[1],laura30l[1]],'40l':[dan40l[1],robert40l[1],laura40l[1]],'50l':[dan50l[1],robert50l[1],laura50l[1]],'60l':[dan60l[1],robert60l[1],laura60l[1]],'70l':[dan70l[1],robert70l[1],laura70l[1]],'80l':[dan80l[1],robert80l[1],laura80l[1]],'90l':[dan90l[1],robert90l[1],laura90l[1]],
		             '10r':[dan10r[1],robert10r[1],laura10r[1]],'20r':[dan20r[1],robert20r[1],laura20r[1]],'30r':[dan30r[1],robert30r[1],laura30r[1]],'40r':[dan40r[1],robert40r[1],laura40r[1]],'50r':[dan50r[1],robert50r[1],laura50r[1]],'60r':[dan60r[1],robert60r[1],laura60r[1]],'70r':[dan70r[1],robert70r[1],laura70r[1]],'80r':[dan80r[1],robert80r[1],laura80r[1]],'90r':[dan90r[1],robert90r[1],laura90r[1]]}

		# storing high and low dim segments under each key (only for Laura I at the moment)
		self.segs = {'10l':[laura10l[0][1:-1],laura10l[1][1:-1]],'20l':[laura20l[0][1:-1],laura20l[1][1:-1]],'30l':[laura30l[0][1:-1],laura30l[1][1:-1]],'40l':[laura40l[0][1:-1],laura40l[1][1:-1]],'50l':[laura50l[0][1:-1],laura50l[1][1:-1]],'60l':[laura60l[0][1:-1],laura60l[1][1:-1]],'70l':[laura70l[0][1:-1],laura70l[1][1:-1]],'80l':[laura80l[0][1:-1],laura80l[1][1:-1]],'90l':[laura90l[0][1:7]+laura90l[0][9:-1],laura90l[1][1:7]+laura90l[1][9:-1]],
		             '10r':[laura10r[0][1:-1],laura10r[1][1:-1]],'20r':[laura20r[0][1:-1],laura20r[1][1:-1]],'30r':[laura30r[0][1:-1],laura30r[1][1:-1]],'40r':[laura40r[0][1:-1],laura40r[1][1:-1]],'50r':[laura50r[0][1:-1],laura50r[1][1:-1]],'60r':[laura60r[0][1:-1],laura60r[1][1:-1]],'70r':[laura70r[0][1:-1],laura70r[1][1:-1]],'80r':[laura80r[0][1:-1],laura80r[1][1:-1]],'90r':[laura90r[0][1:-1],laura90r[1][1:-1]]}

		bar.finish()