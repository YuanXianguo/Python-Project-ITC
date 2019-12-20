from PyQt5.QtCore import QObject, pyqtSignal


class SignalDemo(QObject):
    signal1 = pyqtSignal()
    signal2 = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        # 将信号signal1连接到sin_call1和sin_call2两个槽函数
        self.signal1.connect(self.sin_call1)
        self.signal1.connect(self.sin_call2)
        # 将信号signal2连接到槽函数信号signal1
        self.signal2.connect(self.signal1)
        # 发射信号
        self.signal1.emit()
        self.signal2.emit(1)
        # 断开signal1、signal2信号与各槽函数的连接
        self.signal1.disconnect(self.sin_call1)
        self.signal1.disconnect(self.sin_call2)
        self.signal2.disconnect(self.signal1)
        # 将信号signal1和信号signal2连接到同一个槽函数sin_call1
        self.signal1.connect(self.sin_call1)
        self.signal2.connect(self.sin_call1)
        # 再次发射信号
        self.signal1.emit()
        self.signal2.emit(1)

    def sin_call1(self):
        print('signal-1 emit')

    def sin_call2(self):
        print('signal-2 emit')


if __name__ == '__main__':
    signal = SignalDemo()
