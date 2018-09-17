import unittest,sys
from PyQt5 import QtWidgets
from quant.gui.frames import frameresult

class TestFrameResults(unittest.TestCase):
    def test_results(self):
        app = QtWidgets.QApplication(sys.argv)
        win = frameresult.FrameResult(logic=None)

        win.show()
        app.exec_()
