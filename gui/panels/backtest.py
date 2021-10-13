
import wx
from ...engine.runner import Runner
from ..global_event import g

class CreateStrategy(wx.Panel):
    def __init__(self,parent):
        super(CreateStrategy, self).__init__(parent)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(hbox)

        hbox.Add(wx.StaticText(self, -1, label='请输入基金代码：'), 0)
        self.codes = wx.TextCtrl(self,size=(300,60))
        self.codes.SetValue('510300.SH;510500.SH')
        hbox.Add(self.codes, 0, wx.ALL | wx.EXPAND, 5)

        #固定组合权重
        hbox.Add(wx.StaticText(self, -1, label='请输入权重（与基金数量一定，逗号分隔）：'), 0)
        self.weights = wx.TextCtrl(self, size=(300, 60))
        self.weights.SetValue('0.6,0.4')
        hbox.Add(self.weights, 0, wx.ALL | wx.EXPAND, 5)

        self.box = wx.CheckBox(self, -1, "全部基金",)  # 创建控件
        vbox.Add(self.box)
        self.Bind(wx.EVT_CHECKBOX, self.ChooseAll, self.box)  # 绑定事件
        self.box.SetValue(False)  # 设置当前是否被选中
        self.SetSizer(vbox)

        #===================各种策略==================




        self.btn_save = wx.Button(self,label='保存策略')
        self.Bind(wx.EVT_BUTTON,self.SaveClicked,self.btn_save)
        vbox.Add(self.btn_save)
        #dlg = wx.TextEntryDialog(self, 'Enter a URL', 'HTMLWindow')

    def SaveClicked(self,event):
        #wx.MessageBox('saved!')
        codes = self.codes.GetValue()
        if codes == '':
            wx.MessageBox('请输入基金代码！')
            self.codes.SetFocus()
            return
        codes = codes.split(';')
        weights = self.weights.GetValue().split(',')
        weights = [float(w) for w in weights]
        buy_rules = self.rule_buy.get_rules()
        sell_rules = self.rule_sell.get_rules()
        order_rules = self.rule_orderby.get_rules()
        print(buy_rules,sell_rules,order_rules)

        strategy = {
            'universe':codes,
            'weights': weights,
            'buy_rules':buy_rules,
            'sell_rules':sell_rules,
            'order_rules':order_rules
        }

        print(strategy)
        strategy['benchmarks'] = ['000300.SH']


    def ChooseAll(self,e):
        all = self.box.GetValue()
        if all:
            self.codes.Enabled = False
        else:
            self.codes.Enabled = True
