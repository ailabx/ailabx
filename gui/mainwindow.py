from PyQt5 import QtWidgets
from PyQt5 import QtGui
from .forms.formsetting import FormSetting
from .frames.framemain import FrameMain

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.init_base_info()
        self.init_menu()
        self.init_toolbar()

        self.setCentralWidget(FrameMain(self))

    def init_base_info(self):
        self.setWindowTitle('智能量化系统 - ailabx智能量化实验室')
        self.setWindowIcon(QtGui.QIcon('images/logo.png'))

    def init_menu(self):
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu('&文件')
        tool_menu = self.menu.addMenu('&工具')
        about_menu = self.menu.addMenu('&关于')

    def init_toolbar(self):
        # 工具栏
        setting_action = QtWidgets.QAction(QtGui.QIcon('images/logo.png'), '设置', self)
        # setting_action.setShortcut('Ctrl+Q')
        setting_action.triggered.connect(self.show_setting)
        setting = self.addToolBar('设置')
        setting.addAction(setting_action)

    def show_setting(self):
        self.setting = FormSetting()
        self.setting.show()