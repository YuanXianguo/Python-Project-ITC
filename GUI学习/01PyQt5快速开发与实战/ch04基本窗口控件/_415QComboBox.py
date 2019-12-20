import sys
from PyQt5.QtWidgets import QApplication, QWidget,  QHBoxLayout, QComboBox, QLabel

class Comboxdemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ComBox demo")
        self.setGeometry(300, 300, 300, 200)
        layout = QHBoxLayout()

        self.lb1 = QLabel("")

        self.cb = QComboBox()
        self.cb.addItem("C")
        self.cb.addItem("C++")
        self.cb.addItems(["Java", "C#", "Python"])
        # 当下拉选项的索引发生改变时发射该信号
        self.cb.currentIndexChanged.connect(self.selection_change)

        layout.addWidget(self.cb)
        layout.addWidget(self.lb1)

        self.setLayout(layout)

    def selection_change(self, i):
        # 将下拉框所选项文本设置为标签文本
        self.lb1.setText(self.cb.currentText())
        print("Items in the list are:")
        for index in range(self.cb.count()):
            print("item {} = {}".format(str(index), self.cb.itemText(index)))
        print("Current index {} selection changed {}".format(i, self.cb.currentText()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = Comboxdemo()
    my_show.show()
    sys.exit(app.exec_())
