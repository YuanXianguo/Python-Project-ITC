import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer, QDateTime


class TimerDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QTimer Demo')
        layout = QGridLayout()

        # 初始化一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)

        self.label = QLabel('显示当前时间')
        layout.addWidget(self.label, 0, 0, 1, 2)

        self.start_btn = QPushButton('开始')
        self.start_btn.clicked.connect(self.startTimer)
        layout.addWidget(self.start_btn, 1, 0)

        self.end_btn = QPushButton('结束')
        self.end_btn.clicked.connect(self.endTimer)
        layout.addWidget(self.end_btn, 1, 1)

        self.setLayout(layout)

    def showTime(self):
        # 获取系统现在的时间
        time = QDateTime.currentDateTime()
        # 设置系统时间显示格式
        time_display = time.toString('yyyy-MM-dd hh:mm:ss dddd')
        self.label.setText(time_display)

    def startTimer(self):
        # 设置时间间隔为1秒并启动定时器
        self.timer.start(2000)
        self.start_btn.setEnabled(False)
        self.end_btn.setEnabled(True)

    def endTimer(self):
        self.timer.stop()
        self.start_btn.setEnabled(True)
        self.end_btn.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = TimerDemo()
    my_show.show()
    sys.exit(app.exec_())
