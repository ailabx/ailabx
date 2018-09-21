from PyQt5 import QtWidgets
import os
from PyQt5.uic import loadUi
from ...engine.common.logging_utils import logger
from ...engine import consts

class FrameTrade(QtWidgets.QDialog):
    def __init__(self,logic,parent=None):
        super(FrameTrade,self).__init__(parent)

        current_path = os.path.abspath(__file__)
        father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
        father_path = os.path.abspath(os.path.dirname(father_path) + os.path.sep + ".")
        file = father_path + '/ui/trade_rules.ui'
        loadUi(file,self)

        self.setWindowTitle('策略编辑器')

        self.mgr = logic
        logic.frame_trade = self
        logic.signal.connect(self.on_events)

        self.show_data(self.mgr.jobmgr.stras[0])

    def show_data(self,stra):
        self.edit_name.setText(stra['name'])
        self.edit_desc.setText(stra['desc'])

        mkts = consts.market_types.values()
        self.combo_market.addItems(mkts)
        #self.combo_market = QtWidgets.QComboBox()
        self.combo_market.setCurrentText(consts.market_types[stra['pick_symbols']['market']])

        allocs = consts.alloc_funds_types.values()
        self.combo_allocs.addItems(allocs)
        self.combo_allocs.setCurrentText(consts.alloc_funds_types[stra['alloc_funds']])
        #self.edit_symbols = QtWidgets.QTextEdit()

        universe = stra['pick_symbols']['universe']
        universe_text = '\n'.join(universe)
        self.edit_symbols.setText(universe_text)

        self.edit_long.setText(stra['pick_time']['long'])
        self.edit_flat.setText(stra['pick_time']['flat'])
    def on_events(self,data):
        pass
