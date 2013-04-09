import pylab
import master as m
import pca
import segment

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
data25c=m.readRaw("captures/mechanicalArm/ArmLength60cm/Clockwise/radius25cmHorizontal.txt")[26:,4:]

pylab.matplotlib.rcParams.update({'font.size': 26})

data=[data0a,data5a,data10a,data15a,data20a,data25a,data0c,data5c,data10c,data15c,data20c,data25c]

rawNames =["raw0a","raw5a","raw10a","raw15a","raw20a","raw25a","raw0c","raw5c","raw10c","raw15c","raw20c","raw25c"]
pcaNames =["pca0a","pca5a","pca10a","pca15a","pca20a","pca25a","pca0c","pca5c","pca10c","pca15c","pca20c","pca25c"]
segsNames =["segs0a","segs5a","segs10a","segs15a","segs20a","segs25a","segs0c","segs5c","segs10c","segs15c","segs20c","segs25c"]

for d,n in zip(data,rawNames):
	pylab.close()
	pylab.figure(figsize=(12,9))
	pylab.plot(d)
	pylab.xlabel('Time (frames)')
	pylab.ylabel('Sensor readings')
	pylab.title('Raw data',fontsize=50)
	pylab.tight_layout()
	pylab.savefig('/Users/robertevans/repos/minf/Appendix/%s.png'%n, format='png', dpi=300)

for d,n in zip(data,pcaNames):
	pylab.close()
	pylab.figure(figsize=(12,9))
	pylab.plot(pca.pca(d)[0])
	pylab.xlabel('Time (frames)')
	pylab.ylabel('Latent value')
	pylab.title('Three Principal Components',fontsize=50)
	pylab.tight_layout()
	pylab.savefig('/Users/robertevans/repos/minf/Appendix/%s.png'%n, format='png', dpi=300)

for d,n in zip(data,segsNames):
	pylab.close()
	P = pca.pca(d)[0][:,0]
	(mins,maxs) = segment.segmentationPoints(P, windowSize=100)
	pylab.figure(figsize=(12,9))
	pylab.plot(P)
	for m in maxs:
		pylab.axvline(m,color='r',linewidth=1.5)
	pylab.xlabel('Time (frames)')
	pylab.ylabel('Latent value')
	pylab.title('Automatic segmentation',fontsize=50)
	pylab.tight_layout()
	pylab.savefig('/Users/robertevans/repos/minf/Appendix/%s.png'%n, format='png', dpi=300)