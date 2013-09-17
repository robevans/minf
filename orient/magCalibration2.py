__author__ = 'Andrew'

from comms import *
from pylab import plot, show, array,copy,figure,shape,l2norm, empty, amap, mean, loadtxt
from scipy.optimize import leastsq
from mayavi import mlab

class MagCalibration:
    def __init__(self, id, offline=False, write=True):
        self.id = id
        self.write=write
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
            self.c = CaptureThread(self.handleData)
            self.c.start()
            self.collectData = True
            raw_input("Rotate device. Press Enter when done...")
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

        x_offset, x_scale = self.initialCalibration(xs)
        y_offset, y_scale = self.initialCalibration(ys)
        z_offset, z_scale = self.initialCalibration(zs)

        cxs, cys, czs = self.applyCalibration(xs, ys, zs, x_o = x_offset, x_s = x_scale, y_o = y_offset, y_s = y_scale, z_o = z_offset, z_s = z_scale)

        resError = []
        for i in range(len(cxs)):
            resError.append(self.calculateResidualError(cxs[i],cys[i],czs[i]))
        print len(resError)
        print mean(resError) * 1000


        def residuals(params,x,y,z):
            xo = params[0]
            xs = params[1]
            yo = params[2]
            ys = params[3]
            zo = params[4]
            zs = params[5]
            xys = params[6]
            xzs = params[7]
            yzs = params[8]

            xc = empty(shape(x))
            yc = empty(shape(y))
            zc = empty(shape(z))
            for i in range(len(x)):
                _x = x[i] - xo
                _y = y[i] - yo
                _z = z[i] - zo

                xc[i] = _x * (xs + _y * xys + _z * xzs)
                yc[i] = _y * (ys + _z * yzs)
                zc[i] = _z * (zs)

            res = []
            for i in range(len(xc)):
                norm = l2norm(array([xc[i],yc[i],zc[i]])) - 1.0
                res.append(norm)

            return array(res)

        p0 = [x_offset, x_scale, y_offset, y_scale, z_offset, z_scale, 0.0, 0.0, 0.0]
        ls =  leastsq(residuals, p0, args=(xs,ys,zs))

        x_offset = ls[0][0]
        x_scale = ls[0][1]
        y_offset = ls[0][2]
        y_scale = ls[0][3]
        z_offset = ls[0][4]
        z_scale = ls[0][5]
        xy_scale = ls[0][6]
        xz_scale = ls[0][7]
        yz_scale = ls[0][8]

        print xy_scale, xz_scale, yz_scale

        cxs, cys, czs = self.applyCalibration(xs, ys, zs, x_o = x_offset, x_s = x_scale, y_o = y_offset, y_s = y_scale, z_o = z_offset, z_s = z_scale, xy_s = xy_scale, xz_s = xz_scale, yz_s = yz_scale)

        calibratedMag = empty((len(cxs),3))
        calibratedMag[:,0] = cxs
        calibratedMag[:,1] = cys
        calibratedMag[:,2] = czs

        magnitudes = amap(lambda v: l2norm(v), calibratedMag)

        self.calibratedMag = calibratedMag

        mlab.points3d(xs,ys,zs, scale_mode='none',scale_factor=10)
        mlab.show()
        mlab.clf()

        mlab.points3d(cxs,cys,czs, scale_mode='none', scale_factor=0.02)
        #mlab.points3d(array([-1.0,1.0]),array([0.0,0.0]),array([0.0,0.0]), scale_mode='none', scale_factor=0.02)
        sphere = mlab.points3d(0,0,0, opacity=0.5, resolution=100, color=(1.0,0.0,0.0), scale_mode='none', scale_factor=2.0)
        sphere.actor.property.backface_culling = True
        mlab.show()
        figure()
        plot(magnitudes)
        show()

        # write calibration to a file
        if self.write:
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
        print mean(resError) * 1000

    def calculateResidualError(self,xs,ys,zs):
        errors = []
        norm = l2norm(array([xs,ys,zs])) - 1.0
        errors.append(norm * norm)
        return mean(errors)

    def initialCalibration(self,readings):
        def offsetAndScale(min,max):
            offset = (max + min) / 2.0
            oMax = max - offset
            oMin = min - offset
            scale = 2.0 / (oMax - oMin)
            return offset,scale

        offset,scale = offsetAndScale(min(readings), max(readings))
        return offset, scale

    def applyCalibration(self,xs,ys,zs, x_o=0.0,x_s=1.0,y_o=0.0,y_s=1.0,z_o=0.0,z_s=1.0,xy_s=0.0,xz_s=0.0,yz_s=0.0):
        x = copy(xs)
        y = copy(ys)
        z = copy(zs)
        for i in range(len(xs)):
            xo = xs[i] - x_o
            yo = ys[i] - y_o
            zo = zs[i] - z_o
            x[i] = xo * (x_s + yo * xy_s + zo * xz_s)
            y[i] = yo * (y_s + zo * yz_s)
            z[i] = zo * z_s #(z_s + xo * xz_s + yo * yz_s)
        return x,y,z

if __name__ == '__main__':
    magcal = MagCalibration(4, offline=True, write=False)