import Metashape
from PySide2 import QtGui, QtCore, QtWidgets

import datetime
import shapefile
import os


# Checking compatibility
compatible_major_version = "1.6"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(
        found_major_version, compatible_major_version))


class CopyChunkPhotosDlg(QtWidgets.QDialog):

    def __init__(self, parent):

        QtWidgets.QDialog.__init__(self, parent)

        self.setWindowTitle(
            "COPY CHUNK PHOTOS , CMG (MAROC)")
        self.resize(250, 150)
        self.label_chunk = QtWidgets.QLabel('Chunk : ')
        self.chunksBox = QtWidgets.QComboBox()
        self.chunksBox.resize(200, 23)

        # self.label_time = QtWidgets.QLabel(
        #     'Maximum time between photos (seconds): ')
        # self.spinX = QtWidgets.QSpinBox()
        # self.spinX.setMinimum(1)
        # self.spinX.setValue(60)

        # self.chkMerge = QtWidgets.QCheckBox("Merge Flights Chunks")
        # self.chkMerge.setToolTip(
        #     "Merge chunks to have group sensors per flight")
        # self.chkMerge.stateChanged.connect(self.toggleChkRemove)
        # self.spinX.setFixedSize(100, 25)

        # self.chkRemove = QtWidgets.QCheckBox("Remove Flights Chunks")
        # self.chkRemove.setToolTip(
        #     "Remove chunks after merging flights chunks")
        # self.chkRemove.setEnabled(False)
        # self.spinX.setFixedSize(100, 25)

        self.btnQuit = QtWidgets.QPushButton("Cancel")
        self.btnQuit.setFixedSize(100, 23)

        self.btnP1 = QtWidgets.QPushButton("OK")
        self.btnP1.setFixedSize(100, 23)

        layout = QtWidgets.QGridLayout()  # creating layout

        layout.addWidget(self.label_chunk, 1, 1)
        layout.addWidget(self.chunksBox, 1, 2)
        # layout.addWidget(self.chkMerge, 2, 1)
        # layout.addWidget(self.chkRemove, 2, 2)

        layout.addWidget(self.btnP1, 3, 1)
        layout.addWidget(self.btnQuit, 3, 2)

        self.setLayout(layout)

        def proc_copy(): return self.copyChnukPhotos()

        QtCore.QObject.connect(
            self.btnP1, QtCore.SIGNAL("clicked()"), proc_copy)

        QtCore.QObject.connect(self.btnQuit, QtCore.SIGNAL(
            "clicked()"), self, QtCore.SLOT("reject()"))

        self.exec()

    def toggleChkRemove(self, state):

        if state > 0:
            self.chkRemove.setEnabled(True)
        else:
            self.chkRemove.setEnabled(False)

    def add_new_chunk(self, images, nb):
        doc = Metashape.app.document
        new_chunk = doc.addChunk()
        new_chunk.label = 'flight ' + str(nb)
        new_chunk.addPhotos(images)
        return new_chunk

    def copyChnukPhotos(self):
        print("Import Copy Photos Script started...")

        doc = Metashape.app.document
        chunks = doc.chunks

        date_previous = chunk.cameras[0].photo.meta['Exif/DateTime']
        date_previous = datetime.datetime.strptime(
            date_previous, '%Y:%m:%d %H:%M:%S')
        image_list_by_flight = []

        # for c in chunk.C:

        #     date_current = c.photo.meta['Exif/DateTime']
        #     date_current = datetime.datetime.strptime(
        #         date_current, '%Y:%m:%d %H:%M:%S')

        #     sec = (date_current-date_previous).total_seconds()

        #     if(sec < time_between_photos):
        #         image_list_by_flight.append(c.photo.path)
        #         if c == sorted_cameras[-1]:
        #             print('last flight')
        #             i = i+1
        #             print('Flight {} : {} Photos'.format(
        #                 i, len(image_list_by_flight)))
        #             new_chunk = self.add_new_chunk(image_list_by_flight, i)
        #             list_of_new_chunk.append(new_chunk)
        #             list_of_keys_new_chunk.append(new_chunk.key)

        #     else:
        #         i = i + 1
        #         print('Flight {} : {} Photos'.format(
        #             i, len(image_list_by_flight)))
        #         new_chunk = self.add_new_chunk(image_list_by_flight, i)
        #         list_of_new_chunk.append(new_chunk)
        #         list_of_keys_new_chunk.append(new_chunk.key)
        #         image_list_by_flight = []
        #         image_list_by_flight.append(c.photo.path)

        #     date_previous = date_current

        # if self.chkMerge.isChecked():
        #     print('merging flights ....')
        #     doc.mergeChunks(chunks=list_of_keys_new_chunk)

        # if self.chkRemove.isChecked():
        #     print('Flights chunks removing...')
        #     doc.remove(list_of_new_chunk)
        print("Script finished!")
        self.close()
        return True


def copyChnukPhotos():
    global doc

    doc = Metashape.app.document

    app = QtWidgets.QApplication.instance()
    parent = app.activeWindow()

    dlg = CopyChunkPhotosDlg(parent)


label = "Custom menu/Copy Chunk photos"
Metashape.app.addMenuItem(label, copyChnukPhotos)
print("To execute this script press {}".format(label))
