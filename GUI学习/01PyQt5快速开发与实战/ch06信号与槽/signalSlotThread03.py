import sys
import time
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, QThread, QDateTime


class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyQt5界面实时更新例子')
        self.resize(300, 100)
        self.input = QLineEdit(self)
        self.input.resize(300, 100)
        self.initUI()

    def initUI(self):
        self.backend = BackendThread()  # 创建线程
        self.backend.update_date.connect(self.handleDisplay)  # 连接信号
        self.backend.start()  # 开始线程

    def handleDisplay(self, i,j):
        """将当前时间输出到文本框"""
        print(i,j)


class BackendThread(QThread):
    # 通过类成员对象定义信号
    update_date = pyqtSignal(int, int)

    # 处理业务逻辑
    def run(self):
        while True:
            for i in range(1,21):
                for j in range(2):
                    self.update_date.emit(i, j)
                    time.sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = Window()
    my_show.show()
    sys.exit(app.exec_())
