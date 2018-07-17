from PyQt5 import QtWidgets
from PyQt5 import QtGui
from .forms.formsetting import FormSetting
from .frames.framemain import FrameMain
import os
import pandas as pd
from .consts import *
from .models import table_models
import traceback

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

        loaddata_action = QtWidgets.QAction(QtGui.QIcon('images/logo.png'),'加载数据',self)
        loaddata_action.triggered.connect(self.loaddata)
        loaddata = self.addToolBar('加载数据')
        loaddata.addAction(loaddata_action)

    def show_setting(self):
        self.setting = FormSetting()
        self.setting.show()

    def loaddata(self):
        try:
            filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                       "选取数据文件",
                                                                       os.getcwd() + '//data',
                                                                       "CSV Files (*.csv);;All Files (*)")  # 设置文件扩展名过滤,注意用双分号间隔
            #self.text_file.setText(filename)
            datafeed = CSVDataFeed(csv=filename)


            table = mgr_frames.get_frame(FRAMES.FRAME_DATA_TABLE)

            table.setModel(table_models.DataFrameTableModel(df=datafeed.data))
        except:
            print(traceback.print_exc())