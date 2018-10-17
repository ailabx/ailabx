import logging,sys
from logging import Handler

class LogHandler(Handler):
    def __init__(self, func = None):
        Handler.__init__(self)
        self.func = func

    def emit(self, record):
        """
        Emit a record.
        """
        try:
            msg = self.format(record)
            if self.func:
                self.func(msg)
        except Exception:
            self.handleError(record)


class LoggerUtils(object):
    def __init__(self):
        log = LogHandler(self.onmsg)

        logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter(
            '[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')
        log.setFormatter(formatter)



        self.logger = logging.getLogger(__file__)
        self.logger.addHandler(log)

        self.signal = None


    def onmsg(self,msg):
        if self.signal:
            pass
            #self.signal.emit({'event_type':EventType.onmessage,'msg':msg})

logger_utils = LoggerUtils()
logger = logger_utils.logger
