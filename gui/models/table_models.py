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
        #self.sortingAboutToStart.emit()
        column = self.df.columns[columnId]
        #df = pd.DataFrame()
        self.df.sort_values(column, ascending=not bool(order), inplace=True)
        self.layoutChanged.emit()
        #self.sortingFinished.emit()
        #pass

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
            elif columnDtype in self._boolDtypes:
                # TODO this will most likely always be true
                # See: http://stackoverflow.com/a/715455
                # well no: I am mistaken here, the data is already in the dataframe
                # so its already converted to a bool
                value = bool(self._dataFrame.ix[row, col])

            elif columnDtype in self._dateDtypes:
                # print numpy.datetime64(self._dataFrame.ix[row, col])
                value = pd.Timestamp(self._dataFrame.ix[row, col])
                value = QtCore.QDateTime.fromString(str(value), self.timestampFormat)
                # print value
            # else:
            #     raise TypeError, "returning unhandled data type"
            return value

        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            #columnDtype = self.df.icol(col).dtype

            result = self.df.ix[row, col]
            return str(result)

        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """return the header depending on section, orientation and Qt::ItemDataRole
        Args:
            section (int): For horizontal headers, the section number corresponds to the column number.
                Similarly, for vertical headers, the section number corresponds to the row number.
            orientation (Qt::Orientations):
            role (Qt::ItemDataRole):
        Returns:
            None if not Qt.DisplayRole
            _dataFrame.columns.tolist()[section] if orientation == Qt.Horizontal
            section if orientation == Qt.Vertical
            None if horizontal orientation and section raises IndexError
        """
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

