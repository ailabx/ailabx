from PyQt5 import QtWidgets

class FrameResult(QtWidgets.QTabWidget):
    def __init__(self,parent=None):
        super(FrameResult,self).__init__(parent)
        self.addTab(QtWidgets.QTextEdit(),'数据')
