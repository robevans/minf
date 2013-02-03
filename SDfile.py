import struct
import sys

f = open(sys.argv[1], 'rb')
line = f.read(11)
counts = { 0: 0, 1: 0, 2: 0}
lasttime = { 0: 0, 1: 0, 2: 0}
timediffs = { 0: [], 1: [], 2: []}
while line:
    (header, packetid, nodeid, time) = struct.unpack(">cBBHhhh", line)
    if packetid == 0:
        (x, y, z) = struct.unpack("<hhh", line[5:])
    if (time < lasttime[packetid]):
        lasttime[packetid] -= 48000
    timediff = time - lasttime[packetid]
    print "PID: %i, NID: %i, Count: %6i, Time: %5i, TimeDiff: %5i, X: %5i, Y: %5i, Z: %5i"%(packetid, nodeid, counts[packetid], time, timediff, x, y, z)
    timediffs[packetid].append(timediff)
    lasttime[packetid] = time
    counts[packetid] += 1
    line = f.read(11)
print "0: gyro, 1: accel, 2: mag"
for key in counts.keys():
    print "%i: Count: %6i, minTimeDiff: %5i, maxTimeDiff: %5i, avgTimeDiff: %4.2f"%(key, counts[key], min(timediffs[key][3:]), max(timediffs[key][3:]), float(sum(timediffs[key][3:])) / float(len(timediffs[key][3:])))
