
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This is the main file for launching the PyQt app.

Requirements:
You need Python 2 (+ matplotlib, pylab and pyfits modules), Qt4 and PyQt for this to work


Description:
- Graffiti.py is this Python file, must be executable.
Launch the GUI using the command (in terminal):
  > python -i Graffiti.py

- demo.ui is an XML file, modifiable/editable in a friendly user manner with - Qt Designer or Qt creator (comes with Qt installation).
- demo_ui.py is the PyQt Python file, generated with the terminal command :
  > pyuic4 demo.ui -o demo_ui.py (pyuic4 comes with PyQt package)
  This command has to be typed each time the GUI is modified in order to take into account the changes in PyQt (this program).
  Note: Once generated DO NOT EDIT the demo_ui.py file. Only PyQtDemo.py (this file) can be edited safely.
  
"""



import sys# This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available.
sys.path.insert(0, './lib') #Add in this python session lib path
import os # enable shell commands in python. See also http://www.pythonforbeginners.com/os/pythons-os-module
#try:
import pyfits # See also http://www.stsci.edu/institute/software_hardware/pyfits
#except:
#    from astropy.io import fits as pyfits #https://astropy.readthedocs.org/en/v0.3/io/fits/index.html
from matplotlib.pylab import * #Usefull library for plotting stuff (pylab)
from matplotlib.mlab import * #Usefull library for plotting stuff
#from libfits import * #usefull stuff for reading fits 


# Qt4 libraries
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

# From the "automatically generated" demo_ui.py file (see above) it imports the "Ui_demo_qt" class that defines everything that was created in the Qt GUI file (demo.ui). Do NOT change anything in the demo_ui file. If you want to change something in the GUI, use Qt designer to edit the demo.ui file and re-run the command: "pyuic4 demo.ui -o demo_ui.py" again.
# Note: The "Ui_demo_qt" name was choosen from the name the user put in the QMainWindow (see demo.ui) in which the pyuic4 command added Ui_ suffix.
from Graffiti_ui import Ui_MainWindow #Required

import pdb # Enter in the debug mode by placing :  pdb.set_trace() in your program. Note ipython enables it automatically by entering %pdb
# See also debug mode explanation here:
# http://www.fevrierdorian.com/blog/post/2009/11/04/Un-debugger-dans-Python-pour-voir-pr%C3%A9cis%C3%A9ment-ce-qui-ce-passe-dans-son-code            
            
import VLTTools # Object created for talking to the VLT Tools - Added by C.Deen on 15 Dec 2014
import GuiTools # GUI objects - Added by C. Deen on 16 Dec 2014



"""
 __  __       _          ____ _   _ ___        _               
|  \/  | __ _(_)_ __    / ___| | | |_ _|   ___| | __ _ ___ ___ 
| |\/| |/ _` | | '_ \  | |  _| | | || |   / __| |/ _` / __/ __|
| |  | | (_| | | | | | | |_| | |_| || |  | (__| | (_| \__ \__ \
|_|  |_|\__,_|_|_| |_|  \____|\___/|___|  \___|_|\__,_|___/___/
                                                               
"""

class Graffiti_ui_class( QtGui.QMainWindow ):
    #=========================================================================================
    #          Here we define the class of the main Ui we will manipulate in python.
    #=========================================================================================
    def __init__( self, parent=None, aortc=None ): # This is what happens when an object of this class is called. It's a kind of init.
        QtGui.QWidget.__init__( self, parent )
        self.aortc = aortc   # aortc is the VLT Connection to the work station
        self.ui = Ui_MainWindow() #ui. is the GUI
        self.ui.setupUi( self ) # Just do it
        
        self.SelectedGain = 0

        QtCore.QObject.connect( self.ui.BackgroundButton, QtCore.SIGNAL("clicked()"), self.measureBackground)  # Connects the "Take Background" button with the correct plumbing

        self.ui.GainSelectorGroup = QButtonGroup()
        self.ui.GainSelectorGroup.addButton(self.ui.Both_GainSelector)   # How do I set this to default?
        self.ui.GainSelectorGroup.addButton(self.ui.TT_GainSelector)
        self.ui.GainSelectorGroup.addButton(self.ui.HO_GainSelector)
        
        QtCore.QObject.connect(self.ui.Both_GainSelector, QtCore.SIGNAL("clicked()"), self.gainSelector)
        QtCore.QObject.connect(self.ui.TT_GainSelector, QtCore.SIGNAL("clicked()"), self.gainSelector)
        QtCore.QObject.connect(self.ui.HO_GainSelector, QtCore.SIGNAL("clicked()"), self.gainSelector)
        QtCore.QObject.connect( self.ui.SetGain, QtCore.SIGNAL("clicked()"), self.setGain)  # Connects the "Take Background" button with the correct plumbing

        self.DM_Gui = GuiTools.DM_Gui(self.ui.DMPlotWindow)


        """
        #Initialize attributes of the GUI
        self.ui.nbPushed = 0 # nb of times the push button was pushed
        self.ui.twoStateButtonStatus = "released" #Current state of 2 state button
        self.ui.nbItemsComboBox = 0 # Current number of items in the combo box
        
        # We group the 4 radio buttons so that when one is checked all the others are unchecked automaticallly
        #self.ui.group = QButtonGroup()
        #self.ui.group.addButton(self.ui.radioButton_1)
        #self.ui.group.addButton(self.ui.radioButton_2)
        #self.ui.group.addButton(self.ui.radioButton_3)
        #self.ui.group.addButton(self.ui.radioButton_4)
        
        
        #We connect objects with the proper signal to interact with them...
        QtCore.QObject.connect( self.ui.loadfitsButton,  QtCore.SIGNAL("clicked()"), self.selectFITS ) #Connects "loadfitsButton" button to the "selectFITS" method
        self.ui.twoStateButton.setCheckable(True)     
        self.ui.twoStateButton.clicked[bool].connect(self.twoStateButtonIsPushed) # We define the 2 state buttons here... 
        QtCore.QObject.connect( self.ui.pushButton,  QtCore.SIGNAL("clicked()"), self.theButtonIsPushed ) #Connects "pushButton" to the "theButtonIsPushed" method
        QtCore.QObject.connect( self.ui.plotRandom,  QtCore.SIGNAL("clicked()"), self.theButtonPlotRandomIsPushed ) #Connects "plotRandom" to the "theButtonPlotRandomIsPushed" method
        QtCore.QObject.connect( self.ui.okButton,  QtCore.SIGNAL("clicked()"), self.theButtonOKIsClicked ) #Connects "OK" button to the "theButtonOKIsClicked" method
        QtCore.QObject.connect( self.ui.resetCombobox,  QtCore.SIGNAL("clicked()"), self.resetComboboxClicked ) #Connects "OK" button to the "theButtonOKIsClicked" method

        #We connect here all the radiobutton to the "radioButtonWasClicked" method 
        QtCore.QObject.connect( self.ui.radioButton_1,  QtCore.SIGNAL("clicked()"), self.radioButtonWasClicked ) 
        QtCore.QObject.connect( self.ui.radioButton_2,  QtCore.SIGNAL("clicked()"), self.radioButtonWasClicked ) 
        QtCore.QObject.connect( self.ui.radioButton_3,  QtCore.SIGNAL("clicked()"), self.radioButtonWasClicked ) 
        QtCore.QObject.connect( self.ui.radioButton_4,  QtCore.SIGNAL("clicked()"), self.radioButtonWasClicked ) 

        #Connects the signal when the combobox is changed
        QtCore.QObject.connect(self.ui.ComboBox, QtCore.SIGNAL("currentIndexChanged(QString)"), self.getComboBox)

        #End of GUI Class initialization

        #"""

    def initialize(self):
        #print "Hi"
        updateDMPos()
        
            
    def measureBackground(self):
        print "Let's measure a background!"
        self.aortc.changePixelTapPoint("RAW")
        self.aortc.updateAcq()
        self.aortc.measureBackground(10)
        self.aortc.changePixelTapPoint("CALIB")
        self.aortc.updateAcq()

    def gainSelector(self):
        if(self.ui.Both_GainSelector.isChecked()):
            self.SelectedGain = 0
        elif(self.ui.TT_GainSelector.isChecked()):
            self.SelectedGain = 1
        elif(self.ui.HO_GainSelector.isChecked()):
            self.SelectedGain = 2


    def setGain(self):
        try:
            gain = self.ui.Gain.text().toFloat()[0]
            if (gain < 1.0) & (gain > 0.0):
                if self.SelectedGain == 0:
                    self.aortc.set_TT_gain(-gain)
                    self.aortc.set_HO_gain(-gain)
                elif self.SelectedGain == 1:
                    self.aortc.set_TT_gain(-gain)
                elif self.SelectedGain == 2:
                    self.aortc.set_HO_gain(-gain)
                else:
                    print("How in the world did I get here?")
            else:
                print("Error! Gain must be between 1.0 and 0.0!!")
        except:
            print("Error!  Parsing error!")

        """
                         _     ____        _   _              
         _ __  _   _ ___| |__ | __ ) _   _| |_| |_ ___  _ __  
        | '_ \| | | / __| '_ \|  _ \| | | | __| __/ _ \| '_ \ 
        | |_) | |_| \__ \ | | | |_) | |_| | |_| || (_) | | | |
        | .__/ \__,_|___/_| |_|____/ \__,_|\__|\__\___/|_| |_|
        |_|                                                   

        """
        
    def theButtonIsPushed(self):
    #=========================================================================================
    #          This method is called when the push button is clicked
    #=========================================================================================
        self.ui.nbPushed+=1
        mess = "This button has been pushed %d time(s)" % self.ui.nbPushed
        print mess
        self.ui.dialogBox.setText(mess) #Shows the message in the GUI dialogbox        
                
        
    def theButtonPlotRandomIsPushed(self):
    #=========================================================================================
    #          This method is called when the plot random image in window # is clicked
    #=========================================================================================
        winnum = self.ui.winNumber.value() # Retrieves the desired window number
        pliInGui(np.random.rand(256,256), win=winnum) # Displays random array in the desired matplotlib embedded window


        """
                       _ _       ____        _   _              
         _ __ __ _  __| (_) ___ | __ ) _   _| |_| |_ ___  _ __  
        | '__/ _` |/ _` | |/ _ \|  _ \| | | | __| __/ _ \| '_ \ 
        | | | (_| | (_| | | (_) | |_) | |_| | |_| || (_) | | | |
        |_|  \__,_|\__,_|_|\___/|____/ \__,_|\__|\__\___/|_| |_|
                                                                
                
        """
    def radioButtonWasClicked(self):
    #==============================================================================
    #         This method is Called when one of the radiobuttons are clicked
    #==============================================================================
        if(self.ui.radioButton_1.isChecked()):
            mess = "No!   God outstands. Eric does not count."
        elif(self.ui.radioButton_2.isChecked()):
            mess= "No!    Even a master Jedi is not as good as him!"
        elif(self.ui.radioButton_3.isChecked()):
            mess= "Almost....    Fab is second in the list (will be 1st soon ;-) )"
        elif(self.ui.radioButton_4.isChecked()):
            mess= "Yes!   Zozo = The best   ;-)"
        else:
            mess="Oups I shoudn't be there..."
        self.ui.dialogBox.setText(mess) #Shows the message in the GUI dialogbox        
   
            
            
        """ 
         ____      _        _       ____        _   _              
        |___ \ ___| |_ __ _| |_ ___| __ ) _   _| |_| |_ ___  _ __  
          __) / __| __/ _` | __/ _ \  _ \| | | | __| __/ _ \| '_ \ 
         / __/\__ \ || (_| | ||  __/ |_) | |_| | |_| || (_) | | | |
        |_____|___/\__\__,_|\__\___|____/ \__,_|\__|\__\___/|_| |_|
                                                                   
        
        """
    def twoStateButtonIsPushed(self, pressed):
    #==============================================================================
    #         This method is Called when the 2 state button is clicked
    #==============================================================================
        if(pressed):
            self.ui.twoStateButtonStatus = "pushed" #if pressed we set the twoStateButtonStatus attribute to pushed
        else:
            self.ui.twoStateButtonStatus = "released" #if pressed we set the twoStateButtonStatus attribute to released
        self.ui.twoStateButton.setText("2 state Button (%s)" % self.ui.twoStateButtonStatus) # update the label of the button with proper status
        mess = "2 state buttton is now %s" % self.ui.twoStateButtonStatus
        print mess
        self.ui.dialogBox.setText( mess ) # displays message in dialogbox
        

        
        """
          __ _ _        ____       _           _             
         / _(_) | ___  / ___|  ___| | ___  ___| |_ ___  _ __ 
        | |_| | |/ _ \ \___ \ / _ \ |/ _ \/ __| __/ _ \| '__|
        |  _| | |  __/  ___) |  __/ |  __/ (__| || (_) | |   
        |_| |_|_|\___| |____/ \___|_|\___|\___|\__\___/|_|   
                                                             
         """

        
    def selectFITS(self):
    #==============================================================================
    #         This method is called when the "load fits file"button is called
    #==============================================================================        
        filepath = QtGui.QFileDialog.getOpenFileName( self, "Select FITS file", "./data/", "FITS files (*.fits);;All Files (*)") #Note: Use getOpenFileNames method (with a "s") to enable multiple file selection
        print filepath        
        if(filepath!=''):
            print (str(filepath))
            data = pyfits.getdata(str(filepath)) # Load fits file using the pyfits library
            pliInGui(data) # Displays the data in the GUI.
            mess = filepath+" displayed in window 1"
        else:
            mess = "No File selected skipping..."
            print mess
        self.ui.dialogBox.setText(mess) # displays message
    
        
        """
                             _           ____            
          ___ ___  _ __ ___ | |__   ___ | __ )  _____  __
         / __/ _ \| '_ ` _ \| '_ \ / _ \|  _ \ / _ \ \/ /
        | (_| (_) | | | | | | |_) | (_) | |_) | (_) >  < 
         \___\___/|_| |_| |_|_.__/ \___/|____/ \___/_/\_\
                                                         
        """
    def theButtonOKIsClicked(self):
    #==============================================================================
    #         This method is called when "ok" button is clicked
    #==============================================================================                
        text = str(self.ui.textEdit.toPlainText()) #Get the text from the text edit Field entry
        self.ui.ComboBox.addItem(text)# Adds the text in combo box. Note: Use currentText() to get the current Text in the combobox
        mess = "Added Message: %s in Combobox" % text
        print mess
        self.ui.dialogBox.setText(mess) # prints some messages...
        self.ui.nbItemsComboBox += 1 # updates the "nbItemsComboBox" attribute
        self.ui.ComboBox.setCurrentIndex(self.ui.nbItemsComboBox-1) # sets the current item to the last one entered

    def resetComboboxClicked(self):
    #==============================================================================
    #         This method is called when "reset ComboBox" button is clicked
    #==============================================================================           
        nb = self.ui.ComboBox.count() # retrieves the nb of items in the combo box
        for i in range(nb):
            self.ui.ComboBox.removeItem(0) # removes the first item "nb" times => i.e clear all items
        self.ui.nbItemsComboBox = 0 #upodates the attribute
        
    def getComboBox(self):
    #==============================================================================
    #         This method is called when the combo selector is changed by the user
    #==============================================================================   
        currText=self.ui.ComboBox.currentText() #Retrieves the ciurrent text displayed in comboBox
        mess = "ComboBox changed to: %s" % currText
        self.ui.dialogBox.setText(mess) #displays message

    

        
        
"""
       _   _                      __                  _   _                 
  ___ | |_| |__   ___ _ __ ___   / _|_   _ _ __   ___| |_(_) ___  _ __  ___ 
 / _ \| __| '_ \ / _ \ '__/ __| | |_| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
| (_) | |_| | | |  __/ |  \__ \ |  _| |_| | | | | (__| |_| | (_) | | | \__ \
 \___/ \__|_| |_|\___|_|  |___/ |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
                                                                            
     _       __ _       _ _   _             
  __| | ___ / _(_)_ __ (_) |_(_) ___  _ __  
 / _` |/ _ \ |_| | '_ \| | __| |/ _ \| '_ \ 
| (_| |  __/  _| | | | | | |_| | (_) | | | |
 \__,_|\___|_| |_|_| |_|_|\__|_|\___/|_| |_|
                                            

"""




def updateDMPos(color='gist_earth'):
    exec("wp.ui.DMPlotWindow.canvas.axes.clear()")
    exec("wp.ui.DMPlotWindow.canvas.axes.matshow(wp.DM_Gui.pixels.transpose(), aspect='auto', origin='lower')")
    exec("wp.ui.DMPlotWindow.canvas.draw()")
    #wp.DM_Gui.drawMap()
    print "updated DM Positions"
    #DMPos = 'junk'#aortc.get_HO_ACT_POS_REF_MAP()







"""
 _                        _     _                  _    ____  ____  
| | __ _ _   _ _ __   ___| |__ (_)_ __   __ _     / \  |  _ \|  _ \ 
| |/ _` | | | | '_ \ / __| '_ \| | '_ \ / _` |   / _ \ | |_) | |_) |
| | (_| | |_| | | | | (__| | | | | | | | (_| |  / ___ \|  __/|  __/ 
|_|\__,_|\__,_|_| |_|\___|_| |_|_|_| |_|\__, | /_/   \_\_|   |_|    
                                        |___/                       

"""

#==============================================================================================================
#          !!!!!    Here we launch the MAIN PyQt application    !!!!!
#==============================================================================================================     

hostname = "aortc3"
username = "spacimgr"

aortc = VLTTools.VLTConnection(hostname=hostname, username=username)

app = QApplication([]) #Defines that the app is a Qt application
wp = Graffiti_ui_class(aortc = aortc) # !!!!!!!    THE GUI REALLY STARTS HERE   !!!!!!
wp.initialize()  # Can I initialize here?
wp.show() # shows the GUI (can be hidden by typing wp.hide())



print "Graffiti loaded."

