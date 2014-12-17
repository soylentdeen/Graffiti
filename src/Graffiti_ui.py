# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Graffiti.ui'
#
# Created by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("Graffiti"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.BackgroundButton = QtGui.QPushButton(self.centralwidget)
        self.BackgroundButton.setGeometry(QtCore.QRect(40, 30, 121, 24))
        self.BackgroundButton.setObjectName(_fromUtf8("BackgroundButton"))
        self.Gain = QtGui.QLineEdit(self.centralwidget)
        self.Gain.setGeometry(QtCore.QRect(40, 80, 113, 20))
        self.Gain.setMaxLength(4)
        self.Gain.setProperty("Gain", 0.1)
        self.Gain.setObjectName(_fromUtf8("Gain"))
        self.SetGain = QtGui.QPushButton(self.centralwidget)
        self.SetGain.setGeometry(QtCore.QRect(170, 80, 75, 24))
        self.SetGain.setObjectName(_fromUtf8("SetGain"))
        self.TT_GainSelector = QtGui.QRadioButton(self.centralwidget)
        self.TT_GainSelector.setGeometry(QtCore.QRect(40, 110, 61, 20))
        self.TT_GainSelector.setObjectName(_fromUtf8("TT_GainSelector"))
        self.HO_GainSelector = QtGui.QRadioButton(self.centralwidget)
        self.HO_GainSelector.setGeometry(QtCore.QRect(100, 110, 61, 20))
        self.HO_GainSelector.setObjectName(_fromUtf8("HO_GainSelector"))
        self.Both_GainSelector = QtGui.QRadioButton(self.centralwidget)
        self.Both_GainSelector.setGeometry(QtCore.QRect(160, 110, 51, 20))
        self.Both_GainSelector.setObjectName(_fromUtf8("Both_GainSelector"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Graffiti", None))
        self.BackgroundButton.setText(_translate("MainWindow", "Take Background", None))
        self.Gain.setToolTip(_translate("MainWindow", "Gain", None))
        self.SetGain.setText(_translate("MainWindow", "Set Gain", None))
        self.TT_GainSelector.setText(_translate("MainWindow", "Tip/Tilt", None))
        self.HO_GainSelector.setText(_translate("MainWindow", "HODM", None))
        self.Both_GainSelector.setText(_translate("MainWindow", "Both", None))

