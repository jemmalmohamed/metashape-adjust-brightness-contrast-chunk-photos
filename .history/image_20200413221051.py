# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 19:33:16 2019
@author: Tiny
"""
# =============================================================================
''' is implemented in PyQt5, the basic functions are as follows:
         1. Image zoom (click or shortcut), the single zoom scale partners can adjust themselves;
         2. Picture rotation (click or shortcut), the single rotation angle can be adjusted by the small partners themselves;
         3. Picture movement (click or shortcut key two ways, single move distance friends can adjust themselves) --> to be developed, follow-up. '''
# =============================================================================
# =============================================================================
 ''' There is a problem with this code: '''
 # The picture is reduced very small, the aspect ratio is not good, and after zooming in again, the picture is distorted, and the picture information is lost a lot!
 ''' Store the original image in memory, set a scaling ratio variable for the original image, and scale it based on the original image.
# =============================================================================
# =============================================================================
 ''' Note: '''
 # 1. self.imageLabel.setScaledContents(True) #Allow QLabel to scale its contents to fill the entire available space.
 #  can look at the settings to not set the picture of the board to show the difference;
 # 2. Note the difference in the usage of individual functions of PyQt4 and PyQt5;
 # 3. Many functions are similar, can be written as a function, do not need so many lines of code, are repeated;
 # 4. Change on the basis of others, play, everyone can be a reference.
# =============================================================================
# =============================================================================
 ''' PyQt5 and PyQt4 some differences, for the reference of the friends: '''
 # Need to use QtWidgets.QLabel(), # PyQt4
 # QLabel(); # PyQt5
#
 # Need to use QtWidgets.QAction(QIcon, QString, QObject), # PyQt4
 # not QAction(QIcon, QString, QObject); # PyQt5
#
#    The old style:
#        self.connect(origin, SIGNAL('completed'), self._show_results)  # PyQt4
#    should now be written in the new style:
#        origin.completed.connect(self._show_results)  # PyQt5
#
 # PyQt5 no longer supports PyQt4 kinds of recommended methods QMatrix
 # can be implemented by QTransform
# =============================================================================
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from PyQt5.QtWidgets import QMainWindow , QApplication
from PyQt5 import QtWidgets              # , QtCore, QtGui
 '''Define the main window(including menu bar, toolbar) '''
class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
                 F=QFont("ZYSong18030",12) # Set the font, font size
        self.setFont(f)
                 self.setWindowTitle("Image Processor") # window naming

                 self.imageLabel=QtWidgets.QLabel() # QtWidgets.QLabel() is required, not QLabel()
#        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
                 #Allows QLabel to scale its contents to fill the entire available space
                 self.imageLabel.setScaledContents(True)
                 # Comment out the sentence, the run will not display the picture
                 self.setCentralWidget(self.imageLabel)

        self.image=QImage()
                 If self.image.load("image/cc.png"): # If the image is loaded, then
                                         self.imageLabel.setPixmap(
                                             QPixmap.fromImage(self.image)) # Display image
                                         # Reset size
                                         Self.resize(self.image.width(),self.image.height())

                 self.createActions() # Create QActions such as Zoom In, Zoom Out, and Rotate
                 self.createMenus() # Create menu bar
                 self.createToolBars() # Create toolbar

         '''Create a zoom, rotate QAction'''
    def createActions(self):
        self.zoomInAction=QtWidgets.QAction(QIcon("image/zoomIn.gif"),
                                                                                         Self.tr("zoom in"), self) # is not QAction(QIcon, QString, QObject)
                 self.zoomInAction.setShortcut("Ctrl+I") # Set shortcuts
                 self.zoomInAction.setStatusTip(
                     self.tr("zoom in")) # Set the title bar
#        self.connect(self.zoomInAction,SIGNAL("triggered()"),
#                     self.slotZoomin)                              # PyQt4
        self.zoomInAction.triggered.connect(self.slotZoomIn)        # PyQt5

        self.zoomOutAction=QtWidgets.QAction(QIcon("image/zoomOut.gif"),
                                                                                           Self.tr("shrink"), self) # is not QAction(QIcon, QString, QObject)
        self.zoomOutAction.setShortcut("Ctrl+O") # Set shortcuts
                 self.zoomOutAction.setStatusTip(
                     self.tr("zoom")) # Set the title bar
#        self.connect(self.zoomOutAction,SIGNAL("triggered()"),
#                     self.slotZoomOut)                              # PyQt4
        self.zoomOutAction.triggered.connect(self.slotZoomOut)       # PyQt5

        self.rotateAction=QtWidgets.QAction(QIcon("image/rotate.gif"),
                                                                                         Self.tr("Shun"), self) # is not QAction(QIcon, QString, QObject)
                 self.rotateAction.setShortcut("Ctrl+R") # Set shortcuts
                 self.rotateAction.setStatusTip(
                     self.tr("Shun")) # Set the title bar
#        self.connect(self.rotateAction,SIGNAL("triggered()"),
#                     self.slotRotate)                               # PyQt4
        self.rotateAction.triggered.connect(self.slotRotate)         # PyQt5

        self.rotateAntiAction=QtWidgets.QAction(QIcon("image/rotateAnti.gif"),
                                                                                         Self.tr("reverse"), self) # is not QAction(QIcon, QString, QObject)
                 self.rotateAntiAction.setShortcut("Ctrl+E") # Set shortcuts
                 self.rotateAntiAction.setStatusTip(
                     self.tr("reverse")) # Set the title bar
#        self.connect(self.rotateAntiAction,SIGNAL("triggered()"),
#                     self.slotRotateAnti)                           # PyQt4
        self.rotateAntiAction.triggered.connect(self.slotRotateAnti) # PyQt5

         '''Create menu bar '''
    def createMenus(self):
                 zoomMenu=self.menuBar().addMenu(self.tr("zoom")) # Zoom menu option
                 zoomMenu.addAction(self.zoomInAction) # Zoom suboptions
                 zoomMenu.addAction(self.zoomOutAction) # Zoom out suboptions
                 rotateMenu=self.menuBar().addMenu(self.tr("rotate")) # rotate menu option
                 rotateMenu.addAction(self.rotateAction) #   suboption
                 # Reverse suboption
                 rotateMenu.addAction(self.rotateAntiAction)

         '''Create toolbar'''
    def createToolBars(self):
        fileToolBar=self.addToolBar("Print")
        fileToolBar.addAction(self.zoomInAction)
        fileToolBar.addAction(self.zoomOutAction)
        fileToolBar.addAction(self.rotateAntiAction)
        fileToolBar.addAction(self.rotateAction)

         '''Picture zoom(multiple can be set) '''
    def slotZoomIn(self):
                 If self.image.isNull(): # No image, no action is taken
            return
 # martix =QMatrix() # PyQt4, deprecated in PyQt5
        transform = QTransform()  # PyQt5
 # martix.scale(2,2) # PyQt4, PyQt5 is deprecated
        transform.scale(1.2,1.2)  # PyQt5
                 # corresponding matrix changed to transform
                 Self.image=self.image.transformed(transform);
                 # Display the image to the Qlabel control
                 self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
        self.resize(self.image.width(),self.image.height())

         '''Image zoom out(multiple can be set) '''
    def slotZoomOut(self):
                 If self.image.isNull(): # No image, no action is taken
            return
 # martix =QMatrix() # PyQt4, deprecated in PyQt5
        transform = QTransform()  # PyQt5
 # martix.scale(2,2) # PyQt4, PyQt5 is deprecated
        transform.scale(0.8,0.8)  # PyQt5
                 # corresponding matrix changed to transform
                 Self.image=self.image.transformed(transform);
                 # Display the image to the Qlabel control
                 self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
        self.resize(self.image.width(),self.image.height())

         '''The picture is rotated(angle can be set) '''
    def slotRotate(self):
                 If self.image.isNull(): # No image, no action is taken
            return
 # martix =QMatrix() # PyQt4, deprecated in PyQt5
        transform = QTransform()  # PyQt5
# martix.rotate(90) # PyQt4, PyQt5 is deprecated
        transform.rotate(90)      # PyQt5
                 # corresponding matrix changed to transform
                 Self.image=self.image.transformed(transform);
                 # Display the image to the Qlabel control
                 self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
        self.resize(self.image.width(),self.image.height())
         '''Image reverse rotation(angle can be set) '''
    def slotRotateAnti(self):
                 If self.image.isNull(): # No image, no action is taken
            return
 # martix =QMatrix() # PyQt4, deprecated in PyQt5
        transform = QTransform()  # PyQt5
 # martix.rotate(90) # PyQt4, PyQt5 is deprecated
        transform.rotate(-90)     # PyQt5
                 # corresponding matrix changed to transform
                 Self.image=self.image.transformed(transform);
                 # Display the image to the Qlabel control
                 self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
        self.resize(self.image.width(),self.image.height())

 '''Main function'''
if __name__ == '__main__':
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    app.exec_()
