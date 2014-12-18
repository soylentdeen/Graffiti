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
        self.axes = self.fig.add_subplot(111)

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

class Actuator( object ):
    def __init__(self, number, ring, angle_start, 
            angle_stop, parent = None, value=0.0):
        self.number = number
        self.ring = ring
        self.angle_start = angle_start
        self.angle_stop = angle_stop
        self.value = value
        self.parent = parent
        self.pixels = []

    def included(self, x, y, angle):
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
    def __init__(self, mplWindow):
        self.nact = 60
        self.npix = 100
        self.nact_r1 = 4
        self.nact_r2 = 8
        self.nact_r3 = 12
        self.nact_r4 = 16
        self.nact_r5 = 20

        self.DM_Map = DM_Map(self.npix)
        self.actuators = []
        self.mplWindow = mplWindow
        self.pixels = numpy.zeros((self.npix, self.npix), dtype='float32')

        self.populateActuators()
        self.assignPixels()
        #self.drawMap()

    def populateActuators(self, data=None):
        nring = 1
        act_num = 0
        for nact in [self.nact_r1, self.nact_r2, self.nact_r3, self.nact_r4, self.nact_r5]:
            for i in range(nact):
                angle_start = 360.0/nact * i
                angle_stop = 360.0/nact * (i+1)
                if angle_start >= 180.0:
                    angle_start -= 360.0
                if angle_stop > 180.0:
                    angle_stop -= 360.0

                if data:
                    self.actuators.append(Actuator(act_num, nring, angle_start,
                        angle_stop, parent=self, value=data[act_num]))
                else:
                    self.actuators.append(Actuator(act_num, nring, angle_start,
                        angle_stop, parent=self, value=act_num))
                act_num += 1
            nring += 1

    def assignPixels(self):
        for x in range(self.npix):
            xpix = x-self.npix/2.0
            for y in range(self.npix):
                ypix = y - self.npix/2.0
                angle = numpy.rad2deg(numpy.arctan2(ypix, xpix))
                for act in self.actuators:
                    if act.included(xpix, ypix, angle):
                        act.addPixel(x, y)
                        self.pixels[x][y] = act.getValue()

    def drawMap(self):
        exec("wp.ui.DMPlotWindow.canvas.axes.clear()")
        exec("wp.ui.DMPlotWindow.canvas.axes.matshow(self.pixels.transpose(), aspect='auto', origin='lower')")
        exec("wp.ui.DMPlotWindow.canvas.draw()")
