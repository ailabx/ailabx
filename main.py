import sys
from PyQt5 import QtWidgets
from gui.mainwindow import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.showMaximized()
    app.exec_()