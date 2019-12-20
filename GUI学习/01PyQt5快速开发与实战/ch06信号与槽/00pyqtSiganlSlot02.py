from PyQt5.QtCore import QObject, pyqtSignal

class PyQtSignal(QObject):
    """信号对象类"""
    # 定义一个信号
    send_msg = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    def run(self):
        """发射信号函数"""
        self.send_msg.emit('Hello PyQt5')

class PyQtSlot(QObject):
    """槽对象类"""
    def __init__(self):
        super().__init__()

    def get(self, msg):
        """槽函数"""
        print("QSlot get msg =>{}".format(msg))

if __name__ == '__main__':
    send = PyQtSignal()
    slot = PyQtSlot()
    print('---把信号绑定到槽函数上---')
    send.send_msg.connect(slot.get)
    send.run()
    print('---把信号与槽函数的连接断开---')
    send.send_msg.disconnect(slot.get)
    send.run()
