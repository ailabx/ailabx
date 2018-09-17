from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import QtCore
import os

from ..models import table_models
import pandas as pd
from ...engine.common.logging_utils import logger

from PyQt5.uic import loadUi
from datetime import datetime
from datetime import timedelta
import traceback

from ...engine.consts import *

import matplotlib.pyplot as plt

class FrameBacktest(QtWidgets.QWidget):
    def __init__(self,logic,parent=None):
        super(FrameBacktest,self).__init__(parent=parent)
        current_path = os.path.abspath(__file__)
        father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
        father_path = os.path.abspath(os.path.dirname(father_path) + os.path.sep + ".")
        file = father_path + '/ui/backtest_config.ui'
        loadUi(file, self)

        self.logic = logic
        self.logic.signal.connect(self.on_events)


        #combo = self.combo_strats
        #combo.addItems(['买入并持有','随机买卖','海龟交易原则','深度强化学习'])

        self.btn_backtest.clicked.connect(self.bkt_clicked)
        self.show_data()

    def show_data(self):
        for k,v in benchmark_types.items():
            self.combo_benchmark.addItems([v,])

    def check_data(self):
        logger.info('检查回测数据是否正确...')
        if hasattr(self.logic,'frame_symbols'):
            data = self.logic.frame_symbols.get_data()

        init_cash = self.edit_init_cash.text()
        max_hold = self.box_max_hold.value()
        bench_type = self.combo_benchmark.currentText()
        bench_type = get_type_by_text(benchmark_types,bench_type)
        try:
            init_cash = int(init_cash)
        except:
            logger.info('初始资金请输入整数。')
            self.edit_init_cash.setFocus()
            init_cash = 100000
            return False
        date_start = self.dt_start.date()
        date_end = self.dt_end.date()
        if date_end <= date_start:
            logger.info('开始时间需小于结束时间。')
            return False
        #print(type(date_start))
        data = {'init_cash':init_cash,'max_hold':max_hold,'bench_type':bench_type,
                'start':date_start.toString(QtCore.Qt.ISODate),
                'end':date_end.toString(QtCore.Qt.ISODate)}
        print(data)
        return True

    def bkt_clicked(self):
        try:
            if self.check_data():
                self.logic.run()
        except:
            traceback.print_exc()

    def on_events(self,data):
        if data and 'event_type' in data:
            type = data['event_type']
            if type == EventType.onstart:
                pass
                #self.btn_backtest.enabled=False
            elif type == EventType.onfinished:
                pass
 #               self.btn_backtest.enabled = True
        #print('BKT_ONEVENTs',data)



