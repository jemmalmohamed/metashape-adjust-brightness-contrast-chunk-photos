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
    # path = ''
    # image = Image

    def __init__(self, parent):

        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle(
            "ADJUST PHOTOS BRIGHTNESS , CMG (MAROC)")

        # self.adjustSize()
        self.setMaximumHeight(880)
        self.createParamsGridLayout()
        self.createButtonsGridLayout()
        self.createImageViewerLayout()

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.groupBoxParams)
        vbox.addWidget(self.groupBoxViewer)
        vbox.addWidget(self.groupBoxButtons)

        self.setLayout(vbox)

        self.exec()

    def createImageViewerLayout(self):

        self.groupBoxViewer = QtWidgets.QGroupBox()

        gridViewerLayout = QtWidgets.QGridLayout()
        self.scaleFactor = 0.0
        self.imageLabel = QtWidgets.QLabel(self)
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setMinimumHeight(605)
        # self.scrollArea.setMaximumHeight(605)

        self.scrollArea.setMinimumWidth(830)
        self.scrollArea.setMaximumWidth(830)

        self.getChunk()

        self.getPaths()

        # path = "D:/copy/1/dji_0021"
        # self.image = QtGui.QPixmap(self.path_photo)
        # self.imageLabel.setPixmap(self.image)

        self.getImage()

        self.scrollArea.setWidgetResizable(False)
        self.normalSize()
        self.scaleImage(0.16)

        gridViewerLayout.addWidget(self.scrollArea, 1, 0)
        self.createViewerButtons()
        gridViewerLayout.addWidget(self.groupBoxViewerBtn, 0, 0)
        self.groupBoxViewer.setLayout(gridViewerLayout)

    def createViewerButtons(self):
        self.groupBoxViewerBtn = QtWidgets.QGroupBox()

        gridViewerBtnLayout = QtWidgets.QGridLayout()

        self.btnZoomIn = QtWidgets.QPushButton("+")
        self.btnZoomIn.setFixedSize(23, 23)

        self.btnZoomOut = QtWidgets.QPushButton("-")
        self.btnZoomOut.setFixedSize(23, 23)

        self.btnZoomOut = QtWidgets.QPushButton("-")
        self.btnZoomOut.setFixedSize(23, 23)

        gridViewerBtnLayout.addWidget(self.btnZoomIn, 0, 0)
        gridViewerBtnLayout.addWidget(self.btnZoomOut, 0, 1)

        QtCore.QObject.connect(
            self.btnZoomIn, QtCore.SIGNAL("clicked()"),  self.zoomIn)

        QtCore.QObject.connect(
            self.btnZoomOut, QtCore.SIGNAL("clicked()"),  self.zoomOut)

        # self.btnFit.clicked.connect(lambda: self.fitToWindow(True))
        self.groupBoxViewerBtn.setLayout(gridViewerBtnLayout)

    def createButtonsGridLayout(self):

        self.groupBoxButtons = QtWidgets.QGroupBox()

        gridBtnLayout = QtWidgets.QGridLayout()

        self.btnQuit = QtWidgets.QPushButton("Cancel")
        self.btnQuit.setFixedSize(150, 23)

        self.btnSubmit = QtWidgets.QPushButton("OK")
        self.btnSubmit.setFixedSize(150, 23)

        gridBtnLayout.addWidget(self.btnSubmit, 0, 0)
        gridBtnLayout.addWidget(self.btnQuit, 0, 1)
        self.btnSubmit.setEnabled(False)
        QtCore.QObject.connect(self.btnQuit, QtCore.SIGNAL(
            "clicked()"), self, QtCore.SLOT("reject()"))

        QtCore.QObject.connect(
            self.btnSubmit, QtCore.SIGNAL("clicked()"), self.adjustChunkPhotos)

        self.groupBoxButtons.setLayout(gridBtnLayout)

    def createParamsGridLayout(self):
        self.groupBoxParams = QtWidgets.QGroupBox('Adjustment parameters')

        gridParamsLayout = QtWidgets.QGridLayout()
        gridParamsLayout.setHorizontalSpacing(50)
        self.label_chunk = QtWidgets.QLabel('Chunk : ')

        self.chunksBox = QtWidgets.QComboBox()
        self.chunksBox.resize(200, 23)

        self.getChunks()
        for chunk in self.chunks:
            self.chunksBox.addItem(chunk.label, chunk.key)

        self.label_brightness = QtWidgets.QLabel('Image brightness (%): ')
        self.brightness = QtWidgets.QSpinBox()
        self.brightness.setMaximum(500)
        self.brightness.setSingleStep(20)
        self.brightness.setMinimum(0)
        self.brightness.setValue(100)

        self.label_contrast = QtWidgets.QLabel('Image contrast (%): ')
        self.contrast = QtWidgets.QSpinBox()
        self.contrast.setMaximum(500)
        self.contrast.setSingleStep(20)
        self.contrast.setMinimum(0)
        self.contrast.setValue(100)

        self.label_folder = QtWidgets.QLabel('Select folder  : ')
        self.btn_select_folder = QtWidgets.QPushButton("Select...")
        self.btn_select_folder.setFixedSize(150, 23)
        self.path_label = QtWidgets.QLabel('Selected Path : ...')

        self.space = QtWidgets.QLabel('         ')

        self.chunk_create_label = QtWidgets.QLabel("Create new Chunk")

        self.chkCreateChunk = QtWidgets.QCheckBox()
        self.chkCreateChunk.setChecked(True)
        # adding widget
        gridParamsLayout.addWidget(self.label_chunk, 0, 0)
        gridParamsLayout.addWidget(self.chunksBox, 0, 1)
        gridParamsLayout.addWidget(self.label_folder, 0, 2)
        gridParamsLayout.addWidget(self.btn_select_folder, 0, 3)

        gridParamsLayout.addWidget(self.label_brightness, 1, 0)
        gridParamsLayout.addWidget(self.brightness, 1, 1)
        gridParamsLayout.addWidget(self.path_label, 1, 2)

        gridParamsLayout.addWidget(self.label_contrast, 2, 0)
        gridParamsLayout.addWidget(self.contrast, 2, 1)

        gridParamsLayout.addWidget(self.chunk_create_label, 2, 2)
        gridParamsLayout.addWidget(self.chkCreateChunk, 2, 3)
        QtCore.QObject.connect(
            self.btn_select_folder, QtCore.SIGNAL("clicked()"), self.selectFolder)

        self.chunksBox.currentIndexChanged.connect(self.getChunk)
        self.brightness.valueChanged.connect(self.getPixmapFromEnhance)
        self.contrast.valueChanged.connect(self.getPixmapFromEnhance)
        self.groupBoxParams.setLayout(gridParamsLayout)

    def zoomIn(self):

        self.scaleImage(1.25)

    def zoomOut(self):

        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(
            self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep()/2)))

    def fitToWindow(self, fitToWindow):

        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

    def getChunks(self):
        self.chunks = Metashape.app.document.chunks

        if len(self.chunks) == 0:
            Metashape.app.messageBox('No chunk in project')

    def getChunk(self):
        chunk_key = self.chunksBox.currentData()
        self.chunk = doc.findChunk(chunk_key)

        self.getPaths()
        self.getImage()

    def selectFolder(self):

        directoryPath = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Directory")
        dossier = directoryPath.split('/')[-1]
        path = 'Selected Path : {}'.format(directoryPath)
        self.path_label.setText(path)
        self.btnSubmit.setEnabled(True)
        self.path_folder = directoryPath

    def getPaths(self):
        self.paths = []
        for c in self.chunk.cameras:
            path = c.photo.path
            self.paths.append(path)

        if len(self.paths) == 0:
            Metashape.app.messageBox('No photos in this chunk')

    def getImage(self):
        self.path_photo = self.paths[0]

        self.image = QtGui.QPixmap(self.path_photo)

        self.imageLabel.setPixmap(self.image)

    def nextPhoto(self, index):
        self.path_photo = self.paths[index + 1]
        if index == len(self.paths) + 1:
            self.path_photo = path[0]

    def previousPhoto(self, index):
        self.path_photo = self.paths[index - 1]
        if index == 0:
            self.path_photo = path[len(self.paths) - 1]

    def adjustImage(self, image):
        brghitness = self.brightness.value() / 100
        contrast = self.contrast.value() / 100

        imageEnhancer = ImageEnhance.Brightness(image)
        imgBright = imageEnhancer.enhance(brghitness)

        imageEnhancer = ImageEnhance.Contrast(imgBright)
        imgContrast = imageEnhancer.enhance(contrast)

        return imgContrast

    def getPixmapFromEnhance(self):

        image = Image.open(self.paths[0])

        img = self.adjustImage(image)

        self.image = img.toqimage()
        self.image = QtGui.QPixmap(self.image)
        self.imageLabel.setPixmap(self.image)
        image.close()

    def get_exif(self, image):

        exif = image._getexif()

        return exif

    def add_new_chunk(self, images):
        doc = Metashape.app.document
        new_chunk = doc.addChunk()
        new_chunk.label = 'Adjusted ' + self.chunk.label
        new_chunk.addPhotos(images)

    def adjustChunkPhotos(self):
        print("Import Copy Photos Script started...")

        imageList = []
        commun = os.path.commonpath(self.paths)
        commun_without_drive = os.path.splitdrive(commun)[1]
        commun_without_drive = commun_without_drive.replace('\\', '/')

        for c in self.chunk.cameras:
            source = c.photo.path
            destination = self.path_folder

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

                enhancer = self.adjustImage(image)

                path = path_dist + '/' + c.label + '.jpg'
                enhancer.save(
                    path, exif=image.info["exif"])

                imageList.append(path)
                image.close()

                # shutil.copy2(source, path_dist)
            except RuntimeError:
                Metashape.app.messageBox('error')

        if self.chkCreateChunk.isChecked():

            self.add_new_chunk(imageList)
        self.close()
        print("Script finished!")
        # Metashape.app.messageBox('Adjusting and Copy  successful !')
        return True


def adjustChunkPhotos():
    global doc

    doc = Metashape.app.document

    app = QtWidgets.QApplication.instance()
    parent = app.activeWindow()

    dlg = CopyChunkPhotosDlg(parent)


label = "Custom menu/Adjust brightness Chunk"
Metashape.app.addMenuItem(label, adjustChunkPhotos)
print("To execute this script press {}".format(label))