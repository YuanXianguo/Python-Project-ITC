import sys
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QStackedWidget,\
QFormLayout, QHBoxLayout, QLineEdit, QRadioButton, QCheckBox, QLabel

class StackedWidgetDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StackedWidget Demo")
        self.setGeometry(300, 300, 300, 200)
        layout = QHBoxLayout()

        # QStackedWidget控件不能在页面之间切换，它与当前选中的QListWidget控件中的选项进行连接
        self.left_list = QListWidget()
        self.left_list.insertItem(0, '联系方式')
        self.left_list.insertItem(1, '个人详细信息')
        self.left_list.insertItem(2, '教育程度')
        # 将QListWidget的currentRowChanged信号与display()槽函数相关联，从而改变堆叠控件的视图
        self.left_list.currentRowChanged.connect(self.display)
        layout.addWidget(self.left_list)

        # 创建一个堆栈窗口控件,并添加三个子控件
        self.stack = QStackedWidget()
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        layout.addWidget(self.stack)
        self.setLayout(layout)

    def stack1UI(self):
        layout = QFormLayout()
        layout.addRow('姓名', QLineEdit())
        layout.addRow('地址', QLineEdit())
        self.stack1.setLayout(layout)

    def stack2UI(self):
        layout = QFormLayout()
        sex_layout = QHBoxLayout()
        sex_layout.addWidget(QRadioButton('男'))
        sex_layout.addWidget(QRadioButton('女'))
        layout.addRow(QLabel('性别'), sex_layout)
        layout.addRow('生日', QLineEdit())
        self.stack2.setLayout(layout)

    def stack3UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel('科目'))
        layout.addWidget(QCheckBox('物理'))
        layout.addWidget(QCheckBox('高数'))
        self.stack3.setLayout(layout)

    def display(self, i):
        # 设置当前可见的选项卡所在的索引
        self.stack.setCurrentIndex(i)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = StackedWidgetDemo()
    my_show.show()
    sys.exit(app.exec_())
