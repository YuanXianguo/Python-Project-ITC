import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLCDNumber, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, QTimer


class ThreadDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QThread Demo')
        layout = QVBoxLayout()
        self.sec = 0

        # 添加一个显示面板
        self.lcd_number = QLCDNumber()
        layout.addWidget(self.lcd_number)
        self.btn = QPushButton('测试')
        self.btn.clicked.connect(self.work_start)
        layout.addWidget(self.btn)
        self.setLayout(layout)

        # 实例化QTimer类和WorkThread类
        self.timer = QTimer()
        # 每次计时结束，触发count_time
        self.timer.timeout.connect(self.count_time)
        self.work_thread = WorkThread()

    def count_time(self):
        self.sec += 1
        self.lcd_number.display(self.sec)

    def work_start(self):
        self.timer.start(1000)   # 计时器每秒计数
        self.work_thread.start()
        # 当获得循环完毕的信号时，停止计数
        self.work_thread.trigger.connect(self.time_stop)

    def time_stop(self):
        self.timer.stop()
        print('运行结束用时:', self.lcd_number.value())


class WorkThread(QThread):
    """增加了一个WorkThread类，重写了run()函数"""
    trigger = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        for i in range(2000000000):
            pass
        # 循环完毕后发射信号
        self.trigger.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = ThreadDemo()
    my_show.show()
    sys.exit(app.exec_())
