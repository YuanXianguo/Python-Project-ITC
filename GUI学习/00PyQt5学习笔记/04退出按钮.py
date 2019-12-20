import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import QCoreApplication

class Exp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        qtn = QPushButton('Quit', self)
        qtn.resize(qtn.sizeHint())
        # 信号槽
        qtn.clicked.connect(QCoreApplication.quit)
        qtn.move(40, 50)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Quit')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Exp()
    sys.exit(app.exec_())

