#!/usr/bin/python

inputFile = "balletCapture.csv"
h = ["id","gyroTimestamps","accelTimestamps","magTimestamps","gyroX","gyroY","gyroZ","accelX","accelY","accelZ","magX","magY","magZ"]

def rowIsForSensor(row, sensorID):
    try:
        if float(row.split(',')[0]) == sensorID:
            return True
        return False
    except ValueError:
        return False

def project(row, columns):
    """ Takes a row of comma separated values and a list of column numbers,
    returns those columns from the row. """
    row = row.split(',')
    output = []
    for c in columns:
        if c < len(row):
            output = output + [row[c]];
    return output

def listToCSVrow(list):
    output = ""
    for item in list:
        output = output + item + ","
    return output[:-1]

f = open(inputFile)
i = 0
for row in f:
    i += 1
    if i==1: h = row.split(',')
    if rowIsForSensor(row,20):
        projectedRow = project(row, [h.index("gyroY")])
        print listToCSVrow(projectedRow)