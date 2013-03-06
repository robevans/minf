__author__ = 'Andrew'

from commsTDMA import *
from pylab import plot, show, array,copy,figure,shape,l2norm, empty, amap, mean, loadtxt
from scipy.optimize import leastsq
from mayavi import mlab

DEVICE_ID = 7

CAPTURE_TIME_MINS = 0.5
SEND_FREQ=1

class MagCalibration:
    def __init__(self, id, offline=False):
        self.id = id
        self.magSampleList = []
        self.count = 0
        self.filename = "./calibration/" + str(self.id) + ".cal"
        if offline:
            # load data from file
            #file = open("filename", mode='r')
            data = loadtxt(self.filename, skiprows=3, delimiter=',')

            for i in range(len(data)):
                x = data[i,0]
                y = data[i,1]
                z = data[i,2]

                mag = (x,y,z)

                self.magSampleList.append(mag)

        else:
            self.collectData = True
            self.c = CaptureThread(self.handleData)
            self.c.start()
            print "rotate device in all axes for 30 seconds..."
            #raw_input("Rotate device. Press ENTER when done...")
            sleep(10)
            print "20" + " (" + str(len(self.magSampleList)) + ")"
            sleep(10)
            print "10" + " (" + str(len(self.magSampleList)) + ")"
            sleep(10)
            print "Done" + " (" + str(len(self.magSampleList)) + ")"
            self.collectData = False
            self.c.stop = True

        self.processData()

    def handleData(self, data):
        if self.collectData and self.id == data[NODE_ID]:
            self.magSampleList.append(data[MAG])

    def processData(self):

        print self.magSampleList
        #plot(array(self.magSampleList))
        #show()

        self.mags = array(self.magSampleList)

        xs = self.mags[:,0]
        ys = self.mags[:,1]
        zs = self.mags[:,2]

        cxs, x_offset, x_scale = self.applyCalibration(xs)
        cys, y_offset, y_scale = self.applyCalibration(ys)
        czs, z_offset, z_scale = self.applyCalibration(zs)


        def residuals(params,x,y,z):
            xo = params[0]
            xs = params[1]
            yo = params[2]
            ys = params[3]
            zo = params[4]
            zs = params[5]

            xc = empty(shape(x))
            for i in range(len(x)):
                xc[i] = (x[i] - xo) * xs

            yc = empty(shape(y))
            for i in range(len(y)):
                yc[i] = (y[i] - yo) * ys

            zc = empty(shape(z))
            for i in range(len(z)):
                zc[i] = (z[i] - zo) * zs

            res = []
            for i in range(len(xc)):
                norm = l2norm(array([xc[i],yc[i],zc[i]])) - 1.0
                res.append(norm)

            return array(res)

        p0 = [x_offset, x_scale, y_offset, y_scale, z_offset, z_scale]
        ls =  leastsq(residuals, p0, args=(xs,ys,zs))

        x_offset = ls[0][0]
        x_scale = ls[0][1]
        y_offset = ls[0][2]
        y_scale = ls[0][3]
        z_offset = ls[0][4]
        z_scale = ls[0][5]

        cxs = self.applyCalibration(xs, calibration=(x_offset,x_scale))[0]
        cys = self.applyCalibration(ys, calibration=(y_offset,y_scale))[0]
        czs = self.applyCalibration(zs, calibration=(z_offset,z_scale))[0]


        calibratedMag = empty((len(cxs),3))
        calibratedMag[:,0] = cxs
        calibratedMag[:,1] = cys
        calibratedMag[:,2] = czs

        magnitudes = amap(lambda v: l2norm(v), calibratedMag)

        self.calibratedMag = calibratedMag

        mlab.points3d(cxs,cys,czs, scale_mode='none', scale_factor=0.02)
        #mlab.points3d(array([-1.0,1.0]),array([0.0,0.0]),array([0.0,0.0]), scale_mode='none', scale_factor=0.02)
        sphere = mlab.points3d(0,0,0, opacity=0.5, resolution=100, color=(1.0,0.0,0.0), scale_mode='none', scale_factor=2.0)
        sphere.actor.property.backface_culling = True
        mlab.show()
        figure()
        plot(magnitudes)
        show()

        # write calibration to a file

        f = open(self.filename,mode='w')
        f.write("id,x_offset,x_scale,y_offset,y_scale,z_offset,z_scale\n")
        f.write("%d,%f,%f,%f,%f,%f,%f\n"%(self.id,x_offset,x_scale,y_offset,y_scale,z_offset,z_scale))
        f.write("\n")

        for l in self.magSampleList:
            f.write("%d,%d,%d\n"%(l[0],l[1],l[2]))

        f.close()

        resError = []
        for i in range(len(cxs)):
            resError.append(self.calculateResidualError(cxs[i],cys[i],czs[i]))
        print len(resError)
        print mean(resError)

    def calculateResidualError(self,xs,ys,zs):
        errors = []
        norm = l2norm(array([xs,ys,zs])) - 1.0
        errors.append(norm * norm)
        return mean(errors)


    def applyCalibration(self,readings, calibration=None):
        def offsetAndScale(min,max):
            offset = (max + min) / 2.0
            oMax = max - offset
            oMin = min - offset
            scale = 2.0 / (oMax - oMin)
            return offset,scale

        if calibration is not None:
            offset = calibration[0]
            scale = calibration[1]
        else:
            offset,scale = offsetAndScale(min(readings), max(readings))

        data = copy(readings)
        for i in range(len(data)):
            data[i] = (data[i] - offset) * scale
        return data, offset, scale

if __name__ == '__main__':
    magcal = MagCalibration(DEVICE_ID, offline=False)
