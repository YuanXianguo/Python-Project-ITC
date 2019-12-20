import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QFormLayout, \
QHBoxLayout, QLineEdit, QRadioButton, QCheckBox, QLabel

class TabWidgetDemo(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TabWidget Demo")
        self.setGeometry(300, 300, 300, 200)
        self.setTabPosition(QTabWidget.South)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.addTab(self.tab1, 'Tab 1')
        self.addTab(self.tab2, 'Tab 2')
        self.addTab(self.tab3, 'Tab 3')
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

    def tab1UI(self):
        layout = QFormLayout()
        layout.addRow('姓名', QLineEdit())
        layout.addRow('地址', QLineEdit())
        self.setTabText(0, '联系方式')  # 设置选项卡的显示值
        self.tab1.setLayout(layout)

    def tab2UI(self):
        layout = QFormLayout()
        sex_layout = QHBoxLayout()
        sex_layout.addWidget(QRadioButton('男'))
        sex_layout.addWidget(QRadioButton('女'))
        layout.addRow(QLabel('性别'), sex_layout)
        layout.addRow('生日', QLineEdit())
        self.setTabText(1, '个人详细信息')
        self.tab2.setLayout(layout)

    def tab3UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel('科目'))
        layout.addWidget(QCheckBox('物理'))
        layout.addWidget(QCheckBox('高数'))
        self.setTabText(2, '教育程度')
        self.tab3.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = TabWidgetDemo()
    my_show.show()
    sys.exit(app.exec_())
