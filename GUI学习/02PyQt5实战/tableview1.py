import sys
from PyQt5.QtCore import (Qt, QAbstractTableModel, QModelIndex, QVariant)
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QItemDelegate, QCheckBox, QTableView, QWidget)


class MyModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(MyModel, self).__init__(parent)

    def rowCount(self, QModelIndex):
        return 4

    def columnCount(self, QModelIndex):
        return 3

    def data(self, index, role):
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole:
            return 'Row %d, Column %d' % (row + 1, col + 1)
        return QVariant()

class MyButtonDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(MyButtonDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            button_read = QCheckBox('得电')
            button_read.setTristate(True)
            button_read.setCheckState(Qt.PartiallyChecked)
            button_read.index = [index.row(), index.column()]
            button_read.stateChanged.connect(lambda: self.btn_state(button_read.index))
            h_box_layout = QHBoxLayout()
            h_box_layout.addWidget(button_read)
            h_box_layout.setContentsMargins(0, 0, 0, 0)
            h_box_layout.setAlignment(Qt.AlignCenter)
            widget = QWidget()
            widget.setLayout(h_box_layout)
            self.parent().setIndexWidget(index, widget)

    def btn_state(self, btn):
        print(myModel.data(myModel.index(btn[0], btn[1]), Qt.EditRole))
        # print(myModel.item(btn[0], btn[1])).data(Qt.PartiallyChecked)


class MyTableView(QTableView):
    def __init__(self, parent=None):
        super(MyTableView, self).__init__(parent)
        self.setItemDelegateForColumn(0, MyButtonDelegate(self))


if __name__ == '__main__':
    a = QApplication(sys.argv)
    tableView = MyTableView()
    myModel = MyModel()
    tableView.setModel(myModel)
    print(myModel.data(myModel.index(0, 0), Qt.AccessibleDescriptionRole))
    tableView.show()
    a.exec_()
