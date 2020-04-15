import Metashape
from PySide2 import QtGui, QtCore, QtWidgets, QtPrintSupport


from PySide2.QtCore import QDir, Qt
from PySide2.QtGui import QImage, QPainter, QPalette, QPixmap
from PySide2.QtWidgets import (QAction, QApplication, QFileDialog, QLabel,
                               QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy)
from PySide2.QtPrintSupport import QPrintDialog, QPrinter


import datetime
import shapefile
import os
import shutil

from PIL import Image, ImageEnhance
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS

# Checking compatibility
compatible_major_version = "1.6"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(
        found_major_version, compatible_major_version))


class CopyChunkPhotosDlg(QtWidgets.QDialog):
    path = ''
    def __init__(self, parent):

        QtWidgets.QDialog.__init__(self, parent)

        self.setWindowTitle(
            "ADJUST PHOTOS BRIGHTNESS , CMG (MAROC)")

        self.resize(1100, 800)
        self.adjustSize()

        self.label_chunk = QtWidgets.QLabel('Chunk : ')
        self.label_chunk.resize(100, 23)

        self.chunksBox = QtWidgets.QComboBox()
        self.chunksBox.resize(200, 23)

        self.printer = QtPrintSupport.QPrinter
        self.scaleFactor = 0.0

        self.imageLabel = QtWidgets.QLabel(self)
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        # self.scrollArea.setWidget(self.imageLabel)
        # self.scrollArea.setParent(self)

        # self.scrollArea.setVisible(True)
        # self.set(self.scrollArea)

        self.createActions()
        # self.createMenus()

        # self.setWindowTitle("Image Viewer")
        # self.resize(500, 400)

        path = "D:/copy/1/dji_0021"

        self.imageLabel.setPixmap(QtGui.QPixmap(path))
        # self.imageLabel.setGeometry(100, 150, 900, 600)
        self.scaleFactor = 1.0

        self.printAct.setEnabled(True)
        self.fitToWindowAct.setEnabled(True)
        self.updateActions()

        if not self.fitToWindowAct.isChecked():
            self.imageLabel.adjustSize()

        # self.photo = QtWidgets.QLabel(self)
        # self.photo.setPixmap(QtGui.QPixmap(path).scaled(900, 600,
        #                                                 QtCore.Qt.KeepAspectRatio,
        #                                                 QtCore.Qt.SmoothTransformation))

        #   self.photo.setGeometry(100, 150, 900, 600)

        self.label_brightness = QtWidgets.QLabel('Image brightness (%): ')
        self.brightness = QtWidgets.QSpinBox()
        self.brightness.setMaximum(500)
        self.brightness.setSingleStep(10)
        self.brightness.setMinimum(0)
        self.brightness.setValue(100)

        self.label_contrast = QtWidgets.QLabel('Image contrast (%): ')
        self.contrast = QtWidgets.QSpinBox()
        self.contrast.setMaximum(500)
        self.contrast.setSingleStep(10)
        self.contrast.setMinimum(0)
        self.contrast.setValue(100)

        self.label_folder = QtWidgets.QLabel('Select folder  : ')
        self.label_folder.resize(200, 23)

        self.path_label = QtWidgets.QLabel('Path :')
        self.space = QtWidgets.QLabel('         ')
        self.chunk_create_label = QtWidgets.QLabel("Create new Chunk")

        self.chkCreateChunk = QtWidgets.QCheckBox()

        doc = Metashape.app.document
        chunks = doc.chunks

        for chunk in chunks:
            self.chunksBox.addItem(chunk.label, chunk.key)

        self.btnAdd = QtWidgets.QPushButton("Select...")
        self.btnAdd.setFixedSize(150, 23)

        self.btnQuit = QtWidgets.QPushButton("Cancel")
        self.btnQuit.setFixedSize(150, 23)

        self.btnP1 = QtWidgets.QPushButton("OK")
        self.btnP1.setFixedSize(150, 23)

        layout = QtWidgets.QGridLayout()  # creating layout

        layout.addWidget(self.label_chunk, 1, 1)
        layout.addWidget(self.chunksBox, 1, 2)

        layout.addWidget(self.label_brightness, 2, 1)
        layout.addWidget(self.brightness, 2, 2)

        layout.addWidget(self.label_contrast, 3, 1)
        layout.addWidget(self.contrast, 3, 2)

        layout.addWidget(self.label_folder, 4, 1)
        layout.addWidget(self.btnAdd, 4, 2)

        layout.addWidget(self.chunk_create_label, 5, 1)
        layout.addWidget(self.chkCreateChunk, 5, 2)

        layout.addWidget(self.space, 6, 1)

        layout.addWidget(self.btnP1, 7, 1)
        layout.addWidget(self.btnQuit, 7, 2)

        self.setLayout(layout)

        def proc_copy(): return self.copyChnukPhotos()
        def selectFolder(): return self.selectFolder()

        QtCore.QObject.connect(
            self.btnAdd, QtCore.SIGNAL("clicked()"), selectFolder)
        QtCore.QObject.connect(
            self.btnP1, QtCore.SIGNAL("clicked()"), proc_copy)

        QtCore.QObject.connect(self.btnQuit, QtCore.SIGNAL(
            "clicked()"), self, QtCore.SLOT("reject()"))

        self.btnP1.setEnabled(False)
        self.exec()

    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(),
                                size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(
            self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep()/2)))

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O",
                               triggered=self.open)

        self.printAct = QAction("&Print...", self, shortcut="Ctrl+P",
                                enabled=False, triggered=self.print_)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                               triggered=self.close)

        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++",
                                 enabled=False, triggered=self.zoomIn)

        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-",
                                  enabled=False, triggered=self.zoomOut)

        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S",
                                     enabled=False, triggered=self.normalSize)

        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False,
                                      checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)

        # self.aboutAct = QAction("&About", self, triggered=self.about)

        # self.aboutQtAct = QAction("About &Qt", self,
        #                           triggered=QApplication.instance().aboutQt)

    def selectFolder(self):

        directoryPath = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Directory")
        dossier = directoryPath.split('/')[-1]
        path = 'path : {}'.format(directoryPath)
        self.path_label.setText(path)
        self.btnP1.setEnabled(True)
        self.path = directoryPath

    def get_paths(self, chunk):
        paths = []
        for c in chunk.cameras:

            path = c.photo.path
            paths.append(path)
        return paths

    def get_exif(self, image):

        exif = image._getexif()

        return exif

    print('--------------------------------')

    def copyChnukPhotos(self):

        print("Import Copy Photos Script started...")
        paths = []
        commun = []
        doc = Metashape.app.document
        chunks = doc.chunks

        chunk_key = self.chunksBox.currentData()
        chunk = doc.findChunk(chunk_key)

        paths = self.get_paths(chunk)

        commun = os.path.commonpath(paths)
        commun_without_drive = os.path.splitdrive(commun)[1]
        commun_without_drive = commun_without_drive.replace('\\', '/')

        for c in chunk.cameras:

            source = c.photo.path
            destination = self.path

            path_without_drive = os.path.splitdrive(source)[1]
            subfolder = os.path.splitext(path_without_drive)[0]
            path_to_photo = os.path.split(path_without_drive)[0]

            folders = path_to_photo.split('/')

            path_dist = destination + path_to_photo

            path_dist = path_dist.replace(commun_without_drive, '')

            try:
                if not os.path.exists(path_dist):
                    os.makedirs(path_dist)

                image = Image.open(source)
                exif = self.get_exif(image)
                enhancer = ImageEnhance.Brightness(image)
                path = path_dist + '/' + c.label + '.jpg'

                enhancer.enhance(0.5).save(path, exif=image.info["exif"])

                image.close()

                # shutil.copy2(source, path_dist)
            except RuntimeError:
                Metashape.app.messageBox('error')

        print("Script finished!")
        Metashape.app.messageBox('copy successful !')
        return True


def copyChnukPhotos():
    global doc

    doc = Metashape.app.document

    app = QtWidgets.QApplication.instance()
    parent = app.activeWindow()

    dlg = CopyChunkPhotosDlg(parent)


label = "Custom menu/Adjust brightness photos"
Metashape.app.addMenuItem(label, copyChnukPhotos)
print("To execute this script press {}".format(label))
