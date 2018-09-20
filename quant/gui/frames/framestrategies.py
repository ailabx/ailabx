from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
import os
from PyQt5.uic import loadUi
from ...engine.common.logging_utils import logger
import traceback

class FrameStrategies(QtWidgets.QWidget):
    def __init__(self,logic,parent=None):
        super(FrameStrategies,self).__init__(parent)

        current_path = os.path.abspath(__file__)
        father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
        father_path = os.path.abspath(os.path.dirname(father_path) + os.path.sep + ".")
        file = father_path + '/ui/strategies.ui'
        loadUi(file,self)

        self.mgr = logic
        logic.frame_symbols = self
        logic.signal.connect(self.on_events)

        #初始化数据

        stras = logic.jobmgr.get_stras()
        for stra in stras:
            item = QtWidgets.QListWidgetItem(stra['name'])
            item.setData(Qt.UserRole,stras)
            self.lv_stras.addItem(item)

        self.btn_backtest.clicked.connect(self.backtest)

    def backtest(self):
        items = self.lv_stras.selectedItems()
        if len(items) == 0:
            reply = QMessageBox.information(self,  # 使用infomation信息框
                                           "提示",
                                           '请至少选择一个策略！')
            return
        else:
            logger.info('您选择了{}个策略。'.format(len(items)))

        for item in items:
            try:
                print(item.data(Qt.UserRole))
            except:
                traceback.print_exc()

        params = {'start': '2017-03-01', 'end': '2018-01-31',
                  'universe': ['AAPL', 'AMZN'],
                  'stras': ['1', '2']
                  }

        try:
            self.mgr.run_stras(params)
        except:
            traceback.print_exc()


    def get_data(self):
        text = self.edit_symbols.toPlainText()
        symbols = text.split('\n')
        logger.info(symbols)

    def on_events(self,data):
        pass
