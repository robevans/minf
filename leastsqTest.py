__author__ = 'Rat'

from scipy.optimize import leastsq
from pylab import array, copy

def residuals(params, actual):
    print "params: " + str(params)
    print "actual: " + str(actual)
    print "expected: " + str(exp)
    result =  actual * params[0] / exp - 1.0
    print "result: " + str(result)
    return result


p0 = [0.6,0.6]

act = array([1.0,2.0,3.0,4.0])
exp = copy(act)
act *= 2.0
#print actual


result = leastsq(residuals, p0, args=(act))
