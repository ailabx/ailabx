import wx.grid

class RuleGrid(wx.grid.Grid):
    def __init__(self,parent):
        super(RuleGrid, self).__init__(parent,-1)

    def add_row(self):
        wx.grid.GridTableMessage(self,
                             wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED
        , 1#插入一行记录
        )

    def del_row(self,index):
        wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,
                             index, #改行所在的索引
        1#只删除一行
        )


class PandasGrid(wx.grid.Grid):
    def __init__(self,parent,nrow=10,ncol=20):
        super().__init__(parent,-1)
        self.CreateGrid(numRows=nrow, numCols=ncol)

    def show_df(self,df):
        self.ClearGrid()
        self.df = df

        self.SetRowSize(0, 60)
        self.SetColSize(0, 150)

        for i,col in enumerate(list(df.columns)):
            self.SetColLabelValue(i,col)

        for i,row in enumerate(list(df.index)):
            self.SetRowLabelValue(i, row)

        i = 0
        for index, row in df.iterrows():
            for j in range(len(row)):
                self.SetCellValue(i,j,str(row[j]))
            i += 1

import wx

import matplotlib
matplotlib.use("WXAgg")
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

class MatplotlibPanel(wx.Panel):
    def __init__(self,parent,id=-1):
        super(MatplotlibPanel, self).__init__(parent,id)

        self.TopBoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.TopBoxSizer)

        self.figure = matplotlib.figure.Figure(figsize=(4, 3))
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.TopBoxSizer.Add(self.canvas, proportion=-10, border=2, flag=wx.ALL | wx.EXPAND)

    def show_data(self,data):
        #print(data)
        self.ax.clear()
        data.plot(ax=self.ax)
        self.ax.grid(True)
        self.canvas.draw()


if __name__ == '__main__':
    import pandas as pd
    app = wx.App()
    fr = wx.Frame(None)
    df = pd.DataFrame([['a1', 1], ['a2', 4]], columns=['uid', 'score'])
    grid = PandasGrid(fr)
    grid.show_df(df)
    fr.Show()
    app.MainLoop()
