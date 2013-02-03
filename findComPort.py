__author__ = 'Andrew'

from os import popen

def findComPort():
    s = popen("listComPorts").read()

    lines = s.split("\n")
    #print lines

    for l in lines:
        if "Energy Micro" in l:
            return l.split(" - ")[0]

    print "Basestation not found"
    return None

if __name__ == '__main__':
    print findComPort()