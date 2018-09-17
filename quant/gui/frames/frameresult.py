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

    def init_visual(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.layout = QtWidgets.QVBoxLayout(self.visual_widget)
        self.layout.addWidget(self.canvas)


    def plot_data(self,data):
        #df = pd.DataFrame(index=pd.date_range('2010-01-01', periods=5), columns=['aapl'], data=5)
        data.plot(ax=self.ax)
        plt.show()


    def on_events(self,data):
        pass
        if data and 'event_type' in data.keys():
            type = data['event_type']
            if type ==  EventType.onmessage:
                try:
                    print(data['msg'])
                    #self.edit_result.append(data['msg'])
                except:
                    traceback.print_exc()
            #elif type == EventType.EventType_BacktestFinished:
            #    self.plot_data()







