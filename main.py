import sys,os
from PyQt5 import QtWidgets
from quant.gui.mainwindow import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.showMaximized()

    with open(os.getcwd() + '/quant/gui/ui/style.qss', 'r') as q:
        app.setStyleSheet(q.read())

    app.exec_()