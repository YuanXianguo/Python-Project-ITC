import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QListWidget, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, QTimer


class ThreadDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QThread Demo')
        layout = QGridLayout()
        # 设置界面
        self.list_file = QListWidget()
        layout.addWidget(self.list_file, 0, 0, 1, 2)
        self.start_btn = QPushButton('开始')
        self.start_btn.clicked.connect(self.slot_start)
        layout.addWidget(self.start_btn, 1, 1)
        self.setLayout(layout)

        # 实例化线程类Worker
        self.thread = Worker()
        self.thread.sinOut.connect(self.slot_add)

    def slot_start(self):
        self.start_btn.setEnabled(False)
        self.thread.start()

    def slot_add(self, file_inf):
        """子列表控件中动态添加字符串条目"""
        self.list_file.addItem(file_inf)


class Worker(QThread):
    """定义一个线程类，继承自QThread类，当线程启动后，执行run()函数"""
    # 自定义发射信号
    sinOut = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.working = True
        self.num = 0

    def __del__(self):
        self.working = False
        self.wait()

    def run(self):
        while self.working == True:
            file_str = 'File index{0}'.format(self.num)
            self.num += 1
            # 发射信号
            self.sinOut.emit(file_str)
            # 线程休眠2秒
            self.sleep(2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = ThreadDemo()
    my_show.show()
    QTimer.singleShot(10000, app.quit)
    sys.exit(app.exec_())
