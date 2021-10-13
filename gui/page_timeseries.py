import wx
from .panels.results import ResultsPanel
from .panels.actions import TimeSeriesPanel
from .global_event import g
class PageTimeSeries(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.init_ui()

    def init_ui(self):

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vbox)

        timeseries = TimeSeriesPanel(self)
        self.vbox.Add(timeseries, -1, wx.EXPAND)

        results = ResultsPanel(self)
        self.vbox.Add(results,-1,wx.EXPAND)
        g.add_observer(g.MSG_TYPE_SERIES, results)


        #colour = [(160, 255, 204), (153, 204, 255), (151, 253, 225), ]
        #self.SetBackgroundColour(colour[0])
        #self.tx1 = wx.StaticText(self, -1, "使用说明", (355, 45),
        #                            (100, -1), wx.ALIGN_CENTER)
        #font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD)
        #self.tx1.SetFont(font)