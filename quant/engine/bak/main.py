import sys,os
import xmlrpc
from xmlrpc.server import SimpleXMLRPCServer
from quant.webui.webapp import run_webui,run_flask
from quant.engine.backtest import BacktestRunner
class RPCService:
  def list(self, dir_name):
    return os.listdir(dir_name)

  def echo(self,message):
      print(message)
      return 'server'+message

  def start_stras(self,ids):
      ids = ids.split(',')
      print('要启动任务，任务信息',ids)
      params = {'start': '2017-03-01', 'end': '2018-01-31',
                'universe': ['AAPL', 'AMZN'],
                'stras': ['1', '2']
                }
      BacktestRunner().run_backtests(params)

      return 'Done'

def rpc_run():
    server = SimpleXMLRPCServer(('localhost', 9000), logRequests=True)
    server.register_instance(RPCService())
    try:
        print('输入 Control - C to exit')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Exiting')

def run_in_thread(func, *args, **kwargs):
    """Run function in thread, return a Thread object"""
    from threading import Thread
    thread = Thread(target=func, args=args, kwargs=kwargs)
    thread.daemon = True
    thread.start()
    return thread

if __name__ == '__main__':
    run_in_thread(rpc_run)

    print('starting flask')
    run_flask()
    #run_webui()


'''
from PyQt5 import QtWidgets
from quant.gui.mainwindow import MainWindow

=
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.showMaximized()

    with open(os.getcwd() + '/quant/gui/ui/style.qss', 'r') as q:
        app.setStyleSheet(q.read())

    app.exec_()
'''