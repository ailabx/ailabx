import unittest
from quant.gui.gui_logic import JobMgr

class TestJobMgr(unittest.TestCase):
    def test_jobmgr(self):
        mgr = JobMgr()
        #self.assertEqual(2,len(mgr.stras))

        print(mgr.stras)
        stra = mgr.stras[0].copy()
        stra['job_id'] = '012222'

        mgr.update_sert_stra(stra)

        #mgr.remove_stra('1')
        print(mgr.stras)