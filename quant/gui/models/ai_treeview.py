from PyQt5.QtWidgets import QTreeWidget,QTreeWidgetItem

class AiTreeView(QTreeWidget):
    def __init__(self,parent=None):
        super(AiTreeView,self).__init__(parent)

    def show_data(self,data):
        self.data = data
        self.init_ui()

    def init_ui(self):
        roots = []
        for name,df in self.data.items():
            self.setColumnCount(len(df.columns))
            self.setHeaderLabels(list(df.columns))

            root = QTreeWidgetItem()
            root.setText(0,name)

            for i in range(len(df)):
                child = QTreeWidgetItem(root)
                for j in range(len(df.columns)):
                    child.setText(j,str(df.iloc[i][j]))

            roots.append(root)

        self.insertTopLevelItems(0,roots)