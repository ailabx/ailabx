from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.uic import loadUi
from .forms.formsetting import FormSetting
from .frames.frameresult import FrameResult
from .frames.framebacktest import FrameBacktest
from .frames.framestrategies import FrameStrategies
from .frames.frametrade import FrameTrade
import os
import pandas as pd

from .models import table_models
import traceback
from qtpy.QtWebEngineWidgets import QWebEngineView
from .gui_logic import LogicMgr
from ..engine.common.logging_utils import logger_utils

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        path = os.path.abspath(os.path.join(os.path.abspath(__file__), ".."))
        file = path + '/ui/mainwindow.ui'
        loadUi(file, self)

        self.mgr = LogicMgr()
        logger_utils.signal = self.mgr.signal

        self.init_base_info()
        #self.init_menu()
        self.init_toolbar()
        #self.init_frames()




        self.view = QWebEngineView()
        webview_layout = self.webview_layout
        webview_layout.addWidget(self.view)

        self.view.setEnabled(True)
        self.view.setUrl(QtCore.QUrl("http://www.ailabx.com"))



        frame = FrameResult(logic=self.mgr)
        self.vl_results.addWidget(frame)

        frame_bkt = FrameBacktest(logic=self.mgr)
        self.vl_top_left.addWidget(frame_bkt)

        frame_stras = FrameStrategies(logic=self.mgr)
        self.vl_top_right.addWidget(frame_stras)

    def init_frames(self):







        frame_trade = FrameTrade(logic=self.mgr)
        self.vl_trade.addWidget(frame_trade)





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

