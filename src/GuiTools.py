import scipy
import numpy
import matplotlib.pyplot as pyplot
import sys
import platform
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as Navigationtoolbar
from matplotlib.figure import Figure

import matplotlib

#Embeddable matplotlib figure/canvas
class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.axes = self.fig.add_axes([0.0, 0.0, 1.0, 1.0])
        self.axes.set_xticklabels([])
        self.axes.set_yticklabels([])

        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

#creates embeddable matplotlib figure/canvas with toolbar
class MatplotlibWidget(QtGui.QWidget):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.create_framentoolbar()

    def create_framentoolbar(self):
        self.frame = QWidget()
        self.canvas = MplCanvas()
        self.canvas.setParent(self.frame)
        self.canvas.axes.set_xticklabels([])
        self.canvas.axes.set_yticklabels([])
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)


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

    def quad2(self, x, y):
        return (x < 0.0) and (y > 0.0)

    def quad4(self, x, y):
        return (x > 0.0) and (y < 0.0)

class Actuator( object ):
    def __init__(self, number, ring, angle_start, 
            angle_stop, parent = None, value=0.0, Tip=False, Tilt=False):
        self.number = number
        self.ring = ring
        self.angle_start = angle_start
        self.angle_stop = angle_stop
        self.value = value
        self.parent = parent
        self.pixels = []
        self.Tip = Tip
        self.Tilt = Tilt

    def __str__(self):
        if self.Tip:
            return "Tip"
        if self.Tilt:
            return "Tilt"
        return str(self.number)

    def __lt__(self, other):
        return self.number < other.number

    def __le__(self, other):
        return self.number <= other.number

    def __gt__(self, other):
        return self.number > other.number

    def __ge__(self, other):
        return self.number >= other.number

    def __eq__(self, other):
        return self.number == other.number

    def __ne__(self, other):
        return self.number != other.number

    def included(self, x, y, angle):
        if self.Tip:
            return (self.parent.DM_Map.quad2(x, y) and not(self.parent.DM_Map.ring5(x, y)))
        if self.Tilt:
            return (self.parent.DM_Map.quad4(x, y) and not(self.parent.DM_Map.ring5(x, y)))

        if (self.angle_start <= angle) and (self.angle_stop >= angle):
            pass
        else:
            return False
        if self.ring == 1:
            if self.parent.DM_Map.ring1(x, y):
                pass
            else:
                return False
        elif self.ring == 2:
            if (self.parent.DM_Map.ring2(x, y) and not(self.parent.DM_Map.ring1(x, y))):
                pass
            else:
                return False
        elif self.ring == 3:
            if (self.parent.DM_Map.ring3(x, y) and not(self.parent.DM_Map.ring2(x, y))):
                pass
            else:
                return False
        elif self.ring == 4:
            if (self.parent.DM_Map.ring4(x, y) and not(self.parent.DM_Map.ring3(x, y))):
                pass
            else:
                return False
        else:
            if (self.parent.DM_Map.ring5(x, y) and not(self.parent.DM_Map.ring4(x, y))):
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


class DM_Gui( object ):
    def __init__(self, aortc):
        self.nact = 60
        self.npix = 300
        self.nact_r1 = 4
        self.nact_r2 = 8
        self.nact_r3 = 12
        self.nact_r4 = 16
        self.nact_r5 = 20
        
        self.aortc = aortc

        self.DM_Map = DM_Map(self.npix)
        self.HOactuators = []
        self.TTactuators = []
        self.pixels = numpy.zeros((self.npix, self.npix), dtype='float32')

        self.populateActuators()
        self.assignPixels()
        self.getCurrentActRefPos()

    def populateActuators(self, HOdata = None, TTdata = None):
        nring = 1
        act_num = 0
        for nact in [self.nact_r1, self.nact_r2, self.nact_r3, 
                self.nact_r4, self.nact_r5]:
            for i in range(nact):
                angle_start = 360.0/nact * i
                angle_stop = 360.0/nact * (i+1)
                if angle_start >= 180.0:
                    angle_start -= 360.0
                if angle_stop > 180.0:
                    angle_stop -= 360.0

                if HOdata:
                    self.HOactuators.append(Actuator(act_num, nring, 
                        angle_start, angle_stop, parent = self,
                        value = HOdata[act_num], Tip = False, Tilt = False))
                else:
                    self.HOactuators.append(Actuator(act_num, nring,
                        angle_start, angle_stop, parent = self,
                        value = act_num, Tip = False, Tilt = False))
                act_num += 1
            nring += 1
        if TTdata:
            self.TTactuators.append(Actuator(act_num, 0, 0.0, 0.0, parent=self,
                value = TTdata[0], Tip = True, Tilt = False))
            act_num += 1
            self.TTactuators.append(Actuator(act_num, 0, 0.0, 0.0, parent=self,
                value = TTdata[1], Tip = False, Tilt = Tip))
            act_num += 1
        else:
            self.TTactuators.append(Actuator(act_num, 0, 0.0, 0.0, parent=self,
                value = 0.0, Tip = True, Tilt = False))
            act_num += 1
            self.TTactuators.append(Actuator(act_num, 0, 0.0, 0.0, parent=self,
                value = 0.0, Tip = False, Tilt = True))
            act_num += 1

    def assignPixels(self):
        for x in range(self.npix):
            xpix = x-self.npix/2.0
            for y in range(self.npix):
                ypix = y - self.npix/2.0
                angle = numpy.rad2deg(numpy.arctan2(ypix, xpix))
                for act in self.HOactuators+self.TTactuators:
                    if act.included(xpix, ypix, angle):
                        act.addPixel(x, y)
                        self.pixels[x][y] = act.getValue()
        for act in self.HOactuators+self.TTactuators:
            act.calcTextAnchors()

    def getCurrentActRefPos(self):
        HO = self.aortc.get_HO_ACT_POS_REF_MAP()
        TT = self.aortc.get_TT_ACT_POS_REF_MAP()
        for act, dat in zip(self.HOactuators+self.TTactuators, 
                numpy.append(HO[0],TT[0])):
            act.setValue(dat)
            pix = act.pixels
            print act.number, dat
            self.pixels[pix[:,0],pix[:,1]] = dat

