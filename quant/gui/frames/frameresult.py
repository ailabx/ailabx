from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import os,path
import pandas as pd
from ..gui_logic import LogicMgr
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from ...engine.consts import EventType
import traceback
from ..models.table_models import DataFrameTableModel
from ..models.ai_treeview import AiTreeView

class FrameResult(QtWidgets.QWidget):
    def __init__(self,logic,parent=None):
        super(FrameResult,self).__init__(parent)

        current_path = os.path.abspath(__file__)
        father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
        father_path = os.path.abspath(os.path.dirname(father_path) + os.path.sep + ".")
        file = father_path + '/ui/results.ui'
        loadUi(file,self)

        self.mgr = logic
        logic.signal.connect(self.on_events)
        self.init_visual()

        self.tree = AiTreeView()
        self.vl_trades.addWidget(self.tree)

    def init_visual(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.layout = QtWidgets.QVBoxLayout(self.visual_widget)
        self.layout.addWidget(self.canvas)


    def plot_data(self,data):
        data.plot(ax=self.ax)
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.show()


    def on_events(self,data):
        #print(data)
        if data and 'event_type' in data.keys():
            event_type = data['event_type']
            if event_type ==  EventType.onmessage:
                try:
                    #print(data)
                    #print(data['msg'])
                    if data and 'msg' in data.keys():
                    #   pass
                        self.edit_result.append(data['msg'])
                except:
                    traceback.print_exc()
            elif event_type is EventType.onfinished:
                performance = data['performance']
                model = DataFrameTableModel(df=performance)
                self.tv_results.setModel(model)
                self.tree.show_data(data['trades'])
                self.plot_data(data['data'])






