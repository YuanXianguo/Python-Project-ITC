import sys
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit, QLabel, QGridLayout

class QlabelDemo(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QLabel快捷键例子")

        # 初始化
        layout = QGridLayout(self)
        lb1 = QLabel('&Name', self)
        ed1 = QLineEdit(self)
        lb1.setBuddy(ed1)

        lb2 = QLabel('&Password', self)
        ed2 = QLineEdit(self)
        lb2.setBuddy(ed2)

        btn_ok = QPushButton('&OK')
        btn_cancel = QPushButton('&Cancel')

        # 设置布局
        # 参数分别表示：控件，开始行、列，占用行、列，对齐方式（这里没有）
        layout.addWidget(lb1, 0, 0)
        layout.addWidget(ed1, 0, 1, 1, 2)
        layout.addWidget(lb2, 1, 0)
        layout.addWidget(ed2, 1, 1, 1, 2)
        layout.addWidget(btn_ok, 2, 1)
        layout.addWidget(btn_cancel, 2, 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = QlabelDemo()
    my_show.show()
    sys.exit(app.exec_())
