import wx,time
import webbrowser as web
from .page_timeseries import PageTimeSeries

class MainWindow(wx.Frame):
    def __init__(self):
        displaySize = wx.DisplaySize()  # (1920, 1080)
        displaySize = 0.85 * displaySize[0], 0.75 * displaySize[1]
        super().__init__(parent=None, title='AI量化投资平台', size=displaySize)
        self.init_statusbar()
        self.init_menu_bar()
        self.init_main_tabs()

    def init_main_tabs(self):
        #self.SetBackgroundColour(wx.GREEN)
        #创建水平boxsizer，并设置为平铺到整个窗口
        self.boxH = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.boxH)

        self.tabs = wx.Notebook(self)
        self.boxH.Add(self.tabs,1,wx.ALL | wx.EXPAND)#??todo propotion==1为何
        self.tabs.AddPage(PageTimeSeries(self.tabs),'时间序列分析')

    def on_menu(self,event):
        if event.Id == 1:
            web.open('https://danjuanapp.com/djmodule/value-center')
        if event.Id== 2:
            #self.l.load_data()
            web.open('https://www.jisilu.cn/')

    def init_menu_bar(self):
        # 创建窗口面板
        menuBar = wx.MenuBar(style=wx.MB_DOCKABLE)
        self.SetMenuBar(menuBar)

        files = wx.Menu()
        menuBar.Append(files, '&文件')

        tools = wx.Menu()
        menuBar.Append(tools, '&工具')

        help = wx.Menu()
        menuBar.Append(help, '&帮助')

        valuation = wx.MenuItem(tools, 1, '&蛋卷估值')
        tools.Append(valuation)
        self.Bind(wx.EVT_MENU, self.on_menu, valuation)

        tools.AppendSeparator()

        jisilu = wx.MenuItem(tools,2,'&集思录')
        tools.Append(jisilu)
        self.Bind(wx.EVT_MENU,self.on_menu,jisilu)

    def init_statusbar(self):
        self.statusBar = self.CreateStatusBar()  # 创建状态条
        # 将状态栏分割为3个区域,比例为2:1
        self.statusBar.SetFieldsCount(3)
        self.statusBar.SetStatusWidths([-2, -1, -1])
        t = time.localtime(time.time())
        self.SetStatusText("公众号：ailabx(七年实现财富自由)", 0)
        self.SetStatusText("当前版本：%s" % '1.0.0', 1)
        #self.SetStatusText(time.strftime("%Y-%B-%d %I:%M:%S", t), 2)

class MainApp(wx.App):
	def OnInit(self):
		frame = MainWindow()
		frame.Show(True)
		frame.Center()
		self.SetTopWindow(frame)
		return True

if __name__ == '__main__':
    app = MainApp()
    app.MainLoop()