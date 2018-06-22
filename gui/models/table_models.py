from PyQt5.QtWidgets import QTableView,QApplication
from PyQt5.QtCore import Qt,QAbstractTableModel,QVariant
from PyQt5 import QtWidgets
import pandas as pd
import numpy as np
import sys
from PyQt5 import QtCore
from datetime import datetime

class DataFrameTableModel(QAbstractTableModel):
    def __init__(self,df,parent=None):
        super(DataFrameTableModel,self).__init__(parent)
        self.df = df

    def rowCount(self, QModelIndex):
        return len(self.df)

    def columnCount(self, QModelIndex):
        return len(self.df.columns)

    def sort(self, columnId, order=Qt.AscendingOrder):
        self.layoutAboutToBeChanged.emit()
        column = self.df.columns[columnId]
        #df = pd.DataFrame()
        self.df.sort_values(column, ascending=not bool(order), inplace=True)
        self.layoutChanged.emit()

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= QtCore.Qt.ItemIsEditable
        flags |= QtCore.Qt.ItemIsSelectable
        flags |= QtCore.Qt.ItemIsEnabled
        flags |= QtCore.Qt.ItemIsDragEnabled
        flags |= QtCore.Qt.ItemIsDropEnabled
        return flags

    def data(self, index, role):

        def convertValue(row, col, columnDtype):
            value = None
            if columnDtype == object:
                value = self._dataFrame.ix[row, col]
            elif columnDtype in self._floatDtypes:
                value = round(float(self._dataFrame.ix[row, col]), self._float_precisions[str(columnDtype)])
            elif columnDtype in self._intDtypes:
                value = int(self._dataFrame.ix[row, col])
                value = bool(self._dataFrame.ix[row, col])
            elif columnDtype in self._dateDtypes:
                value = pd.Timestamp(self._dataFrame.ix[row, col])
                value = QtCore.QDateTime.fromString(str(value), self.timestampFormat)
            return value

        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            result = self.df.ix[row, col]
            return str(result)

        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            try:
                label = self.df.columns.tolist()[section]
                if label == section:
                    label = section
                return label
            except (IndexError,):
                return None
        elif orientation == Qt.Vertical:
            return section

