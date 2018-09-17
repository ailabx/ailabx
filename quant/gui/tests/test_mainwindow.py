import unittest
from PyQt5 import QtWidgets
import sys
from quant.gui.mainwindow import MainWindow

class TestMainWindow(unittest.TestCase):
    def test_main(self):
        app = QtWidgets.QApplication(sys.argv)
        win = MainWindow()
        win.showMaximized()
        app.exec_()