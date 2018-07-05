import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

logger = logging.getLogger(__file__)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('logger.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)