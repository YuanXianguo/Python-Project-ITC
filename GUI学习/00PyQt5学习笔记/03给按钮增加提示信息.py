import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton
from PyQt5.QtGui import QFont

class Exp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置提示内容的字体和大小
        QToolTip.setFont(QFont('SansSerif', 10))

        # 支持html语法的加粗显示
        self.setToolTip('This is a <b>widget</b>')

        # 创建一个按钮，当鼠标悬浮于按钮时，提示'press and push'
        btn = QPushButton('Push', self)
        btn.setToolTip('Press and Push')
        btn.resize(btn.sizeHint()) # 自动给定一个合适的尺寸
        btn.move(40, 50)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('setToolTip')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Exp()
    sys.exit(app.exec_())

