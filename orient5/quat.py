from __future__ import division
from scipy import asarray,array,matrix,sqrt,arcsin,arccos,arctan2
from scipy import cos,sin,degrees,radians,pi,empty,nan

EPS = 0.0001

vectorLength = lambda v: sqrt(sum([a**2 for a in v]))
vectorNormalise = lambda v: v/vectorLength(v)

def matrixToEuler(m,order='Aerospace',inDegrees=True):
    if order == 'Aerospace' or order == 'ZYX':
        sp = -m[2,0]
        if sp < (1-EPS):
            if sp > (-1+EPS):
                p = arcsin(sp)
                r = arctan2(m[2,1],m[2,2])
                y = arctan2(m[1,0],m[0,0])
            else:
                p = -pi/2.
                r = 0
                y = pi-arctan2(-m[0,1],m[0,2])
        else:
            p = pi/2.
            y = arctan2(-m[0,1],m[0,2])
            r = 0
        
        if inDegrees:
            return degrees((y,p,r))
        else:
            return (y,p,r)
    elif order == 'BVH' or order == 'ZXY':
        sx = m[2,1]
        if sx < (1-EPS):
            if sx > (-1+EPS):
                x = arcsin(sx)
                z = arctan2(-m[0,1],m[1,1])
                y = arctan2(-m[2,0],m[2,2])
            else:
                x = -pi/2
                y = 0
                z = -arctan2(m[0,2],m[0,0])
        else:
            x = pi/2
            y = 0
            z = arctan2(m[0,2],m[0,0])
        if inDegrees:
            return degrees((z,x,y))
        else:
            return (z,x,y)

    elif order == "ZXZ":
        x = arccos(m[2,2])
        z2 = arctan2(m[2,0],m[2,1])
        z1 = arctan2(m[0,2],-m[1,2])
        if inDegrees:
            return degrees((z1,x,z2))
        else:
            return (z1,x,z2)

class Quat:
    def __init__(self,w=1,x=0,y=0,z=0):
        try:
            w,x,y,z = w
        except: pass
        self.w = w 
        self.x = x
        self.y = y
        self.z = z

    @property
    def values(self):
        return (self.w,self.x,self.y,self.z)

    def __iter__(self):
        return (f for f in (self.w,self.x,self.y,self.z))

    def __add__(self, q):
        return Quat(self.w+q.w,self.x+q.x,self.y+q.y, self.z+q.z)

    def __iadd__(self,q):
        self.w+=q.w
        self.x+=q.x
        self.y+=q.y
        self.z+=q.z
        return self

    def __neg__(self):
        return Quat(-self.w,-self.x,-self.y,-self.z)

    def __isub__(self,q):
        self.w-=q.w
        self.x-=q.x
        self.y-=q.y
        self.z-=q.z
        return self

    def __sub__(self,q):
        return Quat(self.w-q.w,self.x-q.x,self.y-q.y,self.z-q.z)


    def __mul__(self, q):
        tmp = Quat()
        if isinstance(q,Quat):
            tmp.w = self.w*q.w - self.x*q.x - self.y*q.y - self.z*q.z
            tmp.x = self.w*q.x + self.x*q.w + self.y*q.z - self.z*q.y
            tmp.y = self.w*q.y - self.x*q.z + self.y*q.w + self.z*q.x
            tmp.z = self.w*q.z + self.x*q.y - self.y*q.x + self.z*q.w
        else:
            tmp.w = self.w*q
            tmp.x = self.x*q
            tmp.y = self.y*q
            tmp.z = self.z*q
        return tmp
        
    def __rmul__(self,scalar):
        return Quat(self.w*scalar,self.x*scalar,self.y*scalar,self.z*scalar)

    @staticmethod
    def errorAngle(actual,estimate):        
        error = actual*estimate.conjugate()
        error.normalise()
        # Cast error to float so that we can deal with fixed point numbers
        # throws an error otherwise
        eAngle = degrees(2*arccos(float(error.w)))
        
        eAngle = abs(eAngle - 360) if eAngle > 180 else eAngle
        return eAngle
        
    def copy(self):
        """Return a copy of this quaternion"""
        return Quat(self.w,self.x,self.y,self.z,)
        
    def __str__(self):
        return self.__repr__()

    def asMatrix(self):
        m = matrix([[0,0,0],[0,0,0],[0,0,0]],dtype=float)
        m[0,0] = 1. - 2.*self.y**2 - 2.*self.z**2
        m[1,0] = 2. * (self.x*self.y + self.w*self.z)
        m[2,0] = 2. * (self.x*self.z - self.w*self.y)

        m[0,1] = 2. * (self.x*self.y - self.w*self.z)
        m[1,1] = 1. - 2.*self.x**2 - 2. *self.z**2
        m[2,1] = 2. * (self.y*self.z + self.w*self.x)

        m[0,2] = 2. * (self.x*self.z + self.w*self.y)
        m[1,2] = 2. * (self.y*self.z - self.w*self.x)
        m[2,2] = 1. - 2.*self.x**2 - 2.*self.y**2

        return m

    def asAxisAndAngle(self):
        axis = array([nan,nan,nan])
        angle = 2*arccos(self.w)
        if angle != 0:
            s = sqrt(1 - self.w**2)
            axis[0] = self.x / s
            axis[1] = self.y / s
            axis[2] = self.z / s

        return axis, angle

    def setFromMatrix(self,m):
        t = m[0,0]+m[1,1]+m[2,2]
        if t > 0:
            w2 = sqrt(t+1)
            self.w = w2/2
            self.x = (m[2,1]-m[1,2])/(2*w2)
            self.y = (m[0,2]-m[2,0])/(2*w2)
            self.z = (m[1,0]-m[0,1])/(2*w2)
        else:
            t = m[0,0]-m[1,1]-m[2,2]
            if t > 0:
                x2 = sqrt(t+1)
                self.w = (m[2,1]-m[1,2])/(2*x2)
                self.x = x2/2
                self.y = (m[1,0]+m[0,1])/(2*x2)
                self.z = (m[0,2]+m[2,0])/(2*x2)
            else:
                t = m[1,1]-m[0,0]-m[2,2]
                if t > 0:
                    y2 = sqrt(t+1)
                    self.w = (m[0,2]-m[2,0])/(2*y2)
                    self.x = (m[1,0]+m[0,1])/(2*y2)
                    self.y = y2/2
                    self.z = (m[1,2]+m[2,1])/(2*y2)
                else:
                    z2 = sqrt(m[2,2]-m[0,0]-m[1,1]+1)
                    self.w = (m[1,0]-m[0,1])/(2*z2)
                    self.x = (m[0,2]+m[2,0])/(2*z2)
                    self.y = (m[1,2]+m[2,1])/(2*z2)
                    self.z = z2/2

        return self

    def setFromVectors(self,x,y,z):
        self.setFromMatrix(asarray([x,y,z]))
        return self

    def toEuler(self, order='Aerospace',degrees=True):
        '''
        Convert this quaternion to a corresponding Euler angle sequence.
        
        Keyword args:
        order - the rotation order used for the conversion. Choices are:
            'ZYX' or 'Aerospace' for standard aerospace order
            'ZXY' of 'BVH' for the order used in BVH animation files
        '''
        m = self.asMatrix()
        return matrixToEuler(m,order,degrees)
    
    def toAerospace(self):
        '''
        Convert this quaternion to the corresponding aerospace Euler angle sequence.
        
        Returns:
        a tuple containing the roll,pitch and yaw angles
        '''
        return self.toEuler('Aerospace')[::-1]

    def length(self):
        return sqrt(self.w**2+self.x**2+self.y**2+self.z**2)
        
    def normalise(self):
        scale = 1/self.length()
        self.w*=scale
        self.x*=scale
        self.y*=scale
        self.z*=scale
        return self

    def negate(self):
        self.w*=-1 
        self.x*=-1
        self.y*=-1
        self.z*=-1

    def conjugate(self):
        return Quat(self.w,-self.x,-self.y,-self.z,)

    def rotateVector(self,v):
        '''
        Return the vector v as it would appear in the current co-ordinate frame 
        when rotated by the rotation specified by this quaternion.
        '''
        r = empty(3)
        W = -self.x * v[0] - self.y * v[1] - self.z * v[2];
        X = self.w * v[0] + self.y * v[2] - self.z * v[1];
        Y = self.w * v[1] - self.x * v[2] + self.z * v[0];
        Z = self.w * v[2] + self.x * v[1] - self.y * v[0];

        r[2] = -W * self.z - X * self.y + Y * self.x + Z * self.w;
        r[1] = -W * self.y + X * self.z + Y * self.w - Z * self.x;
        r[0] = -W * self.x + X * self.w - Y * self.z + Z * self.y;
        return r
    
    def rotateFrame(self,v):
        '''
        Return the vector v as it would appear in the rotated frame specified 
        by this quaternion.
        '''
        r = empty(3)
        W = self.x * v[0] + self.y * v[1] + self.z * v[2]
        X = self.w * v[0] - self.y * v[2] + self.z * v[1]
        Y = self.w * v[1] + self.x * v[2] - self.z * v[0]
        Z = self.w * v[2] - self.x * v[1] + self.y * v[0]

        r[2] = W * self.z + X * self.y - Y * self.x + Z * self.w
        r[1] = W * self.y - X * self.z + Y * self.w + Z * self.x
        r[0] = W * self.x + X * self.w + Y * self.z - Z * self.y
        return r
        
    
    def __repr__(self):
        return str((self.w,self.x,self.y,self.z))


    def set(self,o):
        self.w = o.w
        self.x = o.x
        self.y = o.y
        self.z = o.z
        
    def setComponents(self, c):
        self.w = c[0]
        self.x = c[1]
        self.y = c[2]
        self.z = c[3]
        return self

    def setFromAerospace(self,roll,pitch,yaw,degrees=True):
        '''
        Set this quaternion from the specified roll,pitch and yaw angles
        
        Keyword args:
        degrees - set True to indicate angles are in degrees, False for radians
        '''
        self.setFromEuler((yaw,pitch,roll), order='Aerospace', degrees=degrees)
        return self

    def setFromEuler(self,angles,order='Aerospace',degrees=True):
        '''
        Set this quaternion from the Euler angle sequence angle
        
        Keyword args:
        order - the order used to apply the Euler angle sequence. Choices are:
            'Aerospace' or 'ZYX' for standard aerospace sequence (default)
            'BVH' of 'ZXY' for order used in BVH files
            'ZXZ' for ZXZ order
        degrees - set True to indicate that angles are in degrees (default) or
            false for radians
        '''
        angles = asarray(angles)/2
        if degrees:
            angles = radians(angles)
        if order == 'Aerospace' or order == 'ZYX':
            self.set(Quat(cos(angles[0]),0,0,sin(angles[0])) *
                     Quat(cos(angles[1]),0,sin(angles[1]),0) *
                     Quat(cos(angles[2]),sin(angles[2]),0,0))
        elif order == 'BVH' or order == 'ZXY':
            self.set(Quat(cos(angles[0]),0,0,sin(angles[0])) *
                     Quat(cos(angles[1]),sin(angles[1]),0,0) *
                     Quat(cos(angles[2]),0,sin(angles[2]),0))
        elif order == 'ZXZ':
            self.set(Quat(cos(angles[0]),0,0,sin(angles[0])) *
                     Quat(cos(angles[1]),sin(angles[1]),0,0) *
                     Quat(cos(angles[2]),0,0,sin(angles[2])))
        else:
            raise RuntimeError("Unknown rotation order: %s"%order)

        return self

