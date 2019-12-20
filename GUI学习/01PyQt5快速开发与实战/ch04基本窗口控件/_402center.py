import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget

class Winform(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("主窗口放在屏幕中间例子")
        # 设置QWidget窗口的大小
        self.resize(370, 250)
        self.center()

    def center(self):
        # 计算显示屏幕的大小
        screen = QDesktopWidget().screenGeometry()
        # 获取QWidget窗口的大小
        size = self.geometry()
        # 将窗口移动到屏幕中间
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = Winform()
    my_show.show()
    sys.exit(app.exec_())

