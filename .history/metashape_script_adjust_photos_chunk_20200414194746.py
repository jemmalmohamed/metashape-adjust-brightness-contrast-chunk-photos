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
        self.label_chunk.resize(100, 23)
        gridLayout.addWidget(self.label_chunk, 0, 0)

        self.chunksBox = QtWidgets.QComboBox()
        self.chunksBox.resize(200, 23)
        chunks = self.getChunks()
        for chunk in chunks:
            self.chunksBox.addItem(chunk.label, chunk.key)
        gridLayout.addWidget(self.chunksBox, 0, 1)

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
