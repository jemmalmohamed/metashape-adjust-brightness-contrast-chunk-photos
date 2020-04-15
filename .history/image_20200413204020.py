import sys
from PySide2 import QtGui, QtCore, QtWidgets


class Window(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('images')
        self.setGeometry(50, 50, 500, 500)
        self.UI()

    def UI(self):
        self.photo = QtWidgets.QLabel(self)


def main():
    App = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()
