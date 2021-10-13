import wx,wx.adv
from .. import widgets
from ...dataloader.dataloader import CSVLoader
from ...dataloader.pd_utils import PdUtils
from ...analysis.performance import PerformanceUtils
import os
import pandas as pd

class TimeSeriesAnalysis(wx.Panel):
    def __init__(self,parent):
        super(TimeSeriesAnalysis, self).__init__(parent)
        #self.SetBackgroundColour('green')

        vbox = wx.BoxSizer(wx.VERTICAL)
        # 水平盒子
        hbox = wx.BoxSizer(wx.HORIZONTAL)


        self.text_codes = wx.TextCtrl(self, -1, size=(200, 20), style=wx.ALIGN_LEFT)
        self.text_codes.SetValue('000300.SH;000905.SH')
        hbox.Add(wx.StaticText(self, -1, label="代码："), 0, wx.ALL | wx.EXPAND, 5)
        hbox.Add(self.text_codes, 0, wx.ALL | wx.EXPAND, 5)

        # 创建按钮
        self.btn_ana = wx.Button(self, label="分析")
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.btn_ana)
        # 在水平盒子里添加查询按钮
        hbox.AddSpacer(20)
        hbox.Add(self.btn_ana, 0)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        self.date_start = wx.adv.DatePickerCtrl(self, id = -1,style=wx.adv.DP_DROPDOWN|wx.adv.DP_SHOWCENTURY)
        self.date_end = wx.adv.DatePickerCtrl(self, id=-1, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        hbox2.Add(wx.StaticText(self,-1,label='起始时间：'),0)
        hbox2.Add(self.date_start, 5)
        hbox2.Add(wx.StaticText(self, -1, label='结束时间：'), 0)
        hbox2.Add(self.date_end, 5)
        hbox2.Add(wx.StaticText(self, -1, label='基准：'), 0)
        # 创建下拉框
        self.languages = ['沪深300', '中证500', '中证800', '创业板']
        self.choice = self.languages[0]
        self.combo = wx.ComboBox(self, choices=self.languages, value=self.languages[0])
        # 在水平盒子添加下拉框
        hbox2.Add(self.combo, 5)

        hbox2.Add(wx.StaticText(self, -1, label='策略：'), 0)
        self.strategies = ['大小盘轮动', '中证500', '中证800', '创业板']
        #self.choice = self.languages[0]
        self.combo_strategy = wx.ComboBox(self, choices=self.strategies, value=self.strategies[0])
        # 在水平盒子添加下拉框
        hbox2.Add(self.combo_strategy, 5)
        # 创建按钮
        self.btn_bkt = wx.Button(self, label="开始回测")
        self.Bind(wx.EVT_BUTTON, self.OnClickBkt, self.btn_bkt)
        hbox2.Add(self.btn_bkt, 5)

        self.btn_create = wx.Button(self, label='新建策略')
        self.Bind(wx.EVT_BUTTON, self.OnClickCreate, self.btn_create)
        hbox2.Add(self.btn_create, 5)


        # 在垂直盒子里添加水平盒子
        vbox.Add(hbox, 0, wx.ALL, 5)
        vbox.Add(hbox2, 0, wx.ALL, 5)

        self.init_cmd(self,vbox)


        self.SetSizer(vbox)

    def init_cmd(self,parent,vbox):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(hbox, 0, wx.ALL, 5)

        #self.date_start = wx.DatePickerCtrl(self)
        #hbox.Add(self.date_start, 1, wx.EXPAND | wx.ALL, 5)




    def OnClickBkt(self,event):
        wx.MessageBox('开始回测！')

    def OnClickCreate(self,event):
        wx.MessageBox('开始创建！')

    def OnClick(self,event):
        codes = self.text_codes.GetValue()
        codes = codes.split(';')
        path = os.path.abspath(os.path.dirname(os.getcwd())+os.path.sep+"datas")
        CSVLoader.check_and_load(codes,path)
        dfs = CSVLoader.load_csvs(path,codes)

        df_prices = PdUtils.dfs_to_prices(dfs)

        date_start = self.date_start.GetValue()
        date_start = pd.Timestamp(_wxdate2pydate(date_start))
        date_end = self.date_end.GetValue()
        date_end = pd.Timestamp(_wxdate2pydate(date_end))

        #df_prices = df_prices[df_prices.index > date_start]
        df_prices = df_prices[df_prices.index < date_end]

        for col in df_prices.columns:
            df_prices[col] = df_prices[col].pct_change()

        df_equity = PerformanceUtils().rate2equity(df_prices)
        df_ratios,df_corr,df_years = PerformanceUtils().calc_rates(df_prices)
        print(df_ratios,df_corr,df_years)
        self.pd.show_df(df_ratios)
        self.pd_yearly.show_df(df_years)
        self.pd_corr.show_df(df_corr)
        self.plot.show_data(df_equity)
