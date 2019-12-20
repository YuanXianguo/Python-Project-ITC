import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip
from PyQt5.QtGui import QFont

class Winform(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置气泡提示信息的字体与字号大小
        QToolTip.setFont(QFont('SansSerif', 10))
        # setToolTip()方法创建工具提示，该方法接收富文本格式的参数
        self.setToolTip("这是一个<b>气泡提示</b>")
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("气泡提示demo")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = Winform()
    my_show.show()
    sys.exit(app.exec_())
