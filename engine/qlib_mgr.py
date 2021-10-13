import qlib
from qlib.config import REG_CN
class QlibMgr:
    def __init__(self):
        provider_uri = "../data/qlib_data/cn_data"  # target_dir
        qlib.init(provider_uri=provider_uri, region=REG_CN)


if __name__ == '__main__':
    QlibMgr()