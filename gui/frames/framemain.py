from PyQt5 import QtWidgets
from .framedata import FrameData
from .frameresult import FrameResult

class FrameMain(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FrameMain, self).__init__(parent)

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        vbox.addWidget(FrameData())
        vbox.addWidget(FrameResult())
