import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton

class TextEditDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTextEdit例子")
        self.resize(300, 270)

        # 初始化
        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.btn_press1 = QPushButton("显示文本")
        self.btn_press2 = QPushButton("显示HTML")

        # 设置布局
        layout.addWidget(self.text_edit)
        layout.addWidget(self.btn_press1)
        layout.addWidget(self.btn_press2)
        self.setLayout(layout)
        # 建立信号槽
        self.btn_press1.clicked.connect(self.btn_press1_clicked)
        self.btn_press2.clicked.connect(self.btn_press2_clicked)

    def btn_press1_clicked(self):
        # 设置多行文本框的文本内容
        self.text_edit.setPlainText("Hello PyQt5!\n单击按钮")

    def btn_press2_clicked(self):
        # 设置多行文本框的内容为HTML文档
        self.text_edit.setHtml("<font color='red' size='6'><red>Hello PyQt5!\n单击按钮</font>")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = TextEditDemo()
    my_show.show()
    sys.exit(app.exec_())
