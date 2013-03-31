__author__ = 'Robert Evans'

import master as m
import progressbar
import pca as p

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
		
		PCArobert10r=p.pca(robert10r,n_components=9)
		PCArobert10l=p.pca(robert10l,n_components=9)
		PCArobert20r=p.pca(robert20r,n_components=9)
		PCArobert20l=p.pca(robert20l,n_components=9)
		PCArobert30r=p.pca(robert30r,n_components=9)
		PCArobert30l=p.pca(robert30l,n_components=9)
		PCArobert40r=p.pca(robert40r,n_components=9)
		PCArobert40l=p.pca(robert40l,n_components=9)
		PCArobert50r=p.pca(robert50r,n_components=9)
		PCArobert50l=p.pca(robert50l,n_components=9)
		PCArobert60r=p.pca(robert60r,n_components=9)
		PCArobert60l=p.pca(robert60l,n_components=9)
		PCArobert70r=p.pca(robert70r,n_components=9)
		PCArobert70l=p.pca(robert70l,n_components=9)
		PCArobert80r=p.pca(robert80r,n_components=9)
		PCArobert80l=p.pca(robert80l,n_components=9)
		PCArobert90r=p.pca(robert90r,n_components=9)
		PCArobert90l=p.pca(robert90l,n_components=9)

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

		self.pca = {'10l':[PCAdan10l,PCArobert10l,PCAlaura10l],'20l':[PCAdan20l,PCArobert20l,PCAlaura20l],'30l':[PCAdan30l,PCArobert30l,PCAlaura30l],'40l':[PCAdan40l,PCArobert40l,PCAlaura40l],'50l':[PCAdan50l,PCArobert50l,PCAlaura50l],'60l':[PCAdan60l,PCArobert60l,PCAlaura60l],'70l':[PCAdan70l,PCArobert70l,PCAlaura70l],'80l':[PCAdan80l,PCArobert80l,PCAlaura80l],'90l':[PCAdan90l,PCArobert90l,PCAlaura90l],
		            '10r':[PCAdan10r,PCArobert10r,PCAlaura10r],'20r':[PCAdan20r,PCArobert20r,PCAlaura20r],'30r':[PCAdan30r,PCArobert30r,PCAlaura30r],'40r':[PCAdan40r,PCArobert40r,PCAlaura40r],'50r':[PCAdan50r,PCArobert50r,PCAlaura50r],'60r':[PCAdan60r,PCArobert60r,PCAlaura60r],'70r':[PCAdan70r,PCArobert70r,PCAlaura70r],'80r':[PCAdan80r,PCArobert80r,PCAlaura80r],'90r':[PCAdan90r,PCArobert90r,PCAlaura90r]}

		self.pcaDataOnly = {key:[tuple[0] for tuple in value] for key,value in self.pca.iteritems()}
		self.explainedVariances = {key:[tuple[1] for tuple in value] for key,value in self.pca.iteritems()}
		self.averageExplainedVariance = [float(sum(t))/len(t) for t in zip(*[[float(sum(t))/len(t) for t in zip(*l)] for l in self.explainedVariances.values()])]

		if computeSegments:
			self.computeSegments()

		print "Database ready"

	def computeSegments(self):
		print "Segmenting data..."
		bar = progressbar.ProgressBar(maxval=54, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		bar.start(); progress = 0

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