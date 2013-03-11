__author__ = 'Robert Evans'

import master as m
import progressbar

class db:
	def __init__ (self):
		print "Gathering data..."
		bar = progressbar.ProgressBar(maxval=14, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		bar.start(); progress = 0
		data0a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius0cmHorizontal.txt")[26:,4:]
		data5a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius5cmHorizontal.txt")[26:,4:]
		data10a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius10cmHorizontal.txt")[26:,4:]
		data15a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius15cmHorizontal.txt")[26:,4:]
		data20a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius20cmHorizontal.txt")[26:,4:]
		data25a=m.readRaw("captures/mechanicalArm/ArmLength60cm/Anticlockwise/radius25cmHorizontal.txt")[26:,4:]
		data0c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius0cmHorizontal.txt")[26:,4:]
		data5c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius5cmHorizontal.txt")[26:,4:]
		data10c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius10cmHorizontal.txt")[26:,4:]
		data15c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius15cmHorizontal.txt")[26:,4:]
		data20c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius20cmHorizontal.txt")[26:,4:]
		data25c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius25cmHorizontal.txt")[26:,4:];
		progress += 1; bar.update(progress)

		(HDsegs0a,LDsegs0a,w0a) = m.getHighAndLowDimSegments(data0a, n_components=9); progress += 1; bar.update(progress)
		(HDsegs5a,LDsegs5a,w5a) = m.getHighAndLowDimSegments(data5a, n_components=9); progress += 1; bar.update(progress)
		(HDsegs10a,LDsegs10a,w10a) = m.getHighAndLowDimSegments(data10a, n_components=9); progress += 1; bar.update(progress)
		(HDsegs15a,LDsegs15a,w15a) = m.getHighAndLowDimSegments(data15a, n_components=9); progress += 1; bar.update(progress)
		(HDsegs20a,LDsegs20a,w20a) = m.getHighAndLowDimSegments(data20a, n_components=9); progress += 1; bar.update(progress)
		(HDsegs25a,LDsegs25a,w25a) = m.getHighAndLowDimSegments(data25a, n_components=9); progress += 1; bar.update(progress)
		(HDsegs0c,LDsegs0c,w0c) = m.getHighAndLowDimSegments(data0c, n_components=9); progress += 1; bar.update(progress)
		(HDsegs5c,LDsegs5c,w5c) = m.getHighAndLowDimSegments(data5c, n_components=9); progress += 1; bar.update(progress)
		(HDsegs10c,LDsegs10c,w10c) = m.getHighAndLowDimSegments(data10c, n_components=9); progress += 1; bar.update(progress)
		(HDsegs15c,LDsegs15c,w15c) = m.getHighAndLowDimSegments(data15c, n_components=9); progress += 1; bar.update(progress)
		(HDsegs20c,LDsegs20c,w20c) = m.getHighAndLowDimSegments(data20c, n_components=9); progress += 1; bar.update(progress)
		(HDsegs25c,LDsegs25c,w25c) = m.getHighAndLowDimSegments(data25c, n_components=9); progress += 1; bar.update(progress)
		
		HDsegs20a=HDsegs20a[:-1]
		HDsegs25a=HDsegs25a[1:]
		HDsegs0c=HDsegs0c[1:-1]
		HDsegs5c=HDsegs5c[1:]
		HDsegs10c=HDsegs10c[:-1]
		HDsegs15c=HDsegs15c[1:-1]
		HDsegs20c=HDsegs20c[1:-1]
		HDsegs25c=HDsegs25c[1:-1]
		LDsegs20a=LDsegs20a[:-1]
		LDsegs25a=LDsegs25a[1:]
		LDsegs0c=LDsegs0c[1:-1]
		LDsegs5c=LDsegs5c[1:]
		LDsegs10c=LDsegs10c[:-1]
		LDsegs15c=LDsegs15c[1:-1]
		LDsegs20c=LDsegs20c[1:-1]
		LDsegs25c=LDsegs25c[1:-1]

		self.data = {'clockwise0cm':data0a,'anticlockwise5cm':data5a, 'anticlockwise10cm':data10a, 'anticlockwise15cm':data15a, 'anticlockwise20cm':data20a, 'anticlockwise25cm':data25a,
					 'clockwise0cm':data0c,'clockwise5cm':data5c, 'clockwise10cm':data10c, 'clockwise15cm':data15c, 'clockwise20cm':data20c, 'clockwise25cm':data25c}
		self.HDsegments = {'anticlockwise0cm':HDsegs0a,'anticlockwise5cm':HDsegs5a, 'anticlockwise10cm':HDsegs10a, 'anticlockwise15cm':HDsegs15a, 'anticlockwise20cm':HDsegs20a, 'anticlockwise25cm':HDsegs25a,
						   'clockwise0cm':HDsegs0c,'clockwise5cm':HDsegs5c, 'clockwise10cm':HDsegs10c, 'clockwise15cm':HDsegs15c, 'clockwise20cm':HDsegs20c, 'clockwise25cm':HDsegs25c}
		self.LDsegments = {'anticlockwise0cm':LDsegs0a,'anticlockwise5cm':LDsegs5a, 'anticlockwise10cm':LDsegs10a, 'anticlockwise15cm':LDsegs15a, 'anticlockwise20cm':LDsegs20a, 'anticlockwise25cm':LDsegs25a,
						   'clockwise0cm':LDsegs0c,'clockwise5cm':LDsegs5c, 'clockwise10cm':LDsegs10c, 'clockwise15cm':LDsegs15c, 'clockwise20cm':LDsegs20c, 'clockwise25cm':LDsegs25c}
		progress += 1; bar.update(progress)
		bar.finish()