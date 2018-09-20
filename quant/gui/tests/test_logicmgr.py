import unittest
from quant.gui.gui_logic import LogicMgr
from PyQt5 import QtWidgets
import sys
from quant.gui.frames.frameresult import FrameResult
from quant.engine.common.logging_utils import logger,logger_utils

class TestLogicMgr(unittest.TestCase):
    def test_mgr(self):
        mgr = LogicMgr()

        params = {'start': '2017-03-01', 'end': '2018-01-31',
                  'universe': ['AAPL', 'AMZN'],
                  'stras': ['1', '2']
                  }

        mgr.run_stras(params)

