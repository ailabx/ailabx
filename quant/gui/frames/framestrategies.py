from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
import os
from PyQt5.uic import loadUi
from ...engine.common.logging_utils import logger
from ...engine.consts import EventType
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



        self.btn_backtest.clicked.connect(self.backtest)
        self.btn_remove.clicked.connect(self.remove)
        self.btn_modify.clicked.connect(self.modify)

        self.load_stras()

    def modify(self):
        pass

    def load_stras(self):
        self.lv_stras.clear()
        #self.lv_stras.items.clear()
        #count = self.lv_stras.count()
        #for i in range(0,count):
        #    item = self.lv_stras.takeItem(i)
        #    del item

        stras = self.mgr.jobmgr.stras
        for stra in stras:
            item = QtWidgets.QListWidgetItem(stra['name'])
            item.setData(Qt.UserRole, stra)
            self.lv_stras.addItem(item)

    def remove(self):
        items = self.lv_stras.selectedItems()
        if len(items) == 0:
            reply = QMessageBox.information(self,  # 使用infomation信息框
                                            "提示",
                                            '请至少选择一个策略！')
            return
        else:
            reply = QMessageBox.information(self,  # 使用infomation信息框
                                            "提示",
                                            '确认要删除{}个策略！'.format(len(items)),QMessageBox.Yes|QMessageBox.No)

            if reply == QMessageBox.No:
                return

        for item in items:
            try:
                stra = item.data(Qt.UserRole)
                self.mgr.jobmgr.remove_stra(stra['job_id'])
            except:
                traceback.print_exc()

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
        if data:
            event = data['event_type']
            if event == EventType.on_stras_changed:
                self.load_stras()
