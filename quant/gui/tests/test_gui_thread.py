import unittest
from quant.gui.gui_logic import ThreadWorker
from PyQt5 import QtWidgets
import sys,traceback


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.btn = QtWidgets.QPushButton('test',self)
        self.btn.clicked.connect(self.clicked)

        self.edit = QtWidgets.QTextEdit(self)
        self.btn.move(10,10)
        self.edit.move(30,50)

    def clicked(self):
        print('clicked')
        self.thread = ThreadWorker()
        try:
            self.thread.signal.connect(self.callback)
            self.thread.start()
        except:
            traceback.print_exc()
    def callback(self):
        self.btn.setText('callback')
        self.edit.append('okok')


class TestGuiThread(unittest.TestCase):

    def test_gui(self):
        app = QtWidgets.QApplication(sys.argv)
        win = MyWidget()

        win.show()
        app.exec_()