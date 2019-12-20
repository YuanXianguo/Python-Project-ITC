import sys
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QItemDelegate, QCheckBox, QTableView, QWidget

class MyTableView(QWidget):
    def __init__(self):
        super().__init__()
        self.model = QAbstractTableModel(4, 3)

        self.tableView = QTableView()
        self.tableView.setModel(self.model)
        tvcb = TableViewCheckBox()
        self.model.setItemDelegateForColumn(0, tvcb)

class TableViewCheckBox(QItemDelegate):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        btn1 = QCheckBox()
        layout.addWidget(btn1)
        widget = QWidget()
        widget.setLayout(layout)



if __name__ == '__main__':
    a = QApplication(sys.argv)
    my_show = MyTableView()
    my_show.show()
    a.exec_()
