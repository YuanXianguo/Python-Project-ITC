import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

class Icon(QWidget):
    """创建一个名为Icon的窗口类，继承自QWidget类"""
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        # 设置窗口在屏幕上的位置和设置窗口本身的大小，前两个参数是x,y，后两个是width,height
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("程序图标")
        # 设置程序图标，需要要给QIcon类型的对象作为参数，需要导入模块
        self.setWindowIcon(QIcon('pangdi.jpg'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = Icon()
    my_show.show()
    sys.exit(app.exec_())
