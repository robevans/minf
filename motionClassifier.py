__author__ = 'Robert Evans'

import progressbar
import master as m

class circlesClassifier:
	def __init__(self, database=None):
			self.db = referenceCirclesDatabase()

	def classify(self, queryMotion):
		# TODO: this.



class referenceCirclesDatabase:
	def __init__(self):
		print "Initialising reference data..."
		bar = progressbar.ProgressBar(maxval=14, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		bar.start(); progress = 0
		self.data0a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius0cmHorizontal.txt")[26:,4:]
		self.data5a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius5cmHorizontal.txt")[26:,4:]
		self.data10a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius10cmHorizontal.txt")[26:,4:]
		self.data15a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius15cmHorizontal.txt")[26:,4:]
		self.data20a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius20cmHorizontal.txt")[26:,4:]
		self.data25a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius25cmHorizontal.txt")[26:,4:]
		self.data0c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius0cmHorizontal.txt")[26:,4:]
		self.data5c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius5cmHorizontal.txt")[26:,4:]
		self.data10c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius10cmHorizontal.txt")[26:,4:]
		self.data15c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius15cmHorizontal.txt")[26:,4:]
		self.data20c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius20cmHorizontal.txt")[26:,4:]
		self.data25c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius25cmHorizontal.txt")[26:,4:];
		progress += 1; bar.update(progress)

		(HDsegs0a,LDsegs0a,self.w0a) = m.getHighAndLowDimSegments(self.data0a, n_components=9); progress += 1; bar.update(progress)
		(HDsegs5a,LDsegs5a,self.w5a) = m.getHighAndLowDimSegments(self.data5a, n_components=9); progress += 1; bar.update(progress)
		(HDsegs10a,LDsegs10a,self.w10a) = m.getHighAndLowDimSegments(self.data10a, n_components=9); progress += 1; bar.update(progress)
		(HDsegs15a,LDsegs15a,self.w15a) = m.getHighAndLowDimSegments(self.data15a, n_components=9); progress += 1; bar.update(progress)
		(HDsegs20a,LDsegs20a,self.w20a) = m.getHighAndLowDimSegments(self.data20a, n_components=9); progress += 1; bar.update(progress)
		(HDsegs25a,LDsegs25a,self.w25a) = m.getHighAndLowDimSegments(self.data25a, n_components=9); progress += 1; bar.update(progress)
		(HDsegs0b,LDsegs0b,self.w0b) = m.getHighAndLowDimSegments(self.data0c, n_components=9); progress += 1; bar.update(progress)
		(HDsegs5b,LDsegs5b,self.w5b) = m.getHighAndLowDimSegments(self.data5c, n_components=9); progress += 1; bar.update(progress)
		(HDsegs10b,LDsegs10b,self.w10b) = m.getHighAndLowDimSegments(self.data10c, n_components=9); progress += 1; bar.update(progress)
		(HDsegs15b,LDsegs15b,self.w15b) = m.getHighAndLowDimSegments(self.data15c, n_components=9); progress += 1; bar.update(progress)
		(HDsegs20b,LDsegs20b,self.w20b) = m.getHighAndLowDimSegments(self.data20c, n_components=9); progress += 1; bar.update(progress)
		(HDsegs25b,LDsegs25b,self.w25b) = m.getHighAndLowDimSegments(self.data25c, n_components=9); progress += 1; bar.update(progress)
		
		self.HDsegs20a=HDsegs20a[:-1]
		self.HDsegs25a=HDsegs25a[1:]
		self.HDsegs0b=HDsegs0b[1:-1]
		self.HDsegs5b=HDsegs5b[1:]
		self.HDsegs10b=HDsegs10b[:-1]
		self.HDsegs15b=HDsegs15b[1:-1]
		self.HDsegs20b=HDsegs20b[1:-1]
		self.HDsegs25b=HDsegs25b[1:-1]
		self.LDsegs20a=LDsegs20a[:-1]
		self.LDsegs25a=LDsegs25a[1:]
		self.LDsegs0b=LDsegs0b[1:-1]
		self.LDsegs5b=LDsegs5b[1:]
		self.LDsegs10b=LDsegs10b[:-1]
		self.LDsegs15b=LDsegs15b[1:-1]
		self.LDsegs20b=LDsegs20b[1:-1]
		self.LDsegs25b=LDsegs25b[1:-1]
		progress += 1; bar.update(progress)
		bar.finish()