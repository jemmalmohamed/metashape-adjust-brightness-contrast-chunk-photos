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
    image = Image

    def __init__(self, parent):

        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle(
            "ADJUST PHOTOS BRIGHTNESS , CMG (MAROC)")

        self.resize(1100, 850)
        self.adjustSize()

        self.createGridLayout()
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.groupBox)

        self.setLayout(vbox)

        self.exec()

    def createGridLayout(self):
        self.groupBox = QtWidgets.QGroupBox('chunk')

        gridLayout = QtWidgets.QGridLayout()
        self.label_chunk = QtWidgets.QLabel('Chunk : ')
        # self.label_chunk.resize(100, 23)

        self.chunksBox = QtWidgets.QComboBox()
        self.chunksBox.resize(200, 23)
        chunks = self.getChunks()
        for chunk in chunks:
            self.chunksBox.addItem(chunk.label, chunk.key)

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

        self.folder_selected = QtWidgets.QLabel('Selected folder  : ')
        # self.label_folder.resize(200, 23)

        self.path_label = QtWidgets.QLabel('Path :')

        self.space = QtWidgets.QLabel('         ')

        self.chunk_create_label = QtWidgets.QLabel("Create new Chunk")

        self.chkCreateChunk = QtWidgets.QCheckBox()
        # adding widget
        gridLayout.addWidget(self.label_chunk, 0, 0)

        gridLayout.addWidget(self.chunksBox, 0, 1)

        gridLayout.addWidget(self.label_brightness, 1, 0)
        gridLayout.addWidget(self.brightness, 1, 1)

        gridLayout.addWidget(self.label_contrast, 2, 0)
        gridLayout.addWidget(self.contrast, 2, 1)

        gridLayout.addWidget(self.folder_selected, 3, 0)

        gridLayout.addWidget(self.chunk_create_label, 4, 0)
        gridLayout.addWidget(self.chkCreateChunk, 4, 1)

        # gridLayout.addWidget(self.space, 6, 1)

        # gridLayout.addWidget(self.btnZoomIn, 7, 1)
        # gridLayout.addWidget(self.btnZoomOut, 7, 2)

        # gridLayout.addWidget(self.btnP1, 8, 1)
        # gridLayout.addWidget(self.btnQuit, 8, 2)

        self.groupBox.setLayout(gridLayout)

    def getChunks(self):
        return Metashape.app.document.chunks


def copyChnukPhotos():
    global doc

    doc = Metashape.app.document

    app = QtWidgets.QApplication.instance()
    parent = app.activeWindow()

    dlg = CopyChunkPhotosDlg(parent)


label = "Custom menu/Adjust brightness photos"
Metashape.app.addMenuItem(label, copyChnukPhotos)
print("To execute this script press {}".format(label))
