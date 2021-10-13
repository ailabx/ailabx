import wx

class RuleMgr(wx.Panel):
    def __init__(self,parent):
        super(RuleMgr, self).__init__(parent)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        #self.list = wx.ListCtrl(self)
        self.list = wx.ListBox(self, -1,size=(200,80), choices=[], style=wx.LB_SINGLE | wx.LB_HSCROLL | wx.LB_ALWAYS_SB | wx.LB_SORT)
        hbox.Add(self.list)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(vbox)

        btn_add = wx.Button(self,label='添加')
        self.Bind(wx.EVT_BUTTON,self.add,btn_add)
        btn_modify = wx.Button(self, label='修改')
        self.Bind(wx.EVT_BUTTON, self.modify, btn_modify)
        btn_del = wx.Button(self,label='删除')
        self.Bind(wx.EVT_BUTTON, self.delete, btn_del)

        vbox.Add(btn_add)
        vbox.Add(btn_modify)
        vbox.Add(btn_del)

        self.SetSizer(hbox)

    def get_rules(self):
        return self.list.GetStrings()

    def add(self,event):
        dlg = wx.TextEntryDialog(None, u"请在下面文本框中输入规则:", "请输入规则", "MOM(20)>0.02")
        if dlg.ShowModal() == wx.ID_OK:
            value = dlg.GetValue()  # 获取文本框中输入的值
            self.list.Append(value)
            #self.list.Insert(0,message)

    def modify(self,event):
        item = self.list.GetSelections()[0]
        value = self.list.GetStrings()[item]
        dlg = wx.TextEntryDialog(None, u"请在下面文本框中输入规则:", "请输入规则", value)
        if dlg.ShowModal() == wx.ID_OK:
            deleted_item = self.list.GetSelection()
            self.list.Delete(deleted_item)

            value = dlg.GetValue()  # 获取文本框中输入的值
            self.list.Append(value)

    def delete(self,event):
        deleted_item = self.list.GetSelection()
        self.list.Delete(deleted_item)


class ActionRollingPanel(wx.Panel):
    def __init__(self,parent):
        super(ActionRollingPanel, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(hbox)
        vbox.Add(hbox2)

        hbox.Add(wx.StaticText(self, -1, label='请输入基金代码：'), 0)
        self.codes = wx.TextCtrl(self, size=(300, 60))
        self.codes.SetValue('510300.SH;510500.SH')
        hbox.Add(self.codes, 0, wx.ALL | wx.EXPAND, 5)

        gs = wx.GridSizer(1, 3, 5, 5)
        vbox.Add(gs, 0, wx.EXPAND)

        rule_buy = RuleMgr(self)
        rule_sell = RuleMgr(self)
        rule_orderby = RuleMgr(self)
        # vbox.Add(rule_buy)
        gs.Add(rule_buy, 0, wx.EXPAND)
        gs.Add(rule_sell, 0, wx.EXPAND)
        gs.Add(rule_orderby, 0, wx.EXPAND)
        self.rule_buy = rule_buy
        self.rule_sell = rule_sell
        self.rule_orderby = rule_orderby