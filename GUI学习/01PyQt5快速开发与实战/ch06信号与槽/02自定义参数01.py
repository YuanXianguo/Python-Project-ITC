import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QMessageBox


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('自定义参数例子')
        self.setGeometry(300, 300, 300, 200)
        layout = QHBoxLayout()

        btn1 = QPushButton('Button 1')
        btn1.clicked.connect(lambda: self.onButtonClick(1))
        layout.addWidget(btn1)

        btn2 = QPushButton('Button 2')
        btn2.clicked.connect(lambda: self.onButtonClick(2))
        layout.addWidget(btn2)

        self.setLayout(layout)

    def onButtonClick(self, n):
        QMessageBox.information(self, '信息提示框', 'Button {} clicked'.format(n))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = Main()
    my_show.show()
    sys.exit(app.exec_())




