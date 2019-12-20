import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

class Exp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """自定义方法来完成界面的初始化，下面三个方法都继承自QWidget基类"""
        # setGeometry同时设定窗口大小和位置，兼具move()(在前)和resize()的作用
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Icon')

        # 设置了这个应用的图标，为此我们创建了QIcon对象
        self.setWindowIcon(QIcon('迪迪003'))

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Exp()
    sys.exit(app.exec_())

