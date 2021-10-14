import qlib
from qlib.config import REG_CN
from qlib.data import D

import sys
import codecs
print(sys.stdout.encoding)

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
class QlibMgr:
    def __init__(self):
        provider_uri = 'D:/008dev/ailabx/data/qlib_data/cn_data'#"../data/qlib_data/cn_data"  # target_dir
        qlib.init(provider_uri=provider_uri, region=REG_CN)

    def load_data(self):
        ret = D.calendar(start_time='2010-01-01', end_time='2017-12-31', freq='day')[:2]
        print(ret)

        instruments = D.instruments('csi300')# ['SH600570','SH600000']
        fields = ['$close', '$volume', 'Ref($close, 1)', 'Mean($close, 3)', '$high-$low']
        data = D.features(instruments, fields, start_time='2010-01-01', end_time='2017-12-31', freq='day')
        #print(type(data))
        #print(data.index)


if __name__ == '__main__':
    mgr = QlibMgr()
    mgr.load_data()