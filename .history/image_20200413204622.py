import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPixmap


class Window(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('images')
        self.setGeometry(50, 50, 500, 500)
        self.UI()

    def UI(self):
        self.photo = QtWidgets.QLabel(self)
        path = "D:/copy/1/dji_0021"
        self.photo.setPixmap(QPixmap())
        self.photo.move(150, 50)
        self.show()


def main():
    App = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()
