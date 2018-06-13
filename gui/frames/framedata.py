from PyQt5 import QtWidgets

class FrameData(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(FrameData,self).__init__(parent=parent)

        vlayout = QtWidgets.QVBoxLayout(self)
        self.groupbox = QtWidgets.QGroupBox('数据文件：')
        vlayout.addWidget(self.groupbox)

        self.setLayout(vlayout)

        self.init_groupbox()

    def init_groupbox(self):
        grid = QtWidgets.QGridLayout()
        self.groupbox.setLayout(grid)
        grid.addWidget(QtWidgets.QLabel('请选择：'), 0, 0)

        self.text_file = QtWidgets.QTextEdit('请选择：')
        grid.addWidget(self.text_file, 0, 1)

        btn = QtWidgets.QPushButton('...')
        btn.clicked.connect(self.btn_sel_clicked)
        grid.addWidget(btn,0,2)

    def btn_sel_clicked(self):
        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "C:/",
                                                          "CSV文件 (.csv)")  # 设置文件扩展名过滤,注意用双分号间隔
        self.text_file.setText(filename)