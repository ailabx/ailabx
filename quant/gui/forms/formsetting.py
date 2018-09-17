from PyQt5 import QtWidgets
from PyQt5 import QtGui

class FormSetting(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(FormSetting,self).__init__(parent)
        self.setWindowTitle('设置')