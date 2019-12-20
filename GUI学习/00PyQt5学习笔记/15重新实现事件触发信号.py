import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal, QObject

class Communicate(QObject):
    """创建了一个closeApp的信号，之前的笔记中我们创建的都是QPushButton,
    QLabel等在窗口中可见的部件，实际上我们也可以创建pyqtSignal()信号函数"""
    closeApp = pyqtSignal()

class MousePress(QMainWindow):
    """docstring for ex"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.c = Communicate()

        self.c.closeApp.connect(self.close)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Emitting')
        self.show()

    def mousePressEvent(self, event):
        self.c.closeApp.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MousePress()
    sys.exit(app.exec_())
