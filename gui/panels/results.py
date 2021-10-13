import wx
from .. import widgets
class ResultsPanel(wx.Panel):
    def __init__(self,parent):
        super(ResultsPanel, self).__init__(parent)
        self.init_tabs()

    def handle_data(self,data_dict):
        if 'raw' in data_dict.keys():
            raw = data_dict['raw']
            self.panel_raw.show_df(raw)

        if 'ratio' in data_dict.keys():
            radio = data_dict['ratio']
            self.pd.show_df(radio)

        if 'corr' in data_dict.keys():
            corr = data_dict['corr']
            self.pd_corr.show_df(corr)

        if 'plot' in data_dict.keys():
            plot = data_dict['plot']
            self.plot.show_data(plot)

        if 'yearly' in data_dict.keys():
            yearly = data_dict['yearly']
            self.pd_yearly.show_df(yearly)



        #self.pd.show_df()

    def init_tabs(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        tabs = wx.Notebook(self)
        vbox.Add(tabs, 1, wx.EXPAND)

        self.panel_raw = widgets.PandasGrid(tabs)

        panel_tab = wx.Panel(tabs)
        panel_yearly = wx.Panel(tabs)
        panel_corr = wx.Panel(tabs)
        panel_plot = wx.Panel(tabs)

        tabs.AddPage(self.panel_raw,'原始数据')
        tabs.AddPage(panel_plot, '序列绘图')
        tabs.AddPage(panel_tab, '风险收益')
        tabs.AddPage(panel_yearly, '年度收益')
        tabs.AddPage(panel_corr, '相关性分析')

        self.pd = widgets.PandasGrid(panel_tab)
        self.pd_yearly = widgets.PandasGrid(panel_yearly)

        vbox_panel = wx.BoxSizer(wx.VERTICAL)
        vbox_panel.Add(self.pd, 1, wx.EXPAND)

        vbox_yearly = wx.BoxSizer(wx.VERTICAL)
        vbox_yearly.Add(self.pd_yearly, 1, wx.EXPAND)
        panel_tab.SetSizer(vbox_panel)
        panel_yearly.SetSizer(vbox_yearly)

        self.init_corr(panel_corr)
        self.init_plot(panel_plot)


    def init_corr(self,parent):
        vbox = wx.BoxSizer(wx.VERTICAL)
        parent.SetSizer(vbox)
        self.pd_corr = widgets.PandasGrid(parent)
        vbox.Add(self.pd_corr,1,wx.EXPAND)

    def init_plot(self,parent):
        vbox = wx.BoxSizer(wx.VERTICAL)
        parent.SetSizer(vbox)
        self.plot = widgets.MatplotlibPanel(parent)
        vbox.Add(self.plot, 1, wx.EXPAND)