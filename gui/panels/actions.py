import wx,os,wx.adv
#from .backtest import CreateStrategy
#import pandas as pd
#from datax.data_loader import load_codes,merge_dfs,dfs2rate
#from ...datax.data_loader import PdUtils
#from datax.performance import PerformanceUtils
from .. import gui_utils
import pandas as pd
#from ...engine.runner import Runner
from .action_rolling import ActionRollingPanel

from ..global_event import g

class BacktestPanel(wx.Panel):
    def __init__(self,parent):
        super(BacktestPanel, self).__init__(parent)
        self.init_ui()
    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(hbox,0,wx.ALL,5)

        self.date_start = wx.adv.DatePickerCtrl(self, id=-1, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        self.date_start.SetValue(wx.DateTime.FromDMY(1, 1, 2005))
        self.date_end = wx.adv.DatePickerCtrl(self, id=-1, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        hbox.Add(wx.StaticText(self, -1, label='起始时间：'), 0)
        hbox.Add(self.date_start, 5)
        hbox.AddSpacer(20)
        hbox.Add(wx.StaticText(self, -1, label='结束时间：'), 0)
        hbox.Add(self.date_end, 5)
        self.btn = wx.Button(self, label="回测")
        hbox.Add(self.btn,0)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.btn)

    def add_callback(self,o):
        self.callback = o

    def OnClick(self,event):
        if self.callback:
            date_start = self.date_start.GetValue()
            date_start = gui_utils._wxdate2pydate(date_start)
            date_start = date_start.strftime('%Y%m%d')
            date_end = self.date_end.GetValue()
            date_end = gui_utils._wxdate2pydate(date_end)
            date_end = date_end.strftime('%Y%m%d')
            self.callback.onclick(date_start,date_end)

class TimeSeriesPanel(wx.Panel):
    def __init__(self,parent):
        super(TimeSeriesPanel, self).__init__(parent)
        #self.SetMaxSize((2,100))
        self.init_ui()

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)
        # 水平盒子
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.text_codes = wx.TextCtrl(self, -1, size=(200, 20), style=wx.ALIGN_LEFT)
        self.text_codes.SetValue('000300.SH;000905.SH')
        hbox.Add(wx.StaticText(self, -1, label="代码："), 0, wx.ALL | wx.EXPAND, 5)
        hbox.Add(self.text_codes, 0, wx.ALL | wx.EXPAND, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        self.date_start = wx.adv.DatePickerCtrl(self, id=-1, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        self.date_start.SetValue(wx.DateTime.FromDMY(1,1,2005))
        self.date_end = wx.adv.DatePickerCtrl(self, id=-1, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        hbox2.Add(wx.StaticText(self, -1, label='起始时间：'), 0)
        hbox2.Add(self.date_start, 5)

        hbox2.AddSpacer(20)

        hbox2.Add(wx.StaticText(self, -1, label='结束时间：'), 0)
        hbox2.Add(self.date_end, 5)

        # 创建按钮
        self.btn_ana = wx.Button(self, label="分析")
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.btn_ana)
        # 在水平盒子里添加查询按钮
        hbox2.AddSpacer(20)
        hbox2.Add(self.btn_ana, 0)

        vbox.Add(hbox, 0, wx.ALL, 5)
        vbox.Add(hbox2, 0, wx.ALL, 5)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(hbox3,0,wx.ALL,5)

        self.btn_indicator = wx.Button(self, label="指标可视化")
        hbox3.Add(wx.StaticText(self, -1, label='请选择指标：'), 0)
        combo = wx.ComboBox(self, -1, pos=(50, 170), size=(150, -1),
                            choices=['RSRS','标准RSRS'], style=wx.CB_READONLY)
        hbox3.Add(combo, 1)
        hbox3.Add(self.btn_indicator,1)
        self.Bind(wx.EVT_BUTTON, self.OnClick_indicator, self.btn_indicator)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(hbox4, 0, wx.ALL, 5)

        self.btn_load = wx.Button(self, label="加载数据")
        self.btn_feature = wx.Button(self, label="特征提取")
        hbox4.Add(self.btn_load,1)
        hbox4.Add(self.btn_feature,2)

        self.Bind(wx.EVT_BUTTON, self.on_load, self.btn_load)
        self.Bind(wx.EVT_BUTTON, self.on_feature, self.btn_feature)

    def OnClick_indicator(self,event):
        pass

    def on_feature(self):
        pass

    def on_load(self,event):
        codes = self.text_codes.GetValue()
        codes = codes.split(';')
        #path = os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep + "datas")
        dfs = load_codes(codes)
        df_all = merge_dfs(dfs)
        print(df_all)
        self.df = df_all

        g.notify(g.MSG_TYPE_SERIES, {
            'raw': df_all,
            #'corr': df_corr,
            #'plot': df_equity,
            #'yearly': df_years
        })


    def OnClick(self,event):
        codes = self.text_codes.GetValue()
        codes = codes.split(';')

        date_start = self.date_start.GetValue()
        date_start = gui_utils._wxdate2pydate(date_start)
        date_start = date_start.strftime('%Y%m%d')
        date_end = self.date_end.GetValue()
        date_end = gui_utils._wxdate2pydate(date_end)
        date_end = date_end.strftime('%Y%m%d')

        dfs = load_codes(codes)
        print(dfs)
        df_all = merge_dfs(dfs)
        print(df_all)
        df_rates = dfs2rate(df_all)
        print(df_rates)



        #df_prices = df_prices[df_prices.index > date_start]
        df_rates.dropna(inplace=True)
        df_rates = df_rates[date_start:date_end]

        #for col in df_prices.columns:
        #    df_prices[col] = df_prices[col].pct_change()

        df_equity = PerformanceUtils().rate2equity(df_rates)
        df_ratios,df_corr,df_years = PerformanceUtils().calc_rates(df_rates)

        g.notify(g.MSG_TYPE_SERIES,{
            'ratio':df_ratios,
            'corr':df_corr,
            'plot':df_equity,
            'yearly':df_years
        })

class PortfolioPanel(wx.Panel):
    def __init__(self,parent):
        super(PortfolioPanel,self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(hbox)
        #vbox.Add(hbox2)

        hbox.Add(wx.StaticText(self, -1, label='请输入策略代码：'), 0)
        self.codes = wx.TextCtrl(self, size=(300, 200),style=wx.TE_MULTILINE)
        self.codes.SetValue('''
        {
            'universe': ['510300.SH', '159915.SZ'],
            'benchmarks': ['510300.SH','159915.SZ'],
            'factors': [('mom_20', 'Mom($close,20)'), ('buy_1', '$mom_20>0.02'), ('sell_1', '$mom_20<0')],
            'factors_date': [('rank', 'Rank($mom_20)')],
            'buy': (['buy_1'], 1),
            'sell': (['sell_1'], 1),
            'order_by': ('rank', 2)  # 从大到小，取前2
        }
        ''')
        hbox.Add(self.codes)

        btn = wx.Button(self,-1,label='回测')
        hbox.Add(btn,0)
        self.Bind(wx.EVT_BUTTON,self.onclick,btn)
        '''
        
        hbox.Add(self.codes, 0, wx.ALL | wx.EXPAND, 5)        # 固定组合权重
        hbox.Add(wx.StaticText(self, -1, label='请输入权重（与基金数量一定，逗号分隔）：'), 0)
        self.weights = wx.TextCtrl(self, size=(300, 60))
        self.weights.SetValue('0.6,0.4')
        hbox.Add(self.weights, 0, wx.ALL | wx.EXPAND, 5)

        bkt = BacktestPanel(self)
        hbox2.Add(bkt, 0)
        bkt.add_callback(self)
        '''

    def onclick(self,event):
        codes = self.codes.GetValue()
        if codes == '':
            wx.MessageBox('请输入策略代码！')
            self.codes.SetFocus()
            return

        strategy = eval(codes.strip())
        print(strategy)

        #print(strategy)
        #strategy['benchmarks'] = ['000300.SH']

        df_ratios, df_corr, df_years, df_equities = Runner().run(strategy)
        g.notify(g.MSG_TYPE_SERIES, {
            'ratio': df_ratios,
            'corr': df_corr,
            'plot': df_equities,
            'yearly': df_years
        })



class ActionsPanel(wx.Panel):
    def __init__(self,parent):
        super(ActionsPanel, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        self.tabs = wx.Notebook(self)
        self.ana = TimeSeriesPanel(self.tabs)
        self.tabs.AddPage(self.ana, "分析&回测")
        self.tabs.AddPage(PortfolioPanel(self.tabs), "资产配置策略")
        #self.tabs.AddPage(ActionRollingPanel(self.tabs),'资产轮动策略')

        vbox.Add(self.tabs, 1, flag=wx.EXPAND | wx.ALL, border=5)