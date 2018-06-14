from PyQt5 import QtWidgets
from ..consts import *

class FrameResult(QtWidgets.QTabWidget):
    def __init__(self,parent=None):
        super(FrameResult,self).__init__(parent)

        table = QtWidgets.QTableView()
        self.addTab(table,'数据')

        mgr_frames.add_frame(FRAMES.FRAME_DATA_TABLE,table)

