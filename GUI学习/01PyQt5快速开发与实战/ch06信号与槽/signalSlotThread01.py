import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QThread
import time
class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('多线程例子1')
        self.setGeometry(300, 300, 300, 200)
        # 创建一个线程实例并设置名称、变量、信号与槽
        # self.thread_list = []
        # for i in range(2):
        #     self.thread_list.append('self.thread_{}'.format(i))
        btn1 = QPushButton('开始1')
        layout = QVBoxLayout()
        layout.addWidget(btn1)
        self.setLayout(layout)
        btn1.clicked.connect(self.start_1)
        btn2 = QPushButton('开始2')
        layout.addWidget(btn2)
        self.setLayout(layout)
        btn2.clicked.connect(self.start_2)
        btn3 = QPushButton('停止1')
        layout.addWidget(btn3)
        self.setLayout(layout)
        btn3.clicked.connect(self.stop_1)
        btn4 = QPushButton('停止2')
        layout.addWidget(btn4)
        self.setLayout(layout)
        btn4.clicked.connect(self.stop_2)

    def start_1(self):
        self.thread_1 = MyThread(0)
        self.thread_1.set_identity('thread1')
        self.thread_1.sinOut.connect(self.outText)
        self.thread_1.set_val(1)

    def start_2(self):
        self.thread_2 = MyThread(1)
        self.thread_2.set_identity('thread1')
        self.thread_2.sinOut.connect(self.outText)
        self.thread_2.set_val(2)

    def stop_1(self):
        self.thread_1.time = 0

    def stop_2(self):
        self.thread_2.time = 0

    def outText(self, text):
        print(text)

class MyThread(QThread):
    sinOut = pyqtSignal(str)
    def __init__(self, i):
        super().__init__()
        self.identity = None
        self.time = 1
        self.i = i

    def set_identity(self, text):
        self.identity = text

    def set_val(self, val):
        self.times = int(val)
        self.start()    # 执行线程的run方法

    def run(self):
        while self.time > 0 and self.identity:
            self.sinOut.emit('{}==>{}'.format(self.identity, str(self.times)))
            time.sleep(0.2)
            self.times += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = Main()
    my_show.show()
    sys.exit(app.exec_())
