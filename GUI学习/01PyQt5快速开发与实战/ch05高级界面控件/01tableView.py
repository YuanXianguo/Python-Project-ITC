import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableView, QHeaderView
from PyQt5.QtGui import *

class TableViewDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTableView表格视图控件的例子")
        self.setGeometry(300, 300, 300, 200)
        layout = QVBoxLayout()

        # 创建自定义模型
        self.model = QStandardItemModel(4, 4)
        self.model.setHorizontalHeaderLabels(['标题1', '标题2', '标题3', '标题4'])
        for row in range(4):
            for column in range(4):
                item = QStandardItem("row {}, column {}".format(row, column))
                self.model.setItem(row, column, item)

        # 创建QTableView表格，并添加自定义模型
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        layout.addWidget(self.table_view)
        self.setLayout(layout)

    def else_(self):
        # 表格并没有填满窗口，每列可以自由拉动，如果需要填满窗口，可以添加以下代码
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 添加数据
        self.model.appendRow([QStandardItem('new'), QStandardItem('new'), QStandardItem('new'), QStandardItem('new')])
        # 删除数据1
        # 选取当前选中的所有行
        indexs = self.table_view.selectionModel().selection().indexes()
        # 选取第一行
        if len(indexs) > 0:
            index = indexs[0]
            self.model.removeRows(index.row(), 1)
        # 删除数据2
        # 如果在表格中什么也不选，那么默认删除的是第一行，也就是索引为0的行；
        # 选中一行是就删除这一行；
        # 选中多行时，如果焦点在最后一行，就删除这一行；
        index = self.table_view.currentIndex()
        self.model.removeRow(index.row())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = TableViewDemo()
    my_show.show()
    sys.exit(app.exec_())


