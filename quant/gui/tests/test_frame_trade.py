import unittest
from PyQt5 import QtWidgets
import sys
from quant.gui.frames.frametrade import FrameTrade
from quant.gui.gui_logic import LogicMgr

class TestMainWindow(unittest.TestCase):
    def test_main(self):
        app = QtWidgets.QApplication(sys.argv)
        win = FrameTrade(logic=LogicMgr())
        win.show()
        app.exec_()