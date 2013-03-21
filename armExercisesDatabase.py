__author__ = 'Robert Evans'

import master as m
import progressbar
import pca as p

class db:
	def __init__ (self, computeSegments=False):
		print "Reading data..."
		dan10r=m.readRaw("captures/armExercise/Up and sideways/danr10.txt")[26:,4:]
		dan10l=m.readRaw("captures/armExercise/Up and sideways/danl10.txt")[26:,4:]
		dan20r=m.readRaw("captures/armExercise/Up and sideways/danr20.txt")[26:,4:]
		dan20l=m.readRaw("captures/armExercise/Up and sideways/danl20.txt")[26:,4:]
		dan30r=m.readRaw("captures/armExercise/Up and sideways/danr30.txt")[26:,4:]
		dan30l=m.readRaw("captures/armExercise/Up and sideways/danl30.txt")[26:,4:]
		dan40r=m.readRaw("captures/armExercise/Up and sideways/danr40.txt")[26:,4:]
		dan40l=m.readRaw("captures/armExercise/Up and sideways/danl40.txt")[26:,4:]
		dan50r=m.readRaw("captures/armExercise/Up and sideways/danr50.txt")[26:,4:]
		dan50l=m.readRaw("captures/armExercise/Up and sideways/danl50.txt")[26:,4:]
		dan60r=m.readRaw("captures/armExercise/Up and sideways/danr60.txt")[26:,4:]
		dan60l=m.readRaw("captures/armExercise/Up and sideways/danl60.txt")[26:,4:]
		dan70r=m.readRaw("captures/armExercise/Up and sideways/danr70.txt")[26:,4:]
		dan70l=m.readRaw("captures/armExercise/Up and sideways/danl70.txt")[26:,4:]
		dan80r=m.readRaw("captures/armExercise/Up and sideways/danr80.txt")[26:,4:]
		dan80l=m.readRaw("captures/armExercise/Up and sideways/danl80.txt")[26:,4:]
		dan90r=m.readRaw("captures/armExercise/Up and sideways/danr90.txt")[26:,4:]
		dan90l=m.readRaw("captures/armExercise/Up and sideways/danl90.txt")[26:,4:]
		laura10r=m.readRaw("captures/armExercise/Up/laura10r.txt")[26:,4:]
		laura10l=m.readRaw("captures/armExercise/Up/laura10l.txt")[26:,4:]
		laura20r=m.readRaw("captures/armExercise/Up/laura20r.txt")[26:,4:]
		laura20l=m.readRaw("captures/armExercise/Up/laura20l.txt")[26:,4:]
		laura30r=m.readRaw("captures/armExercise/Up/laura30r.txt")[26:,4:]
		laura30l=m.readRaw("captures/armExercise/Up/laura30l.txt")[26:,4:]
		laura40r=m.readRaw("captures/armExercise/Up/laura40r.txt")[26:,4:]
		laura40l=m.readRaw("captures/armExercise/Up/laura40l.txt")[26:,4:]
		laura50r=m.readRaw("captures/armExercise/Up/laura50r.txt")[26:,4:]
		laura50l=m.readRaw("captures/armExercise/Up/laura50l.txt")[26:,4:]
		laura60r=m.readRaw("captures/armExercise/Up/laura60r.txt")[26:,4:]
		laura60l=m.readRaw("captures/armExercise/Up/laura60l.txt")[26:,4:]
		laura70r=m.readRaw("captures/armExercise/Up/laura70r.txt")[26:,4:]
		laura70l=m.readRaw("captures/armExercise/Up/laura70l.txt")[26:,4:]
		laura80r=m.readRaw("captures/armExercise/Up/laura80r.txt")[26:,4:]
		laura80l=m.readRaw("captures/armExercise/Up/laura80l.txt")[26:,4:]
		laura90r=m.readRaw("captures/armExercise/Up/laura90r.txt")[26:,4:]
		laura90l=m.readRaw("captures/armExercise/Up/laura90l.txt")[26:,4:]

		self.data = {'10l':[dan10l,laura10l],'20l':[dan20l,laura20l],'30l':[dan30l,laura30l],'40l':[dan40l,laura40l],'50l':[dan50l,laura50l],'60l':[dan60l,laura60l],'70l':[dan70l,laura70l],'80l':[dan80l,laura80l],'90l':[dan90l,laura90l],
		             '10r':[dan10r,laura10r],'20r':[dan20r,laura20r],'30r':[dan30r,laura30r],'40r':[dan40r,laura40r],'50r':[dan50r,laura50r],'60r':[dan60r,laura60r],'70r':[dan70r,laura70r],'80r':[dan80r,laura80r],'90r':[dan90r,laura90r]}

		"""
		dan22r=m.readRaw("captures/armExercise/dan22r.txt")[26:,4:]
		dan45l=m.readRaw("captures/armExercise/dan45l.txt")[26:,4:]
		dan45r=m.readRaw("captures/armExercise/dan45r.txt")[26:,4:]
		dan67l=m.readRaw("captures/armExercise/dan67l.txt")[26:,4:]
		dan67r=m.readRaw("captures/armExercise/dan67r.txt")[26:,4:]
		dan90l=m.readRaw("captures/armExercise/dan90l.txt")[26:,4:]
		dan90r=m.readRaw("captures/armExercise/dan90r.txt")[26:,4:]
		self.data = {'22l':dan22l,'22r':dan22r, '45l':dan45l, '45r':dan45r, '67l':dan67l, '67r':dan67r, '90l':dan90l,'90r':dan90r}
		print "Computing dimensionality reduction..."
		pcadan22l=p.pca(dan22l,n_components=9)
		pcadan22r=p.pca(dan22r,n_components=9)
		pcadan45l=p.pca(dan45l,n_components=9)
		pcadan45r=p.pca(dan45r,n_components=9)
		pcadan67l=p.pca(dan67l,n_components=9)
		pcadan67r=p.pca(dan67r,n_components=9)
		pcadan90l=p.pca(dan90l,n_components=9)
		pcadan90r=p.pca(dan90r,n_components=9)
		self.pca = {'22l':pcadan22l,'22r':pcadan22r, '45l':pcadan45l, '45r':pcadan45r, '67l':pcadan67l, '67r':pcadan67r, '90l':pcadan90l,'90r':pcadan90r}
		"""

		print "Computing dimensionality reduction..."
		PCAdan10r=p.pca(dan10r,n_components=9)
		PCAdan10l=p.pca(dan10l,n_components=9)
		PCAdan20r=p.pca(dan20r,n_components=9)
		PCAdan20l=p.pca(dan20l,n_components=9)
		PCAdan30r=p.pca(dan30r,n_components=9)
		PCAdan30l=p.pca(dan30l,n_components=9)
		PCAdan40r=p.pca(dan40r,n_components=9)
		PCAdan40l=p.pca(dan40l,n_components=9)
		PCAdan50r=p.pca(dan50r,n_components=9)
		PCAdan50l=p.pca(dan50l,n_components=9)
		PCAdan60r=p.pca(dan60r,n_components=9)
		PCAdan60l=p.pca(dan60l,n_components=9)
		PCAdan70r=p.pca(dan70r,n_components=9)
		PCAdan70l=p.pca(dan70l,n_components=9)
		PCAdan80r=p.pca(dan80r,n_components=9)
		PCAdan80l=p.pca(dan80l,n_components=9)
		PCAdan90r=p.pca(dan90r,n_components=9)
		PCAdan90l=p.pca(dan90l,n_components=9)
		PCAlaura10r=p.pca(laura10r,n_components=9)
		PCAlaura10l=p.pca(laura10l,n_components=9)
		PCAlaura20r=p.pca(laura20r,n_components=9)
		PCAlaura20l=p.pca(laura20l,n_components=9)
		PCAlaura30r=p.pca(laura30r,n_components=9)
		PCAlaura30l=p.pca(laura30l,n_components=9)
		PCAlaura40r=p.pca(laura40r,n_components=9)
		PCAlaura40l=p.pca(laura40l,n_components=9)
		PCAlaura50r=p.pca(laura50r,n_components=9)
		PCAlaura50l=p.pca(laura50l,n_components=9)
		PCAlaura60r=p.pca(laura60r,n_components=9)
		PCAlaura60l=p.pca(laura60l,n_components=9)
		PCAlaura70r=p.pca(laura70r,n_components=9)
		PCAlaura70l=p.pca(laura70l,n_components=9)
		PCAlaura80r=p.pca(laura80r,n_components=9)
		PCAlaura80l=p.pca(laura80l,n_components=9)
		PCAlaura90r=p.pca(laura90r,n_components=9)
		PCAlaura90l=p.pca(laura90l,n_components=9)

		self.pca = {'10l':[PCAdan10l,PCAlaura10l],'20l':[PCAdan20l,PCAlaura20l],'30l':[PCAdan30l,PCAlaura30l],'40l':[PCAdan40l,PCAlaura40l],'50l':[PCAdan50l,PCAlaura50l],'60l':[PCAdan60l,PCAlaura60l],'70l':[PCAdan70l,PCAlaura70l],'80l':[PCAdan80l,PCAlaura80l],'90l':[PCAdan90l,PCAlaura90l],
		            '10r':[PCAdan10r,PCAlaura10r],'20r':[PCAdan20r,PCAlaura20r],'30r':[PCAdan30r,PCAlaura30r],'40r':[PCAdan40r,PCAlaura40r],'50r':[PCAdan50r,PCAlaura50r],'60r':[PCAdan60r,PCAlaura60r],'70r':[PCAdan70r,PCAlaura70r],'80r':[PCAdan80r,PCAlaura80r],'90r':[PCAdan90r,PCAlaura90r]}


		if computeSegments:
			self.computeSegments()

		print "Database ready"

	def computeSegments(self):
		print "Segmenting data..."
		bar = progressbar.ProgressBar(maxval=18, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		bar.start(); progress = 0
		laura10r=m.getHighAndLowDimSegments(self.data['10r'][1], n_components=9); progress += 1; bar.update(progress)
		laura10l=m.getHighAndLowDimSegments(self.data['10l'][1], n_components=9); progress += 1; bar.update(progress)
		laura20r=m.getHighAndLowDimSegments(self.data['20r'][1], n_components=9); progress += 1; bar.update(progress)
		laura20l=m.getHighAndLowDimSegments(self.data['20l'][1], n_components=9); progress += 1; bar.update(progress)
		laura30r=m.getHighAndLowDimSegments(self.data['30r'][1], n_components=9); progress += 1; bar.update(progress)
		laura30l=m.getHighAndLowDimSegments(self.data['30l'][1], n_components=9); progress += 1; bar.update(progress)
		laura40r=m.getHighAndLowDimSegments(self.data['40r'][1], n_components=9); progress += 1; bar.update(progress)
		laura40l=m.getHighAndLowDimSegments(self.data['40l'][1], n_components=9); progress += 1; bar.update(progress)
		laura50r=m.getHighAndLowDimSegments(self.data['50r'][1], n_components=9); progress += 1; bar.update(progress)
		laura50l=m.getHighAndLowDimSegments(self.data['50l'][1], n_components=9); progress += 1; bar.update(progress)
		laura60r=m.getHighAndLowDimSegments(self.data['60r'][1], n_components=9); progress += 1; bar.update(progress)
		laura60l=m.getHighAndLowDimSegments(self.data['60l'][1], n_components=9); progress += 1; bar.update(progress)
		laura70r=m.getHighAndLowDimSegments(self.data['70r'][1], n_components=9); progress += 1; bar.update(progress)
		laura70l=m.getHighAndLowDimSegments(self.data['70l'][1], n_components=9); progress += 1; bar.update(progress)
		laura80r=m.getHighAndLowDimSegments(self.data['80r'][1], n_components=9); progress += 1; bar.update(progress)
		laura80l=m.getHighAndLowDimSegments(self.data['80l'][1], n_components=9); progress += 1; bar.update(progress)
		laura90r=m.getHighAndLowDimSegments(self.data['90r'][1], n_components=9); progress += 1; bar.update(progress)
		laura90l=m.getHighAndLowDimSegments(self.data['90l'][1], n_components=9); progress += 1; bar.update(progress)

		self.segs = {'10l':[laura10l[0][1:-1],laura10l[1][1:-1]],'20l':[laura20l[0][1:-1],laura20l[1][1:-1]],'30l':[laura30l[0][1:-1],laura30l[1][1:-1]],'40l':[laura40l[0][1:-1],laura40l[1][1:-1]],'50l':[laura50l[0][1:-1],laura50l[1][1:-1]],'60l':[laura60l[0][1:-1],laura60l[1][1:-1]],'70l':[laura70l[0][1:-1],laura70l[1][1:-1]],'80l':[laura80l[0][1:-1],laura80l[1][1:-1]],'90l':[laura90l[0][1:6]+laura90l[0][8:-1],laura90l[1][1:7]+laura90l[1][9:-1]],
		            '10r':[laura10r[0][1:-1],laura10r[1][1:-1]],'20r':[laura20r[0][1:-1],laura20r[1][1:-1]],'30r':[laura30r[0][1:-1],laura30r[1][1:-1]],'40r':[laura40r[0][1:-1],laura40r[1][1:-1]],'50r':[laura50r[0][1:-1],laura50r[1][1:-1]],'60r':[laura60r[0][1:-1],laura60r[1][1:-1]],'70r':[laura70r[0][1:-1],laura70r[1][1:-1]],'80r':[laura80r[0][1:-1],laura80r[1][1:-1]],'90r':[laura90r[0][1:-1],laura90r[1][1:-1]]}

		bar.finish()