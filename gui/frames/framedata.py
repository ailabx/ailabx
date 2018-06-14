from PyQt5 import QtWidgets
import os
from ..consts import *
from ..models import table_models
import pandas as pd

class FrameData(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(FrameData,self).__init__(parent=parent)

        vlayout = QtWidgets.QVBoxLayout(self)
        self.groupbox = QtWidgets.QGroupBox('数据文件：')
        vlayout.addWidget(self.groupbox)

        self.setLayout(vlayout)

        self.init_groupbox()

    def init_groupbox(self):
        grid = QtWidgets.QGridLayout()
        self.groupbox.setLayout(grid)
        grid.addWidget(QtWidgets.QLabel('请选择：'), 0, 0)

        self.text_file = QtWidgets.QTextEdit('请选择：')
        grid.addWidget(self.text_file, 0, 1)

        btn = QtWidgets.QPushButton('...')
        btn.clicked.connect(self.btn_sel_clicked)
        grid.addWidget(btn,0,2)

    def btn_sel_clicked(self):
        #print(os.getcwd())
        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self,
                                                          "选取数据文件",
                                                          os.getcwd()+'//data',
                                                          "CSV Files (*.csv);;All Files (*)")  # 设置文件扩展名过滤,注意用双分号间隔
        self.text_file.setText(filename)
        df = pd.read_csv(filename)
        df.index = df['date']

        table = mgr_frames.get_frame(FRAMES.FRAME_DATA_TABLE)
        print(table,df.head())
        table.setModel(table_models.DataFrameTableModel(df=df))
