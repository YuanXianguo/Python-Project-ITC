import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem

class tableWidgetDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QTableWidget Demo")
        self.setGeometry(300, 300, 300, 200)
        layout = QHBoxLayout()

        # 创建一个QTableWidget对象，并设置表格为4行3列
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(4)    # 设置QTableWidget表格控件为4行
        self.table_widget.setColumnCount(3) # 设置QTableWidget表格控件为3列
        layout.addWidget(self.table_widget)
        # 设置表格头
        self.table_widget.setHorizontalHeaderLabels(['姓名', '性别', '体重(kg)'])
        # 生成QTableWidgetItem对象，并加载到表格中
        newItem1 = QTableWidgetItem('张三')
        self.table_widget.setItem(0, 0, newItem1)
        newItem2 = QTableWidgetItem('男')
        self.table_widget.setItem(0, 1, newItem2)
        newItem3 = QTableWidgetItem('160')
        self.table_widget.setItem(0, 2, newItem3)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = tableWidgetDemo()
    my_show.show()
    sys.exit(app.exec_())


