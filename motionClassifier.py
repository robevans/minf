__author__ = 'Robert Evans'

import progressbar
import master as m
import dtw

class circlesClassifier:
	def __init__(self, database=None):
			self.db = referenceCirclesDatabase()

	def classify(self, query):
		nearest = ''
		minDist = float("inf")

		dist = sum([dtw.dist(query,reference) for reference in self.db.HDsegs0a])/float(len(self.db.HDsegs0a))
		if dist < minDist:
			minDist = dist
			nearest = 'Anticlockwise radius=0cm'
		dist = sum([dtw.dist(query,reference) for reference in self.db.HDsegs5a])/float(len(self.db.HDsegs5a))
		if dist < minDist:
			minDist = dist
			nearest = 'Anticlockwise radius=5cm'
		dist = sum([dtw.dist(query,reference) for reference in self.db.HDsegs10a])/float(len(self.db.HDsegs10a))
		if dist < minDist:
			minDist = dist
			nearest = 'Anticlockwise radius=10cm'
		dist = sum([dtw.dist(query,reference) for reference in self.db.HDsegs15a])/float(len(self.db.HDsegs15a))
		if dist < minDist:
			minDist = dist
			nearest = 'Anticlockwise radius=15cm'
		dist = sum([dtw.dist(query,reference) for reference in self.db.HDsegs20a])/float(len(self.db.HDsegs20a))
		if dist < minDist:
			minDist = dist
			nearest = 'Anticlockwise radius=20cm'
		dist = sum([dtw.dist(query,reference) for reference in self.db.HDsegs25a])/float(len(self.db.HDsegs25a))
		if dist < minDist:
			minDist = dist
			nearest = 'Anticlockwise radius=25cm'
		dist = sum([dtw.dist(query,reference) for reference in self.db.HDsegs0c])/float(len(self.db.HDsegs0c))
		if dist < minDist:
			minDist = dist
			nearest = 'Clockwise radius=0cm'
		dist = sum([dtw.dist(query,reference) for reference in self.db.HDsegs5c])/float(len(self.db.HDsegs5c))
		if dist < minDist:
			minDist = dist
			nearest = 'Clockwise radius=5cm'
		dist = sum([dtw.dist(query,reference) for reference in self.db.HDsegs10c])/float(len(self.db.HDsegs10c))
		if dist < minDist:
			minDist = dist
			nearest = 'Clockwise radius=10cm'
		dist = sum([dtw.dist(query,reference) for reference in self.db.HDsegs15c])/float(len(self.db.HDsegs15c))
		if dist < minDist:
			minDist = dist
			nearest = 'Clockwise radius=15cm'
		dist = sum([dtw.dist(query,reference) for reference in self.db.HDsegs20c])/float(len(self.db.HDsegs20c))
		if dist < minDist:
			minDist = dist
			nearest = 'Clockwise radius=20cm'
		dist = sum([dtw.dist(query,reference) for reference in self.db.HDsegs25c])/float(len(self.db.HDsegs25c))
		if dist < minDist:
			minDist = dist
			nearest = 'Clockwise radius=25cm'

		return (nearest, minDist)



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

		(self.HDsegs0a,self.LDsegs0a,self.w0a) = m.getHighAndLowDimSegments(self.data0a, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs5a,self.LDsegs5a,self.w5a) = m.getHighAndLowDimSegments(self.data5a, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs10a,self.LDsegs10a,self.w10a) = m.getHighAndLowDimSegments(self.data10a, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs15a,self.LDsegs15a,self.w15a) = m.getHighAndLowDimSegments(self.data15a, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs20a,self.LDsegs20a,self.w20a) = m.getHighAndLowDimSegments(self.data20a, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs25a,self.LDsegs25a,self.w25a) = m.getHighAndLowDimSegments(self.data25a, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs0c,self.LDsegs0c,self.w0c) = m.getHighAndLowDimSegments(self.data0c, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs5c,self.LDsegs5c,self.w5c) = m.getHighAndLowDimSegments(self.data5c, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs10c,self.LDsegs10c,self.w10c) = m.getHighAndLowDimSegments(self.data10c, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs15c,self.LDsegs15c,self.w15c) = m.getHighAndLowDimSegments(self.data15c, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs20c,self.LDsegs20c,self.w20c) = m.getHighAndLowDimSegments(self.data20c, n_components=9); progress += 1; bar.update(progress)
		(self.HDsegs25c,self.LDsegs25c,self.w25c) = m.getHighAndLowDimSegments(self.data25c, n_components=9); progress += 1; bar.update(progress)
		
		self.HDsegs20a=self.HDsegs20a[:-1]
		self.HDsegs25a=self.HDsegs25a[1:]
		self.HDsegs0c=self.HDsegs0c[1:-1]
		self.HDsegs5c=self.HDsegs5c[1:]
		self.HDsegs10c=self.HDsegs10c[:-1]
		self.HDsegs15c=self.HDsegs15c[1:-1]
		self.HDsegs20c=self.HDsegs20c[1:-1]
		self.HDsegs25c=self.HDsegs25c[1:-1]
		self.LDsegs20a=self.LDsegs20a[:-1]
		self.LDsegs25a=self.LDsegs25a[1:]
		self.LDsegs0c=self.LDsegs0c[1:-1]
		self.LDsegs5c=self.LDsegs5c[1:]
		self.LDsegs10c=self.LDsegs10c[:-1]
		self.LDsegs15c=self.LDsegs15c[1:-1]
		self.LDsegs20c=self.LDsegs20c[1:-1]
		self.LDsegs25c=self.LDsegs25c[1:-1]
		progress += 1; bar.update(progress)
		bar.finish()