import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFormLayout, QInputDialog

class InputDialogDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Input Dialog demo")
        self.setGeometry(300, 300, 300, 200)
        layout = QFormLayout()

        self.btn1 = QPushButton("获得列表里的选项")
        self.btn1.clicked.connect(self.get_item)
        self.le1 = QLineEdit()
        layout.addRow(self.btn1, self.le1)

        self.btn2 = QPushButton("获得字符串")
        self.btn2.clicked.connect(self.get_text)
        self.le2 = QLineEdit()
        layout.addRow(self.btn2, self.le2)

        self.btn3 = QPushButton("获得整数")
        self.btn3.clicked.connect(self.get_int)
        self.le3 = QLineEdit()
        layout.addRow(self.btn3, self.le3)

        self.setLayout(layout)

    def get_item(self):
        items = ("C", "C++", "Java", "Python")
        # 默认为列表第一项，可以修改列表内容
        item, ok = QInputDialog.getItem(self, "Select Input Dialog", "语言列表", items, 0, False)
        if ok:
            self.le1.setText(item)

    def get_text(self):
        text, ok = QInputDialog.getText(self, "Text Input Dialog", "输入姓名：")
        if ok:
            self.le2.setText(text)

    def get_int(self):
        num, ok = QInputDialog.getInt(self, "Integer Input Dialog", "输入数字")
        if ok:
            self.le3.setText(str(num))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = InputDialogDemo()
    my_show.show()
    sys.exit(app.exec_())
