import unittest
from quant.gui.gui_logic import ThreadWorker
from PyQt5 import QtWidgets
import sys,traceback

class TestGuiThread(unittest.TestCase):
    def callback(self):
        self.btn.setText('callback')

    def clicked(self):
        print('clicked')
        self.thread = ThreadWorker()
        try:
            self.thread.signal.connect(self.callback)
            self.thread.start()
        except:
            traceback.print_exc()


    def test_gui(self):
        app = QtWidgets.QApplication(sys.argv)
        win = QtWidgets.QWidget()
        self.btn = QtWidgets.QPushButton('test')
        self.btn.clicked.connect(self.clicked)
        layout = QtWidgets.QVBoxLayout()
        win.setLayout(layout)
        layout.addWidget(self.btn)
        win.show()
        app.exec_()