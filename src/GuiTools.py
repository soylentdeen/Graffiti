import scipy
import numpy
import matplotlib.pyplot as pyplot
import sys
import platform
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as Navigationtoolbar
from matplotlib.figure import Figure

import matplotlib

class DM_Map( object ):
    def __init__(self, npix):
        self.npix = npix
        self.r1 = npix/10.0
        self.r2 = npix/5.0
        self.r3 = 3.0*npix/10.0
        self.r4 = 4.0*npix/10.0
        self.r5 = npix/2.0

    def ring1(self, x, y):
        return (x**2.0 + y**2.0)**(0.5) < self.r1

    def ring2(self, x, y):
        return (x**2.0 + y**2.0)**(0.5) < self.r2

    def ring3(self, x, y):
        return (x**2.0 + y**2.0)**(0.5) < self.r3

    def ring4(self, x, y):
        return (x**2.0 + y**2.0)**(0.5) < self.r4

    def ring5(self, x, y):
        return (x**2.0 + y**2.0)**(0.5) < self.r5

    def measureAngle(self, x, y):
        return numpy.rad2deg(numpy.arctan2(y,x))


class Actuator( object ):
    def __init__(self, number, ring, angle_start, 
            angle_stop, DM_map = None, value=0.0):
        self.number = number
        self.ring = ring
        self.angle_start = angle_start
        self.angle_stop = angle_stop
        self.value = value
        self.DM_map = DM_map
        self.pixels = []

    def included(self, x, y, angle):
        if (self.angle_start <= angle) and (self.angle_stop >= angle):
            pass
        else:
            return False
        if self.ring == 1:
            if self.DM_map.ring1(x, y):
                pass
            else:
                return False
        elif self.ring == 2:
            if (self.DM_map.ring2(x, y) and not(self.DM_map.ring1(x, y))):
                pass
            else:
                return False
        elif self.ring == 3:
            if (self.DM_map.ring3(x, y) and not(self.DM_map.ring2(x, y))):
                pass
            else:
                return False
        elif self.ring == 4:
            if (self.DM_map.ring4(x, y) and not(self.DM_map.ring3(x, y))):
                pass
            else:
                return False
        else:
            if (self.DM_map.ring5(x, y) and not(self.DM_map.ring4(x, y))):
                pass
            else:
                return False

        return True

    def addPixel(self, x, y):
        self.pixels.append([x, y])

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def calcTextAnchors(self):
        self.pixels = numpy.array(self.pixels)
        self.xTextAnchor = numpy.average(self.pixels[:,0])
        self.yTextAnchor = numpy.average(self.pixels[:,1])
