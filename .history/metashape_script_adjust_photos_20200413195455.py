import Metashape
from PySide2 import QtGui, QtCore, QtWidgets

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
        self.resize(250, 150)
        self.label_chunk = QtWidgets.QLabel('Chunk : ')
        self.label_chunk.resize(100, 23)

        self.chunksBox = QtWidgets.QComboBox()
        self.chunksBox.resize(200, 23)

        self.label_brightness = QtWidgets.QLabel('Image brightness (%): ')
        self.brightness = QtWidgets.QSpinBox()
        self.brightness.setMaximum(500)
        self.brightness.setMinimum(0)
        self.brightness.setValue(100)

        self.label_contrast = QtWidgets.QLabel('Image contrast (%): ')
        self.contrast = QtWidgets.QSpinBox()
        self.contrast.setMaximum(500)
        self.contrast.setMinimum(0)
        self.contrast.setValue(100)

        self.label_folder = QtWidgets.QLabel('Select folder  : ')
        self.label_folder.resize(200, 23)

        self.path_label = QtWidgets.QLabel('Path :')

        self.chkCreateChun = QtWidgets.QCheckBox("Create new Chunk")


s       elf.checkCreateChunk = QtWidgets.QCheckBox

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

        layout.addWidget(self.path_label, 5, 1)

        layout.addWidget(self.checkCreateChunk, 6, 1)

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
