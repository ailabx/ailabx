from PyQt5 import QtWidgets
import unittest,sys
import pandas as pd

from ..models.ai_treeview import AiTreeView

class TestTreeView(unittest.TestCase):
    def test_treeview(self):
        app = QtWidgets.QApplication(sys.argv)
        tree = AiTreeView()

        sig = pd.DataFrame(index=pd.date_range('2010-01-01', periods=5), columns=['交易','日期'])
        sig['日期'] = sig.index
        sig['交易'] = [0, 0, 1, -1, 0]

        print(sig)

        df = sig[['日期','交易']]
        tree.show_data({'stra1':df,'stra2':df})
        tree.show()
        app.exec_()
