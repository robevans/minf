# Run this script to enable interactivity for RPY2 graphics windows
# Terminates if all windows are closed.

__author__ = 'Robert Evans'

from threading import Thread
from rpy2.robjects import r
from rpy2 import rinterface
import time

def enableInteractivity():
	while(r.length(r('dev.list()'))[0]>0):
		rinterface.process_revents()
		time.sleep(0.1)